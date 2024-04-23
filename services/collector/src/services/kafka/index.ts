import kafka from 'kafkajs'

import { config } from '../../config.js'

const client = new kafka.Kafka({
  clientId: '@birdy/collector',
  brokers: config.kafkaBrokers,
})

const producer = client.producer({
  retry: {
    retries: 10,
  },
})

let producerConnected = false

const getProducer = async (): Promise<kafka.Producer> => {
  if (producerConnected) {
    return producer
  }

  while (true) {
    try {
      await producer.connect()
      break
    } catch (error) {
      producerConnected = false
      if (
        error instanceof kafka.KafkaJSNonRetriableError &&
        error.name === 'KafkaJSNumberOfRetriesExceeded'
      ) {
        continue
      }

      throw error
    }
  }

  producerConnected = true
  return producer
}

export const publish = async (topic: string, messages: kafka.Message[]): Promise<void> => {
  if (!config.kafkaEnabled) {
    return
  }

  await (
    await getProducer()
  ).send({
    topic,
    messages,
  })
}
