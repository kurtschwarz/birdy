import asyncio
import grpc
from types import TracebackType
from typing import Self
from loguru import logger
from grpc_health.v1 import health
from grpc_health.v1 import health_pb2_grpc

from birdy_analyzer.config import Config

import birdy_protos.analyzer.v1.service_pb2 as analyzer_pb2
import birdy_protos.analyzer.v1.service_pb2_grpc as analyzer_pb2_grpc


class GrpcService:
    _config: Config
    _server: grpc.aio.Server

    def __init__(self, config: Config) -> None:
        self._config = config

    async def __aenter__(self) -> Self:
        if not self._config.grpc_enabled:
            return self

        self._server = grpc.aio.server()
        self._server.add_insecure_port(
            "[::]:{port}".format(port=self._config.grpc_port)
        )

        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        if not self._config.grpc_enabled:
            return self

        return None

    async def listen(self, servicer: any) -> None:
        if not self._config.grpc_enabled:
            while True:
                asyncio.Sleep(1)

        logger.info(
            f"starting grpc server on [::]:{self._config.grpc_port}",
            port=self._config.grpc_port,
        )

        analyzer_pb2_grpc.add_AnalyzerServiceServicer_to_server(servicer, self._server)
        health_pb2_grpc.add_HealthServicer_to_server(
            health.HealthServicer(), self._server
        )

        await self._server.start()

        logger.info(
            f"grpc server running on [::]:{self._config.grpc_port}",
            port=self._config.grpc_port,
        )

        try:
            await self._server.wait_for_termination()
        except asyncio.exceptions.CancelledError:
            await self._server.stop(5)
