import sys
import asyncio
import grpc

sys.path.insert(0, '../../packages/protos/gen/py')

from analyzer.v1 import service_pb2 as analyzer_pb2
from analyzer.v1 import service_pb2_grpc as analyzer_pb2_grpc

class Analyzer(analyzer_pb2_grpc.AnalyzerServiceServicer):
    async def Analyze(
        self,
        request: analyzer_pb2.AnalyzeRequest,
        context: grpc.aio.ServicerContext,
    ) -> analyzer_pb2.AnalyzeResponse:
        return analyzer_pb2.AnalyzeResponse(status=analyzer_pb2.Status(code=0))

async def serve() -> None:
    server = grpc.aio.server()
    analyzer_pb2_grpc.add_AnalyzerServiceServicer_to_server(Analyzer(), server)
    listen_addr = "[::]:50051"
    server.add_insecure_port(listen_addr)
    await server.start()
    await server.wait_for_termination()

if __name__ == "__main__":
    asyncio.run(serve())
