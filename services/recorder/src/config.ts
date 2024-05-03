import yargs from 'yargs'

import { getArgvWithoutBin, BaseConfig } from '@birdy/config'

const argvParser = yargs(getArgvWithoutBin())
  .option('id', { string: true, demandOption: true })
  .option('log-level', { string: true, default: 'info' })
  // location settings
  .option('location-id', { string: true, demandOption: true })
  .option('location-lat', { number: true, demandOption: true })
  .option('location-long', { number: true, demandOption: true })
  // recording settings
  .option('recording-duration', { number: true, default: 15 })
  // worker settings
  .option('transfer-chunk-size', { number: true, default: 512000 })
  .option('worker-queue-retry-delay', { number: true, default: 200 })
  .option('worker-queue-retry-delay-max', { number: true, default: 5000 })
  .option('worker-queue-retry-attempts-max', { number: true, default: 10 })
  // collector settings
  .option('collector-endpoint', { string: true })
  // mqtt settings
  .option('mqtt-enabled', { boolean: true, default: false })
  .option('mqtt-broker', { string: true, default: null })
  // inherit from process.env
  .env(true)

class Config extends BaseConfig<typeof argvParser, ReturnType<typeof argvParser.parseSync>> {
  constructor() {
    super('@birdy/recorder', argvParser)
  }

  get id(): string {
    return this.argv.id
  }

  get logLevel(): string {
    return this.argv.logLevel
  }

  get locationId(): string {
    return this.argv.locationId
  }

  get locationLat(): number {
    return this.argv.locationLat
  }

  get locationLong(): number {
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

  get collectorEndpoint(): string {
    return this.argv.collectorEndpoint
  }

  get mqttEnabled(): boolean {
    return this.argv.mqttEnabled
  }
  get mqttBroker(): string {
    return this.argv.mqttBroker
  }
}

export const config = new Config()
