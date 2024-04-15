import type { ConnectRouter } from '@connectrpc/connect'

import { CollectorService } from '@birdy/protos'

import { storeRecording } from '../services/storage/index.js'

export const initializeConnect = async (): Promise<(router: ConnectRouter) => ConnectRouter> => {
  return (router: ConnectRouter): ConnectRouter => {
    return router.service(CollectorService, {
      async collect (requests) {
        const buffers = []
        for await (const request of requests) {
          buffers.push(request.recording.buffer)
        }

        await storeRecording(
          Buffer.concat(buffers)
        )

        return {
          ok: true
        }
      }
    })
  }
}
