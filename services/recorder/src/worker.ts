import { isMainThread, parentPort, Worker, SHARE_ENV } from 'node:worker_threads'
import fastq, { queueAsPromised } from 'fastq'
import NodeCache from 'node-cache'
import { Timestamp } from '@bufbuild/protobuf'

import type { Recording } from './types/index.js'
import { config, logger } from './utils/index.js'
import { collectorService } from './services/collector/index.js'

let instance: Worker
let cache: NodeCache
let queue: queueAsPromised<{ recordingId: string; attempt: number }>

export const start = async (): Promise<void> => {
  logger.info('starting background worker')

  try {
    if (isMainThread) {
      if (instance) {
        await instance.terminate()
      }

      if (process.env.NODE_ENV === 'development') {
        const result = await (
          await import('esbuild')
        ).build({
          entryPoints: ['src/worker.ts'],
          bundle: true,
          write: false,
          platform: 'node',
          external: ['esbuild'],
        })

        instance = new Worker(
          Buffer.from(result.outputFiles[0].contents.buffer).toString('utf-8'),
          {
            eval: true,
            env: SHARE_ENV,
          },
        )
      } else {
        instance = new Worker('./worker.js')
      }
    }
  } catch (error) {
    console.error(error)
  }
}

export const enqueue = async (recording: Recording): Promise<void> => {
  instance.postMessage({ recording })
}

async function worker(): Promise<void> {
  if (!isMainThread) {
    logger.info('background worker ready')

    cache = new NodeCache({
      useClones: false,
    })

    queue = fastq.promise(async ({ recordingId, attempt }): Promise<void> => {
      if (attempt > 0) {
        const delay = config.workerQueueRetryDelay * Math.pow(2, attempt)
        await new Promise(resolve =>
          setTimeout(resolve, Math.min(delay, config.workerQueueRetryDelayMax)),
        )
      }

      logger.info({ recordingId, attempt }, 'processing recording')

      await collectorService.collect(
        (async function* (recordingId) {
          const recording = cache.get(recordingId) as Recording
          const chunkSize = config.transferChunkSize
          for (let i = 0; i < recording.buffer.length; i += chunkSize) {
            yield {
              recorder: {
                id: recording.id,
              },
              recording: {
                id: recording.id,
                startTime: Timestamp.fromDate(recording.startTime),
                endTime: Timestamp.fromDate(recording.endTime),
                buffer: recording.buffer.subarray(i, i + chunkSize),
              },
            }
          }
        })(recordingId),
      )
    }, 1)

    queue.error((error, { recordingId, attempt }) => {
      if (error && attempt <= config.workerQueueRetryAttemptsMax) {
        queue.unshift({ recordingId, attempt: attempt + 1 })
      }
    })

    parentPort.on('message', async ({ recording }: { recording: Recording }) => {
      cache.set(recording.id, recording)
      queue.push({ recordingId: recording.id, attempt: 0 })
    })
  }
}

export default worker()
