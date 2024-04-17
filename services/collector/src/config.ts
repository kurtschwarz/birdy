import yargs from 'yargs'

const getArgvWithoutBin = (): string[] => {
  let argv = process.argv.slice(2)
  if (argv?.[0] === '--') {
    argv.shift()
  }

  return argv
}

const argvParser = yargs(getArgvWithoutBin())
  .option('port', {
    number: true,
    default: 3000
  })

class Config {
  protected argv: ReturnType<typeof argvParser.parseSync>

  constructor () {
    this.argv = argvParser.parseSync()
  }

  get port(): number {
    return this.argv.port
  }
}

export const config = new Config()
