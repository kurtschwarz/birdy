import yargs, { Argv } from 'yargs'

class Config {
  argv: Argv

  constructor () {
    this.argv = yargs(process.argv.slice(2))
      .option('recording-duration', {
        number: true,
        default: 15
      })
      .option('transfer-chunk-size', {
        number: true,
        default: 512000 // 512kb
      })
      .option('worker-queue-retry-delay', {
        number: true,
        default: 200
      })
      .option('worker-queue-retry-delay-max', {
        number: true,
        default: 5000 // 5 seconds
      })
      .option('worker-queue-retry-attempts-max', {
        number: true,
        default: 10
      })
      .parseSync()
  }

  get recordingDuration(): number {
    return this.argv.recordingDuration
  }

  get transferChunkSize(): number {
    return this.argv.transferChunkSize
  }

  get workerQueueRetryDelay(): number {
    return this.argv.workerQueueRetryDelay
  }

  get workerQueueRetryDelayMax(): number {
    return this.argv.workerQueueRetryDelayMax
  }

  get workerQueueRetryAttemptsMax(): number {
    return this.argv.workerQueueRetryAttemptsMax
  }
}

export const config = new Config()
