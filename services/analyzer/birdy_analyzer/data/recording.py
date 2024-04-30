from dataclasses import dataclass
import datetime

import birdy_protos.analyzer.v1.service_pb2 as analyzer_pb2


@dataclass
class Recording:
    id: str
    duration: float
    start_time: datetime.datetime
    end_time: datetime.datetime
    storage_uri: str

    @staticmethod
    def from_proto(proto: analyzer_pb2.Recording) -> "Recording":
        return Recording(
            id=proto.id,
            duration=proto.duration,
            storage_uri=proto.storage_uri,
            start_time=datetime.datetime.fromtimestamp(
                proto.start_time.seconds, tz=datetime.UTC
            ),
            end_time=datetime.datetime.fromtimestamp(
                proto.end_time.seconds, tz=datetime.UTC
            ),
        )
