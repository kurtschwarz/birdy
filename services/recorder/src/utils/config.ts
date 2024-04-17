import yargs from 'yargs'

const getArgvWithoutBin = (): string[] => {
  let argv = process.argv.slice(2)
  if (argv?.[0] === '--') {
    argv.shift()
  }

  return argv
}

const argvParser = yargs(getArgvWithoutBin())
  .option('id', {
    string: true,
  })
  .option('log-level', {
    string: true,
    default: 'info'
  })
  .option('location-id', {
    string: true,
  })
  .option('location-lat', {
    string: true,
  })
  .option('location-long', {
    string: true,
  })
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

class Config {
  protected argv: ReturnType<typeof argvParser.parseSync>

  constructor () {
    this.argv = argvParser.parseSync()
  }

  get id (): string {
    return this.argv.id
  }

  get logLevel(): string {
    return this.argv.logLevel
  }

  get locationId (): string {
    return this.argv.locationId
  }

  get locationLat (): string {
    return this.argv.locationLat
  }

  get locationLong (): string {
    return this.argv.locationLong
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
