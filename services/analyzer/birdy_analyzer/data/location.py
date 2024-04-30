from dataclasses import dataclass

import birdy_protos.analyzer.v1.service_pb2 as analyzer_pb2


@dataclass
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
