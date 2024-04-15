import * as process from 'node:process'

import './initializers/dayjs.js'
import { config } from './utils/config.js'
import * as audio from './services/audio/index.js'
import * as worker from './worker.js'

async function main(): Promise<void> {
  await worker.start()
  await audio.capture({ duration: config.recordingDuration })
  audio.events.on('recording', async (recording) => await worker.enqueue(recording))
}

export default main()
  .catch((error) => {
    process.stderr.write(error.message)
    process.exit(1)
  })
