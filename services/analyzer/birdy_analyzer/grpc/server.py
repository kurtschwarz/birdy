import asyncio
import grpc
from loguru import logger

import birdy_protos.analyzer.v1.service_pb2 as analyzer_pb2
import birdy_protos.analyzer.v1.service_pb2_grpc as analyzer_pb2_grpc

from birdy_analyzer.analyzer import Analyzer
from birdy_analyzer.config import Config
from birdy_analyzer.grpc.service import Service


class Server:
    _config: Config
    _analyzer: Analyzer
    _server: grpc.aio.Server

    def __init__(self, config: Config, analyzer: Analyzer) -> None:
        self._config = config
        self._analyzer = analyzer

    async def setup(self) -> None:
        self._server = grpc.aio.server()
        self._server.add_insecure_port(
            "[::]:{port}".format(port=self._config.grpc_port)
        )

        analyzer_pb2_grpc.add_AnalyzerServiceServicer_to_server(
            Service(analyzer=self._analyzer), self._server
        )

        logger.info(
            f"starting grpc server on [::]:{self._config.grpc_port}",
            port=self._config.grpc_port,
        )

        await self._server.start()

    async def run(self) -> None:
        logger.info(
            f"grpc server running on [::]:{self._config.grpc_port}",
            port=self._config.grpc_port,
        )

        try:
            await self._server.wait_for_termination()
        except asyncio.exceptions.CancelledError:
            await self._server.stop(5)
