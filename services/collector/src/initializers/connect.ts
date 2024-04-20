import type { ConnectRouter } from '@connectrpc/connect'

import { CollectorService } from '@birdy/protos'

import { client } from '../initializers/prisma.js'
import { storeRecording } from '../services/storage/index.js'

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
        let recordings = {}

        for await (const request of requests) {
          recordings[request.recording.id] = {
            id: request.recording.id,
            buffers: [
              ...(recordings?.[request.recording.id]?.buffers || []),
              request.recording.buffer,
            ],
          }
        }

        for (const recordingId of Object.keys(recordings)) {
          await storeRecording(recordingId, Buffer.concat(recordings[recordingId].buffers))
        }

        return {
          ok: true,
        }
      },
    })
  }
}
