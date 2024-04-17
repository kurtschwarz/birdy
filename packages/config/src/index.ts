import { Argv as Yargv } from 'yargs'

export const getArgvWithoutBin = (): string[] => {
  let argv = process.argv.slice(2)
  if (argv?.[0] === '--') {
    argv.shift()
  }

  return argv
}

export class BaseConfig<Parser extends Yargv<{}>, Argv> {
  protected argv: Argv

  constructor (parser: Parser) {
    this.argv = parser.parseSync() as Argv
  }
}
