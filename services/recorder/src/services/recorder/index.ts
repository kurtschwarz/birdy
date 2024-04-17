import { client } from '../../initializers/prisma.js'
import { config, logger } from '../../utils/index.js'

export const register = async (): Promise<void> => {
  await client.$transaction([
    client.location.upsert({
      where: { id: config.locationId },
      create: { id: config.locationId, latitude: config.locationLat, longitude: config.locationLong },
      update: {},
    }),
    client.recorder.upsert({
      where: { id: config.id },
      create: { id: config.id, locationId: config.locationId },
      update: {},
    })
  ])
}
