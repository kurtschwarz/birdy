import asyncio
import confluent_kafka
from loguru import logger

from birdy_analyzer.config import Config


class Producer:
    _config: Config
    _loop: asyncio.AbstractEventLoop
    _producer: confluent_kafka.Producer

    def __init__(self, config: Config) -> None:
        self._config = config

    async def setup(
        self, tasks: set[asyncio.Task], loop: asyncio.AbstractEventLoop | None = None
    ) -> None:
        self._loop = loop or asyncio.get_event_loop()
        self._producer = confluent_kafka.Producer(
            {
                "bootstrap.servers": ",".join(self._config.kafka_brokers),
            },
        )

        task = self._loop.create_task(self.poll())
        tasks.add(task)
        task.add_done_callback(tasks.remove)

    def publish(self, topic: str, key: str, message: any) -> asyncio.Future[any]:
        result = self._loop.create_future()

        def ack(err, msg):
            if err:
                self._loop.call_soon_threadsafe(
                    result.set_exception, confluent_kafka.KafkaException(err)
                )
            else:
                self._loop.call_soon_threadsafe(result.set_result, msg)

        self._producer.produce(topic, message, key, on_delivery=ack)

        return result

    async def poll(self) -> None:
        try:
            while True:
                await self._loop.run_in_executor(None, self._producer.poll, 0.1)
        finally:
            self._producer.close()
