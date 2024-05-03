from dataclasses import dataclass, field, fields
from dataclasses_json import dataclass_json, config, LetterCase
from datetime import datetime, UTC

import birdy_protos.analyzer.v1.service_pb2 as analyzer_pb2


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True, init=True)
class Recording:
    id: str
    duration: float
    start_time: datetime = field(
        metadata=config(encoder=datetime.isoformat, decoder=datetime.fromisoformat)
    )
    end_time: datetime = field(
        metadata=config(encoder=datetime.isoformat, decoder=datetime.fromisoformat)
    )
    storage_uri: str

    @staticmethod
    def from_proto(proto: analyzer_pb2.Recording) -> "Recording":
        return Recording(
            id=proto.id,
            duration=proto.duration,
            storage_uri=proto.storage_uri,
            start_time=datetime.fromtimestamp(proto.start_time.seconds, tz=UTC),
            end_time=datetime.fromtimestamp(proto.end_time.seconds, tz=UTC),
        )
