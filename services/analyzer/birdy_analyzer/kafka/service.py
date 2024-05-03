import asyncio
import confluent_kafka
from types import TracebackType
from typing import Self

from birdy_analyzer.config import Config


class KafkaService:
    _config: Config

    _consumer: confluent_kafka.Consumer
    _producer: confluent_kafka.Producer

    _subscriptions: dict[str, any]

    _loop: asyncio.AbstractEventLoop
    _poll_task: asyncio.Task

    def __init__(self, config: Config) -> None:
        self._config = config

        self._producer = confluent_kafka.Producer(
            {
                "bootstrap.servers": ",".join(self._config.kafka_brokers),
            },
        )

        self._consumer = confluent_kafka.Consumer(
            {
                "group.id": "@birdy/analyzer",
                "bootstrap.servers": ",".join(self._config.kafka_brokers),
                "auto.offset.reset": "earliest",
                "enable.auto.offset.store": False,
            },
        )

        self._subscriptions = dict()

    async def __aenter__(self) -> Self:
        if not self._config.kafka_enabled:
            return self

        self._loop = asyncio.get_running_loop()
        self._poll_task = self._loop.create_task(self._poll())

        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        if not self._config.kafka_enabled:
            return self

        self._poll_task.cancel()

        return None

    async def publish(self, topic: str, key: str, message: any) -> any:
        if not self._config.kafka_enabled:
            return

        self._producer.produce(topic, message, key)

    async def subscribe(self, topics: list[str], consumer: any) -> None:
        self._consumer.subscribe(topics)

        for topic in topics:
            self._subscriptions[topic] = consumer

    async def _poll(self) -> None:
        try:
            while True:
                await self._loop.run_in_executor(None, self._producer.poll, 0.1)

                message = await self._loop.run_in_executor(
                    None, self._consumer.poll, 0.1
                )

                if message is None or message.error():
                    continue

                if message.topic() in self._subscriptions:
                    await self._subscriptions[message.topic()].consume(message=message)

                self._consumer.store_offsets(message=message)
        finally:
            self._producer.close()
