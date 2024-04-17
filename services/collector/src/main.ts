import * as process from 'node:process'

import { config } from './config.js'
import { initializeFastify } from './initializers/fastify.js'
import { initializeConnect } from './initializers/connect.js'

async function main(): Promise<void> {
  console.log({ config })

  const connectRoutes = await initializeConnect()
  const server = await initializeFastify(connectRoutes)
  await server.listen({
    host: '0.0.0.0',
    port: config.port
  })
}

export default main()
  .catch((error) => {
    process.stderr.write(error.message)
    process.exit(1)
  })
