import type { ConnectRouter } from '@connectrpc/connect'

import { CollectorService } from '@birdy/protos'

import { client } from '../initializers/prisma.js'
import { storeRecording } from '../services/storage/index.js'
import * as kafka from '../services/kafka/index.js'

export const initializeConnect = async (): Promise<(router: ConnectRouter) => ConnectRouter> => {
  return (router: ConnectRouter): ConnectRouter => {
    return router.service(CollectorService, {
      async register(request) {
        try {
          await client.$transaction([
            client.location.upsert({
              where: { id: request.location.id },
              create: {
                id: request.location.id,
                latitude: request.location.latitude,
                longitude: request.location.longitude,
              },
              update: {
                latitude: request.location.latitude,
                longitude: request.location.longitude,
              },
            }),
            client.recorder.upsert({
              where: { id: request.recorder.id },
              create: { id: request.recorder.id, locationId: request.location.id },
              update: { locationId: request.location.id },
            }),
          ])

          return {
            status: {
              code: 0,
            },
          }
        } catch {
          return {
            status: {
              code: 1,
            },
          }
        }
      },
      async collect(requests) {
        let chunks = {}

        for await (const request of requests) {
          chunks[request.recording.id] = {
            recorder: request.recorder,
            location: request.location,
            recording: {
              ...request.recording,
              buffers: [
                ...(chunks?.[request.recording.id]?.buffers || []),
                request.recording.buffer,
              ],
            },
          }
        }

        for (const recordingId of Object.keys(chunks)) {
          const storageUri = await storeRecording(
            recordingId,
            Buffer.concat(chunks[recordingId].recording.buffers),
          )

          await kafka.publish('queuing.recordings.unanalyzed', [
            {
              key: recordingId,
              value: JSON.stringify({
                recording: {
                  id: recordingId,
                  duration: 15,
                  startTime: chunks[recordingId].recording.startTime,
                  endTime: chunks[recordingId].recording.endTime,
                  storageUri: storageUri,
                },
                location: {
                  id: chunks[recordingId].location.id,
                  latitude: chunks[recordingId].location.latitude,
                  longitude: chunks[recordingId].location.longitude,
                },
              }),
            },
          ])
        }

        return {
          ok: true,
        }
      },
    })
  }
}
