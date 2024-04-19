import io
import os
import sys
import asyncio
import grpc
import logging
import click

from minio import Minio

from service import AnalyzerService
from subscriber import subscribe

sys.path.insert(0, "../../../packages/protos/gen/py")

from analyzer.v1 import service_pb2 as analyzer_pb2
from analyzer.v1 import service_pb2_grpc as analyzer_pb2_grpc


logging.basicConfig(level=logging.INFO)

storage = Minio(
    "%s:%s" % (os.environ["MINIO_ENDPOINT"], os.environ["MINIO_PORT"]),
    access_key=os.environ["MINIO_ROOT_USER"],
    secret_key=os.environ["MINIO_ROOT_PASSWORD"],
    secure=False,
)

background_tasks = set()
cleanup_tasks = []


async def start():
    logging.info("starting")

    loop = asyncio.get_event_loop()
    task = loop.create_task(subscribe())
    background_tasks.add(task)
    task.add_done_callback(background_tasks.remove)

    server = grpc.aio.server()
    server.add_insecure_port("[::]:50051")
    analyzer_pb2_grpc.add_AnalyzerServiceServicer_to_server(AnalyzerService(), server)

    await server.start()

    async def server_graceful_shutdown():
        logging.info("Starting graceful shutdown...")
        await server.stop(5)

    cleanup_tasks.append(server_graceful_shutdown())

    await server.wait_for_termination()


def configure(ctx, param, file_path):
    pass


def configureLogger(ctx, param, level):
    levels = logging.getLevelNamesMapping()
    if level.upper() in levels:
        logging.getLogger().setLevel(levels[level.upper()])


@click.group(invoke_without_command=True)
@click.option(
    "-c",
    "--config",
    type=click.Path(dir_okay=False),
    callback=configure,
    is_eager=True,
    expose_value=False,
    show_default=False,
)
@click.option(
    "--log-level",
    type=click.Choice(
        choices=list(
            map(lambda key: key.lower(), logging.getLevelNamesMapping().keys())
        )
    ),
    default="info",
    callback=configureLogger,
    is_eager=True,
    expose_value=False,
    show_default=False,
)
def main(**kwargs):
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(start())
    finally:
        loop.run_until_complete(*cleanup_tasks)
        loop.close()


if __name__ == "__main__":
    main()
