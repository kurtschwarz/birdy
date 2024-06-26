import mqtt from 'mqtt'

import { Topics, TopicDefinitions } from './topics.js'

export class MqttClient<PublishableTopics extends Topics> {
  protected enabled: boolean
  protected client: mqtt.MqttClient
  protected topicEncoder?: (topic: string) => string

  constructor(options: {
    broker: string
    enabled: boolean
    topicEncoder?: (topic: string) => string
  }) {
    this.enabled = options.enabled
    this.topicEncoder = options.topicEncoder
    this.client = mqtt.connect(options.broker, {
      manualConnect: true,
    })
  }

  private encodeTopic = (topic: string, message: Record<string, any>): string => {
    topic = this.topicEncoder?.(topic) || topic

    for (const [key, value] of Object.entries(message)) {
      const isValueString = toString.call(value) == '[object String]'
      const isValueNumeric = !isNaN(parseFloat(value)) && !isNaN(value - 0)
      if (isValueString || isValueNumeric) {
        topic = topic.replace(new RegExp(`:${key}`, 'g'), `${value}`)
      }
    }

    return topic
  }

  private encodeMessage = (message: Record<string, any>): Buffer => {
    return Buffer.from(JSON.stringify(message), 'utf-8')
  }

  public async publish<T extends PublishableTopics>(
    topic: T,
    message: TopicDefinitions[T],
  ): Promise<void> {
    if (!this.enabled) {
      return
    }

    if (!this.client.connected) {
      await this.client.connect()
    }

    await this.client.publishAsync(this.encodeTopic(topic, message), this.encodeMessage(message))
  }
}

export * from './topics.js'
