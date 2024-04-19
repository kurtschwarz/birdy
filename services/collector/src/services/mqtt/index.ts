import mqtt from 'mqtt'

import { config } from '../../config.js'

const client = mqtt.connect(config.mqttBroker, {
  manualConnect: true
})

export enum Topic {
  SERVICE_ONLINE = 'birdy/collector/status/online',
  SERVICE_OFFLINE = 'birdy/collector/status/offline',
}

type TopicDefinitions = {
  [Topic.SERVICE_ONLINE]: { now: Date },
  [Topic.SERVICE_OFFLINE]: { now: Date }
}

export type Topics = keyof TopicDefinitions

export const publish = async <T extends Topics>(
  topic: T,
  message: TopicDefinitions[T]
): Promise<void> => {
  if (!config.mqttEnabled) {
    return
  }

  if (!client.connected) {
    await client.connect()
  }

  await client.publish(
    topic,
    JSON.stringify(message)
  )
}
