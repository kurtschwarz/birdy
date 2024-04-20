import * as process from 'node:process'
import { asyncExitHook } from 'exit-hook'

import { config } from './config.js'
import { initializeFastify } from './initializers/fastify.js'
import { initializeConnect } from './initializers/connect.js'
import * as mqtt from './services/mqtt/index.js'

asyncExitHook(
  async () =>
    await mqtt.publish(mqtt.Topic.COLLECTOR_SERVICE_OFFLINE, {
      collectorId: config.id,
      now: new Date(),
    }),
  { wait: 500 },
)

async function main(): Promise<void> {
  await mqtt.publish(mqtt.Topic.COLLECTOR_SERVICE_ONLINE, {
    collectorId: config.id,
    now: new Date(),
  })

  const connectRoutes = await initializeConnect()
  const server = await initializeFastify(connectRoutes)
  await server.listen({
    host: '0.0.0.0',
    port: config.port,
  })
}

export default main().catch(error => {
  process.stderr.write(error.message)
  process.exit(1)
})
