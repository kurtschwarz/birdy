from dataclasses import dataclass

import birdy_protos.analyzer.v1.service_pb2 as analyzer_pb2


@dataclass
class Recording:
    id: str

    @staticmethod
    def from_proto(proto: analyzer_pb2.Recording) -> "Recording":
        return Recording(id=proto.id)
