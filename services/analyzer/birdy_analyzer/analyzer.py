from minio import Minio
from loguru import logger

from birdy_analyzer.data.recording import Recording
from birdy_analyzer.data.detection import Detection
from birdy_analyzer.config import Config


class Analyzer:
    config: Config
    storage: Minio

    def __init__(self, config: Config) -> None:
        self.config = config
        self.storage = None

    def analyzeRecording(self, recording: Recording) -> list[Detection]:
        return []
