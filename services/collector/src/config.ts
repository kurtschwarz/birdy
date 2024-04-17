import yargs from 'yargs'

import { getArgvWithoutBin, BaseConfig } from '@birdy/config'

const argvParser = yargs(getArgvWithoutBin())
  .option('port', {
    number: true,
    default: 3000
  })

class Config extends BaseConfig<typeof argvParser, ReturnType<typeof argvParser.parseSync>> {
  constructor () {
    super('@birdy/collector', argvParser)
  }

  get port (): number {
    return this.argv.port
  }
}

export const config = new Config()
