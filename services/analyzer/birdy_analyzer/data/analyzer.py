from dataclasses import dataclass

import birdy_protos.analyzer.v1.service_pb2 as analyzer_pb2

from birdy_analyzer.data.recording import Recording
from birdy_analyzer.data.detection import Detection


@dataclass
class AnalyzeResult:
    recording: Recording
    detections: list[Detection]
