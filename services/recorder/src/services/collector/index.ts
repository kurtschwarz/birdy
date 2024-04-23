import { createPromiseClient } from '@connectrpc/connect'
import { createConnectTransport } from '@connectrpc/connect-node'

import { CollectorService } from '@birdy/protos'

import { config } from '../../config.js'

export const collectorService = createPromiseClient(
  CollectorService,
  createConnectTransport({
    httpVersion: '1.1',
    baseUrl: config.collectorEndpoint,
  }),
)
