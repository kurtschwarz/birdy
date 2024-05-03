import grpc
from loguru import logger

import birdy_protos.analyzer.v1.service_pb2 as analyzer_pb2
import birdy_protos.analyzer.v1.service_pb2_grpc as analyzer_pb2_grpc

from birdy_analyzer.analyzer import Analyzer
from birdy_analyzer.data.recording import Recording
from birdy_analyzer.data.location import Location


class GrpcServicer(analyzer_pb2_grpc.AnalyzerServiceServicer):
    _analyzer: Analyzer

    def __init__(self, analyzer: Analyzer) -> None:
        super().__init__()
        self._analyzer = analyzer

    async def Analyze(
        self,
        request: analyzer_pb2.AnalyzeRequest,
        context: grpc.aio.ServicerContext,
    ) -> analyzer_pb2.AnalyzeResponse:
        response = analyzer_pb2.AnalyzeResponse(status=analyzer_pb2.Status(code=0))

        try:
            result = await self._analyzer.analyze(
                recording=Recording.from_proto(request.recording),
                location=Location.from_proto(request.location),
            )

            for detection in result.detections:
                response.detections.append(detection.to_proto())
        except Exception as e:
            logger.exception(e)
            response.status = analyzer_pb2.Status(code=1)

        return response
