import grpc

from birdnetlib import RecordingFileObject
from birdnetlib.analyzer import Analyzer
from datetime import datetime

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


# class AnalyzerService(analyzer_pb2_grpc.AnalyzerServiceServicer):
#     async def Analyze(
#         self,
#         request: analyzer_pb2.AnalyzeRequest,
#         context: grpc.aio.ServicerContext,
#     ) -> analyzer_pb2.AnalyzeResponse:
#         response = analyzer_pb2.AnalyzeResponse(status=analyzer_pb2.Status(code=0))

#         try:
#             file = storage.get_object(
#                 "birdy-recordings-unprocessed", request.recording.id
#             )

#             with io.BytesIO(file.read()) as file_obj:
#                 recording = RecordingFileObject(
#                     analyzer,
#                     file_obj,
#                     lat=request.location.latitude,
#                     lon=request.location.longitude,
#                     date=datetime(year=2023, month=6, day=27),
#                     min_conf=0.25,
#                 )

#                 recording.analyze()

#                 for detection in recording.detections:
#                     response.detections.append(
#                         analyzer_pb2.Detection(
#                             start_time=detection["start_time"],
#                             end_time=detection["end_time"],
#                             confidence=detection["confidence"],
#                             common_name=detection["common_name"],
#                             scientific_name=detection["scientific_name"],
#                             label=detection["label"],
#                         )
#                     )
#         except:
#             response.status = analyzer_pb2.Status(code=1)
#         finally:
#             file.close()
#             file.release_conn()

#         return response
