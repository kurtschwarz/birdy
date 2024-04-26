import asyncio
import confluent_kafka
from loguru import logger

from birdy_analyzer.config import Config
from birdy_analyzer.analyzer import Analyzer


class Consumer:
    _config: Config
    _analyzer: Analyzer
    _topics: list[str]
    _consumer: confluent_kafka.Consumer

    def __init__(self, config: Config, analyzer: Analyzer) -> None:
        self._config = config
        self._analyzer = analyzer

    async def setup(self, topics: list[str], tasks: set[asyncio.Task]) -> None:
        self._topics = topics

        logger.info(
            f"starting kafka consumer for topics: {', '.join(topics)}",
            topics=topics,
        )

        self._consumer = confluent_kafka.Consumer(
            {
                "group.id": "@birdy/analyzer",
                "bootstrap.servers": ",".join(self._config.kafka_brokers),
                "auto.offset.reset": "earliest",
                "enable.auto.offset.store": False,
            },
        )

        self._consumer.subscribe(topics)

        loop = asyncio.get_running_loop()
        task = loop.create_task(self.consume())
        tasks.add(task)
        task.add_done_callback(tasks.remove)

    async def consume(self) -> None:
        logger.info(
            f"kafka consumer subscribed to topics: {', '.join(self._topics)}",
            topics=self._topics,
        )

        loop = asyncio.get_running_loop()

        try:
            while True:
                message = await loop.run_in_executor(None, self._consumer.poll, 0.1)
                if message is None:
                    continue
                if message.error():
                    continue
                self._consumer.store_offsets(message=message)
        finally:
            self._consumer.close()
