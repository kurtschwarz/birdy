from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase

import birdy_protos.analyzer.v1.service_pb2 as analyzer_pb2


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True, init=True)
class Detection:
    common_name: str
    scientific_name: str
    confidence: float

    def to_proto(self) -> analyzer_pb2.Detection:
        return analyzer_pb2.Detection(
            common_name=self.common_name,
            scientific_name=self.scientific_name,
            confidence=self.confidence,
        )

    @staticmethod
    def from_proto(proto: analyzer_pb2.Detection) -> "Detection":
        return Detection(
            common_name=proto.common_name,
            scientific_name=proto.scientific_name,
            confidence=proto.confidence,
        )
