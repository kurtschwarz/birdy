import asyncio
import confluent_kafka
from loguru import logger

from birdy_analyzer.config import Config
from birdy_analyzer.analyzer import Analyzer


class QueuingRecordingsUnanalyzedConsumer:
    _analyzer_service: Analyzer

    def __init__(self, analyzer_service: Analyzer) -> None:
        self._analyzer_service = analyzer_service

    async def consume(self, message: confluent_kafka.Message) -> None:
        logger.info("QueuingRecordingsUnanalyzedConsumer.consume", message=message)
        return
