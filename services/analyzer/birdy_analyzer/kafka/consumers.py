import asyncio
import json
import confluent_kafka
from loguru import logger

from birdy_analyzer.config import Config
from birdy_analyzer.analyzer import Analyzer
from birdy_analyzer.data.analyzer import AnalyzeRequest


class QueuingRecordingsUnanalyzedConsumer:
    _analyzer: Analyzer

    def __init__(self, analyzer: Analyzer) -> None:
        self._analyzer = analyzer

    async def consume(self, message: confluent_kafka.Message) -> None:
        request = AnalyzeRequest.from_json(message.value().decode("utf-8"))
        await self._analyzer.analyze(request)
