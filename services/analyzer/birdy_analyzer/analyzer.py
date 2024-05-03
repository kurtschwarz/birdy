from datetime import datetime
import io
from minio import Minio
from loguru import logger
from urllib.parse import urlparse

from birdnetlib import RecordingFileObject
from birdnetlib.analyzer import Analyzer as BirdnetAnalyzer

from birdy_analyzer.config import Config
from birdy_analyzer.data.recording import Recording
from birdy_analyzer.data.location import Location
from birdy_analyzer.data.detection import Detection
from birdy_analyzer.data.analyzer import AnalyzeRequest, AnalyzeResult
from birdy_analyzer.kafka.service import KafkaService
from birdy_analyzer.mqtt.service import MqttService


class Analyzer:
    _config: Config
    _birdnet: BirdnetAnalyzer
    _storage: Minio | None
    _mqtt: MqttService | None
    _kafka: KafkaService | None

    def __init__(
        self,
        config: Config,
        mqtt: MqttService | None = None,
        kafka: KafkaService | None = None,
    ) -> None:
        self._config = config
        self._birdnet = BirdnetAnalyzer()
        self._mqtt = mqtt
        self._kafka = kafka
        self._storage = (
            lambda storage_uri: Minio(
                endpoint=storage_uri.netloc,
                access_key=self._config.storage_s3_access_key,
                secret_key=self._config.storage_s3_secret_key,
                secure=storage_uri.scheme == "https",
            )
        )(urlparse(self._config.storage_s3_endpoint))

    async def analyze(
        self, request: AnalyzeRequest, collect: bool = True
    ) -> AnalyzeResult:
        result = AnalyzeResult(recording=request.recording, detections=[])
        recording_file_handle = None

        try:
            parsed_storage_uri = urlparse(
                request.recording.storage_uri, allow_fragments=False
            )

            recording_file_handle = self._storage.get_object(
                bucket_name=parsed_storage_uri.netloc,
                object_name=parsed_storage_uri.path,
            )

            with io.BytesIO(recording_file_handle.read()) as recording_file_bytes:
                birdnet_recording = RecordingFileObject(
                    self._birdnet,
                    file_obj=recording_file_bytes,
                    lat=request.location.latitude,
                    lon=request.location.longitude,
                    date=request.recording.start_time.date(),
                    min_conf=0.25,
                )

                birdnet_recording.analyze()

                for detection in birdnet_recording.detections:
                    result.detections.append(
                        Detection(
                            common_name=detection["common_name"],
                            scientific_name=detection["scientific_name"],
                            confidence=detection["confidence"],
                        )
                    )

                if collect:
                    await self._kafka.publish(
                        topic="queuing.recordings.analyzed",
                        key=request.recording.id,
                        message=result.to_json(),
                    )
        except Exception as e:
            logger.exception(e)
        finally:
            recording_file_handle.close()
            recording_file_handle.release_conn()

        return result
