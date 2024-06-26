import * as fs from 'node:fs'
import { Argv as Yargv } from 'yargs'
import { isMainThread } from 'node:worker_threads'

export const getArgvWithoutBin = (): string[] => {
  let argv = process.argv.slice(isMainThread ? 2 : 4)
  if (argv?.[0] === '--') {
    argv.shift()
  }

  return argv
}

export class BaseConfig<Parser extends Yargv<{}>, Argv> {
  protected readonly service: string
  protected readonly argv: Argv

  constructor(service: string, parser: Parser) {
    this.service = service
    this.argv = parser
      .config('config', configPath => {
        try {
          return JSON.parse(fs.readFileSync(configPath, 'utf-8'))
        } catch {
          return {}
        }
      })
      .parseSync() as Argv
  }
}
