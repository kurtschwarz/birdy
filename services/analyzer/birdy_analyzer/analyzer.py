from minio import Minio
from loguru import logger
from urllib.parse import urlparse

from birdy_analyzer.data.recording import Recording
from birdy_analyzer.data.detection import Detection
from birdy_analyzer.config import Config


class Analyzer:
    config: Config
    storage: Minio | None

    def __init__(self, config: Config) -> None:
        self.config = config
        self.storage = lambda storage_uri: Minio(
            endpoint=storage_uri.netloc,
            access_key=self.config.storage_s3_access_key,
            secret_key=self.config.storage_s3_secret_key,
            secure=storage_uri.scheme == "https",
        )(urlparse(self.config.storage_s3_endpoint))

    def analyzeRecording(self, recording: Recording) -> list[Detection]:
        return []
