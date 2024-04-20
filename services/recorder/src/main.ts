import * as process from 'node:process'
import { asyncExitHook } from 'exit-hook'

import './initializers/dayjs.js'

import { config } from './utils/index.js'
import * as audio from './services/audio/index.js'
import * as recorder from './services/recorder/index.js'
import * as mqtt from './services/mqtt/index.js'
import * as worker from './worker.js'

asyncExitHook(
  async () =>
    await mqtt.publish(mqtt.Topic.RECORDER_SERVICE_OFFLINE, {
      recorderId: config.id,
      now: new Date(),
    }),
  { wait: 500 },
)

async function main(): Promise<void> {
  await mqtt.publish(mqtt.Topic.RECORDER_SERVICE_ONLINE, { recorderId: config.id, now: new Date() })

  await recorder.register()
  await worker.start()
  await audio.capture({ duration: config.recordingDuration })

  audio.events.on('recording', async recording => await worker.enqueue(recording))
}

export default main().catch(error => {
  process.stderr.write(error.message)
  process.exit(1)
})
