from datetime import datetime
import io
from minio import Minio
from loguru import logger
from urllib.parse import urlparse

from birdnetlib import RecordingFileObject
from birdnetlib.analyzer import Analyzer as BirdnetAnalyzer

from birdy_analyzer.data.recording import Recording
from birdy_analyzer.data.detection import Detection
from birdy_analyzer.config import Config


class Analyzer:
    config: Config
    birdnet: BirdnetAnalyzer
    storage: Minio | None

    def __init__(self, config: Config) -> None:
        self.config = config
        self.birdnet = BirdnetAnalyzer()
        self.storage = (
            lambda storage_uri: Minio(
                endpoint=storage_uri.netloc,
                access_key=self.config.storage_s3_access_key,
                secret_key=self.config.storage_s3_secret_key,
                secure=storage_uri.scheme == "https",
            )
        )(urlparse(self.config.storage_s3_endpoint))

    def analyzeRecording(self, recording: Recording) -> list[Detection]:
        detections = []
        recording_file = None

        try:
            recording_file = self.storage.get_object(
                bucket_name=self.config.storage_s3_bucket_unanalyzed,
                object_name=recording.id,
            )

            with io.BytesIO(recording_file.read()) as recording_bytes:
                birdnet_recording = RecordingFileObject(
                    self.birdnet,
                    recording_bytes,
                    lat=35.4244,
                    lon=-120.7463,
                    date=datetime(year=2023, month=6, day=27),
                    min_conf=0.25,
                )

                birdnet_recording.analyze()

                for detection in birdnet_recording.detections:
                    detections.append(
                        Detection(
                            common_name=detection["common_name"],
                            scientific_name=detection["scientific_name"],
                            confidence=detection["confidence"],
                        )
                    )
        except Exception as e:
            logger.exception(e)
        finally:
            recording_file.close()
            recording_file.release_conn()

        return detections
