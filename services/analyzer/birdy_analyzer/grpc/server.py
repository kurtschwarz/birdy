import grpc
from loguru import logger

import birdy_protos.analyzer.v1.service_pb2 as analyzer_pb2
import birdy_protos.analyzer.v1.service_pb2_grpc as analyzer_pb2_grpc

from birdy_analyzer.config import Config
from birdy_analyzer.grpc.service import Service


class Server:
    config: Config
    server: grpc.aio.Server

    def __init__(self, config: Config) -> None:
        self.config = config

    async def setup(self) -> None:
        self.server = grpc.aio.server()
        self.server.add_insecure_port("[::]:{port}".format(port=self.config.grpc_port))

        analyzer_pb2_grpc.add_AnalyzerServiceServicer_to_server(Service(), self.server)

        logger.info(
            f"starting grpc server on [::]:{self.config.grpc_port}",
            port=self.config.grpc_port,
        )

        await self.server.start()

    async def run(self) -> None:
        logger.info(
            f"grpc server running on [::]:{self.config.grpc_port}",
            port=self.config.grpc_port,
        )

        await self.server.wait_for_termination()
