import { createPromiseClient } from '@connectrpc/connect'
import { createConnectTransport } from '@connectrpc/connect-node'

import { CollectorService } from '@birdy/protos'

export const collectorService = createPromiseClient(
  CollectorService,
  createConnectTransport({
    httpVersion: '1.1',
    baseUrl: process.env.COLLECTOR_SERVICE_ENDPOINT,
  }),
)
