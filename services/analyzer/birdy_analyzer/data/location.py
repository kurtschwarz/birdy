from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase

import birdy_protos.analyzer.v1.service_pb2 as analyzer_pb2


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True, init=True)
class Location:
    id: str
    latitude: float
    longitude: float

    @staticmethod
    def from_proto(proto: analyzer_pb2.Location) -> "Location":
        return Location(
            id=proto.id,
            latitude=proto.latitude,
            longitude=proto.longitude,
        )
