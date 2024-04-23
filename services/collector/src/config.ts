import yargs from 'yargs'

import { getArgvWithoutBin, BaseConfig } from '@birdy/config'

const argvParser = yargs(getArgvWithoutBin())
  .option('id', { string: true })
  .option('port', { number: true, default: 3000 })

  .option('storage', { choices: ['s3'] })
  .option('storageS3Endpoint', { string: true })
  .option('storageS3AccessKey', { string: true })
  .option('storageS3SecretKey', { string: true })
  .option('storageS3Bucket', { string: true })

  .option('mqttEnabled', { boolean: true, default: false })
  .option('mqttBroker', { string: true, default: null })

  .option('kafkaEnabled', { boolean: true, default: false })
  .option('kafkaBrokers', { string: true, array: true, default: [] })
  .env(true)

class Config extends BaseConfig<typeof argvParser, ReturnType<typeof argvParser.parseSync>> {
  constructor() {
    super('@birdy/collector', argvParser)
  }

  get id(): string {
    return this.argv.id
  }

  get port(): number {
    return this.argv.port
  }

  get storage(): string {
    return this.argv.storage
  }

  get storageS3Endpoint(): string {
    return this.argv.storageS3Endpoint
  }

  get storageS3AccessKey(): string {
    return this.argv.storageS3AccessKey
  }

  get storageS3SecretKey(): string {
    return this.argv.storageS3SecretKey
  }

  get storageS3Bucket(): string {
    return this.argv.storageS3Bucket
  }

  get mqttEnabled(): boolean {
    return this.argv.mqttEnabled
  }

  get mqttBroker(): string {
    return this.argv.mqttBroker
  }

  get kafkaEnabled(): boolean {
    return this.argv.kafkaEnabled
  }

  get kafkaBrokers(): string[] {
    return this.argv.kafkaBrokers
  }
}

export const config = new Config()
