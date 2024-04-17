import * as fs from 'node:fs'
import * as path from 'node:path'
import { Argv as Yargv } from 'yargs'

export const getArgvWithoutBin = (): string[] => {
  let argv = process.argv.slice(2)
  if (argv?.[0] === '--') {
    argv.shift()
  }

  return argv
}

export class BaseConfig<Parser extends Yargv<{}>, Argv> {
  protected readonly service: string
  protected readonly argv: Argv

  constructor (
    service: string,
    parser: Parser
  ) {
    let configPath
    let config

    try {
      configPath = path.join('/', 'birdy', 'services', service.replace('@birdy/', ''), '.config.json').trim()
      config = fs.existsSync(configPath) ? JSON.parse(fs.readFileSync(configPath, 'utf-8'))|| {} : {}
    } catch {
      config = {}
    }

    this.service = service
    this.argv = parser
      .config(config)
      .parseSync() as Argv
  }
}
