from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase

from birdy_analyzer.data.recording import Recording
from birdy_analyzer.data.detection import Detection
from birdy_analyzer.data.location import Location


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True, init=True)
class AnalyzeRequest:
    recording: Recording
    location: Location


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True, init=True)
class AnalyzeResult:
    recording: Recording
    detections: list[Detection]
