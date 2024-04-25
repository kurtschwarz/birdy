from dataclasses import dataclass

import birdy_protos.analyzer.v1.service_pb2 as analyzer_pb2


@dataclass
class Detection:
    confidence: float

    def to_proto(self) -> analyzer_pb2.Detection:
        return analyzer_pb2.Detection(confidence=self.confidence)

    @staticmethod
    def from_proto(proto: analyzer_pb2.Detection) -> "Detection":
        return Detection(confidence=proto.confidence)
