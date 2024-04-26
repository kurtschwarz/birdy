import grpc
from loguru import logger

from birdy_analyzer.data.recording import Recording
from birdy_analyzer.analyzer import Analyzer

import birdy_protos.analyzer.v1.service_pb2 as analyzer_pb2
import birdy_protos.analyzer.v1.service_pb2_grpc as analyzer_pb2_grpc


class Service(analyzer_pb2_grpc.AnalyzerServiceServicer):
    analyzer: Analyzer

    def __init__(self, analyzer: Analyzer) -> None:
        super().__init__()
        self.analyzer = analyzer

    async def Analyze(
        self,
        request: analyzer_pb2.AnalyzeRequest,
        context: grpc.aio.ServicerContext,
    ) -> analyzer_pb2.AnalyzeResponse:
        response = analyzer_pb2.AnalyzeResponse(status=analyzer_pb2.Status(code=0))

        try:
            detections = self.analyzer.analyzeRecording(
                Recording.from_proto(request.recording)
            )

            for detection in detections:
                response.detections.append(detection.to_proto())
        except Exception as e:
            logger.exception(e)
            response.status = analyzer_pb2.Status(code=1)

        return response
