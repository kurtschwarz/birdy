import asyncio
import grpc
from types import TracebackType
from typing import Self
from loguru import logger

from birdy_analyzer.config import Config

import birdy_protos.analyzer.v1.service_pb2 as analyzer_pb2
import birdy_protos.analyzer.v1.service_pb2_grpc as analyzer_pb2_grpc


# class Service(analyzer_pb2_grpc.AnalyzerServiceServicer):
#     _analyzer: Analyzer

#     def __init__(self, analyzer: Analyzer) -> None:
#         super().__init__()
#         self._analyzer = analyzer

#     async def Analyze(
#         self,
#         request: analyzer_pb2.AnalyzeRequest,
#         context: grpc.aio.ServicerContext,
#     ) -> analyzer_pb2.AnalyzeResponse:
#         response = analyzer_pb2.AnalyzeResponse(status=analyzer_pb2.Status(code=0))

#         try:
#             result = await self._analyzer.analyzeRecording(
#                 Recording.from_proto(request.recording)
#             )

#             for detection in result.detections:
#                 response.detections.append(detection.to_proto())
#         except Exception as e:
#             logger.exception(e)
#             response.status = analyzer_pb2.Status(code=1)

#         return response


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

        await self._server.start()

        logger.info(
            f"grpc server running on [::]:{self._config.grpc_port}",
            port=self._config.grpc_port,
        )

        try:
            await self._server.wait_for_termination()
        except asyncio.exceptions.CancelledError:
            await self._server.stop(5)
