import * as process from 'node:process'

import { initializeFastify } from './initializers/fastify'
import { initializeConnect } from './initializers/connect'

async function main(): Promise<void> {
  const connectRoutes = await initializeConnect()
  const server = await initializeFastify(connectRoutes)
  await server.listen({
    host: '0.0.0.0',
    port: 3000
  })
}

export default main()
  .catch((error) => {
    process.stderr.write(error.message)
    process.exit(1)
  })
