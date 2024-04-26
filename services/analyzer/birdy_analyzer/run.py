import sys
import signal
import asyncio
import click

from loguru import logger

from birdy_analyzer.analyzer import Analyzer
from birdy_analyzer.config import Config
from birdy_analyzer.kafka.consumer import Consumer
from birdy_analyzer.grpc.server import Server

tasks = set()


def setup_logger(level: str) -> None:
    logger.configure(
        handlers=[
            {
                "sink": sys.stdout,
                "level": level,
                "format": ("<green>{time}</green> <level>{message}</level> {extra}"),
                "colorize": True,
            }
        ]
    )


def setup_signal_handlers() -> None:
    loop = asyncio.get_running_loop()

    for sig in (signal.SIGHUP, signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, shutdown, sig)


def shutdown(sig: signal.Signals) -> None:
    logger.info(f"Received exit signal {sig.name}")

    for task in tasks:
        task.cancel()

    logger.info(f"Cancelled {len(tasks)} task(s)")
    logger.info(f"Exiting")


@click.command()
@click.option("--verbose", is_flag=True)
@click.option("--storage", default="s3")
@click.option("--storage-s3-endpoint")
@click.option("--storage-s3-access-key", envvar="STORAGE_S3_ACCESS_KEY")
@click.option("--storage-s3-secret-key", envvar="STORAGE_S3_SECRET_KEY")
@click.option("--storage-s3-bucket-unanalyzed")
@click.option("--storage-s3-bucket-analyzed")
@click.option("--kafka-enabled", is_flag=True)
@click.option("--kafka-brokers", multiple=True, default=[])
@click.option("--grpc-enabled", is_flag=True)
@click.option("--grpc-port", default=50051)
def main(**kwargs) -> None:
    setup_logger(level=(lambda: "DEBUG" if kwargs["verbose"] else "INFO")())

    logger.info(
        "starting @birdy/analyzer service",
        grpc_enabled=kwargs["grpc_enabled"],
        kafka_enabled=kwargs["kafka_enabled"],
    )

    config = Config(**kwargs)

    analyzer: Analyzer = Analyzer(config)
    consumer: Consumer | None = None
    server: Server | None = None

    if config.kafka_enabled:
        consumer = Consumer(config=config, analyzer=analyzer)

    if config.grpc_enabled:
        server = Server(config=config, analyzer=analyzer)

    async def _main() -> None:
        setup_signal_handlers()

        if consumer:
            await consumer.setup(["queuing.recordings.unanalyzed"], tasks)

        if server != None:
            await server.setup()
            await server.run()
        else:
            while True:
                await asyncio.sleep(1)

    asyncio.run(_main())


if __name__ == "__main__":
    main()
