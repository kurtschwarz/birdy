import yargs from 'yargs'

import { getArgvWithoutBin, BaseConfig } from '@birdy/config'

const argvParser = yargs(getArgvWithoutBin())
  .option('port', { number: true, default: 3000 })
  .option('minioEndpoint', { string: true })
  .option('minioPort', { number: true })
  .option('minioUser', { string: true, alias: 'minioRootUser' })
  .option('minioPassword', { string: true, alias: 'minioRootPassword' })
  .option('storageBucketName', { string: true, default: 'birdy-recordings-unprocessed' })
  .env(true)

class Config extends BaseConfig<typeof argvParser, ReturnType<typeof argvParser.parseSync>> {
  constructor () {
    super('@birdy/collector', argvParser)
  }

  get port (): number { return this.argv.port }

  get minioEndpoint (): string { return this.argv.minioEndpoint }
  get minioPort (): number { return this.argv.minioPort }
  get minioUser (): string { return this.argv.minioUser }
  get minioPassword (): string { return this.argv.minioPassword }

  get storageBucketName (): string { return this.argv.storageBucketName }
}

export const config = new Config()
