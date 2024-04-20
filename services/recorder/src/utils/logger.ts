import pino from 'pino'
import pretty from 'pino-pretty'

import { config } from '../config'

export const logger = (() => {
  let stream
  if (process.env.NODE_ENV === 'development') {
    stream = pretty({ colorize: true })
  }

  return pino(
    {
      level: config.logLevel,
    },
    stream,
  )
})()
