import mqtt from 'mqtt'

import { Topics, TopicDefinitions } from './topics.js'

export class MqttClient <PublishableTopics extends Topics> {
  protected enabled: boolean
  protected client: mqtt.MqttClient
  protected topicEncoder?: (topic: string) => string

  constructor (
    options: {
      broker: string
      enabled: boolean
      topicEncoder?: (topic: string) => string
    }
  ) {
    this.enabled = options.enabled
    this.topicEncoder = options.topicEncoder
    this.client = mqtt.connect(options.broker, {
      manualConnect: true
    })
  }

  private encodeTopic = (topic: string): string => {
    return this.topicEncoder?.(topic) || topic
  }

  private encodeMessage = (message: Record<string, any>): Buffer => {
    return Buffer.from(JSON.stringify(message), 'utf-8')
  }

  public async publish <T extends PublishableTopics>(
    topic: T,
    message: TopicDefinitions[T]
  ): Promise<void> {
    if (!this.enabled) {
      return
    }

    if (!this.client.connected) {
      await this.client.connect()
    }

    await this.client.publishAsync(
      this.encodeTopic(topic),
      this.encodeMessage(message)
    )
  }
}

export * from './topics.js'
