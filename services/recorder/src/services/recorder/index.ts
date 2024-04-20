import { backOff } from 'exponential-backoff'
import { config } from '../../utils/index.js'
import { collectorService } from '../collector/index.js'

export const register = async (): Promise<void> => {
  await backOff(
    async () => {
      const response = await collectorService.register({
        recorder: {
          id: config.id,
        },
        location: {
          id: config.locationId,
          latitude: config.locationLat,
          longitude: config.locationLong,
        },
      })

      if (response?.status?.code !== 0) {
        throw new Error(`Unable to register recorder`)
      }
    },
    {
      maxDelay: 5000,
      numOfAttempts: 10,
    },
  )
}
