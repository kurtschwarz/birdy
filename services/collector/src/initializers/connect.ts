import type { ConnectRouter } from '@connectrpc/connect'

import { CollectorService } from '@birdy/protos'

import { storeRecording } from '../services/storage/index.js'

export const initializeConnect = async (): Promise<(router: ConnectRouter) => ConnectRouter> => {
  return (router: ConnectRouter): ConnectRouter => {
    return router.service(CollectorService, {
      async collect (requests) {
        let recordings = {}

        for await (const request of requests) {
          recordings[request.recording.id] = {
            id: request.recording.id,
            buffers: [
              ...(recordings?.[request.recording.id]?.buffers || []),
              request.recording.buffer,
            ]
          }
        }

        for (const recordingId of Object.keys(recordings)) {
          await storeRecording(
            recordingId,
            Buffer.concat(recordings[recordingId].buffers)
          )
        }

        return {
          ok: true
        }
      }
    })
  }
}
