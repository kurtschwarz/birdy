import { fastify, FastifyInstance } from 'fastify'
import { fastifyConnectPlugin } from '@connectrpc/connect-fastify'
import { ConnectRouter } from '@connectrpc/connect'

export const initializeFastify = async (
  connectRoutes: (router: ConnectRouter) => ConnectRouter,
): Promise<FastifyInstance> => {
  const server = fastify()
  await server.register(fastifyConnectPlugin, {
    routes: connectRoutes,
  })

  return server
}
