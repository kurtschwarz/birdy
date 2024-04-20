import { MqttClient } from '@birdy/mqtt'

import { config } from '../../config.js'

const client = new MqttClient({
  broker: config.mqttBroker,
  enabled: config.mqttEnabled,
  topicEncoder: (topic: string): string => topic.replace(':recorderId', config.id)
})

export const publish = client.publish.bind(client)
export { Topic } from '@birdy/mqtt'
