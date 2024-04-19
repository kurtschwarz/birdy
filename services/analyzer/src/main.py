import io
import os
import sys
import asyncio
import grpc
import aiomqtt
import json
import logging

from minio import Minio
from birdnetlib import RecordingFileObject
from birdnetlib.analyzer import Analyzer
from datetime import datetime

sys.path.insert(0, "../../../packages/protos/gen/py")

from analyzer.v1 import service_pb2 as analyzer_pb2
from analyzer.v1 import service_pb2_grpc as analyzer_pb2_grpc

storage = Minio(
    "%s:%s" % (os.environ["MINIO_ENDPOINT"], os.environ["MINIO_PORT"]),
    access_key=os.environ["MINIO_ROOT_USER"],
    secret_key=os.environ["MINIO_ROOT_PASSWORD"],
    secure=False,
)

analyzer = Analyzer()


class Analyzer(analyzer_pb2_grpc.AnalyzerServiceServicer):
    async def Analyze(
        self,
        request: analyzer_pb2.AnalyzeRequest,
        context: grpc.aio.ServicerContext,
    ) -> analyzer_pb2.AnalyzeResponse:
        response = analyzer_pb2.AnalyzeResponse(status=analyzer_pb2.Status(code=0))

        try:
            file = storage.get_object(
                "birdy-recordings-unprocessed", request.recording.id
            )

            with io.BytesIO(file.read()) as fileObj:
                recording = RecordingFileObject(
                    analyzer,
                    fileObj,
                    lat=request.location.latitude,
                    lon=request.location.longitude,
                    date=datetime(year=2023, month=6, day=27),
                    min_conf=0.25,
                )

                recording.analyze()

                for detection in recording.detections:
                    response.detections.append(
                        analyzer_pb2.Detection(
                            start_time=detection["start_time"],
                            end_time=detection["end_time"],
                            confidence=detection["confidence"],
                            common_name=detection["common_name"],
                            scientific_name=detection["scientific_name"],
                            label=detection["label"],
                        )
                    )
        except:
            response.status = analyzer_pb2.Status(code=1)
        finally:
            file.close()
            file.release_conn()

        return response


async def listen() -> None:
    async with aiomqtt.Client(
        identifier="analyzer",
        hostname="mqtt.service.docker",
        port=1883,
        protocol=aiomqtt.ProtocolVersion.V5,
        clean_start=2,
    ) as client:
        await client.subscribe("birdy/#")
        async for message in client.messages:
            data = json.loads(message.payload)
            logging.info(message.payload)
            if data["EventName"] == "s3:ObjectCreated:Put":
                logging.info(data["Records"])


background_tasks = set()
cleanup_tasks = []


async def main():
    logging.info("starting")

    loop = asyncio.get_event_loop()
    task = loop.create_task(listen())
    background_tasks.add(task)
    task.add_done_callback(background_tasks.remove)

    server = grpc.aio.server()
    server.add_insecure_port("[::]:50051")
    analyzer_pb2_grpc.add_AnalyzerServiceServicer_to_server(Analyzer(), server)

    await server.start()

    async def server_graceful_shutdown():
        logging.info("Starting graceful shutdown...")
        await server.stop(5)

    cleanup_tasks.append(server_graceful_shutdown())

    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.run_until_complete(*cleanup_tasks)
        loop.close()
