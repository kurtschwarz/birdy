import functools
import sys
import signal
import asyncio
import click
import datetime

from loguru import logger

from birdy_analyzer.analyzer import Analyzer
from birdy_analyzer.config import Config
from birdy_analyzer.kafka.consumer import Consumer
from birdy_analyzer.kafka.producer import Producer
from birdy_analyzer.grpc.server import Server
from birdy_analyzer.mqtt.service import MqttService

background_tasks = set()


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


def setup_signal_handlers(mqttService: MqttService) -> None:
    loop = asyncio.get_running_loop()

    async def _shutdown(sig: signal.Signals) -> None:
        await mqttService.publish(
            "birdy/analyzer/status/offline",
            dict(now=datetime.datetime.now(tz=datetime.UTC).isoformat()),
        )

        tasks = []
        for task in asyncio.all_tasks(loop):
            if task is not asyncio.current_task(loop):
                task.cancel()
                tasks.append(task)
        results = await asyncio.gather(*tasks, return_exceptions=True)
        print("Finished awaiting cancelled tasks, results: {0}".format(results))
        loop.stop()

    for sig in [signal.SIGINT, signal.SIGTERM]:
        loop.add_signal_handler(sig, lambda: asyncio.create_task(_shutdown(sig)))


async def shutdown(
    sig: signal.Signals,
    loop: asyncio.AbstractEventLoop,
    mqttService: MqttService,
) -> None:
    logger.info(f"Received exit signal {sig.name}")

    await mqttService.publish(
        "birdy/analyzer/status/offline",
        dict(now=datetime.datetime.now(tz=datetime.UTC).isoformat()),
    )

    tasks = []
    for task in asyncio.all_tasks(loop):
        if task is not asyncio.current_task(loop):
            task.cancel()
            tasks.append(task)

    results = await asyncio.gather(*tasks, return_exceptions=True)
    logger.info(f"Cancelled {len(tasks)} task(s), results: {results}")
    logger.info(f"Exiting")

    loop.stop()


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
@click.option("--mqtt-enabled", is_flag=True)
@click.option("--mqtt-broker")
def main(**kwargs) -> None:
    setup_logger(level=(lambda: "DEBUG" if kwargs["verbose"] else "INFO")())

    logger.info(
        "starting @birdy/analyzer service",
        grpc_enabled=kwargs["grpc_enabled"],
        kafka_enabled=kwargs["kafka_enabled"],
        mqtt_enabled=kwargs["mqtt_enabled"],
    )

    config = Config(**kwargs)

    consumer: Consumer | None = None
    producer: Producer | None = None

    if config.kafka_enabled:
        producer = Producer(config=config)

    analyzer: Analyzer = Analyzer(config, producer=producer)

    if config.kafka_enabled:
        consumer = Consumer(config=config, analyzer=analyzer)

    server: Server | None = None

    if config.grpc_enabled:
        server = Server(config=config, analyzer=analyzer)

    async def _main() -> None:
        async with MqttService(config) as mqttService:
            setup_signal_handlers(mqttService)

            await mqttService.publish(
                "birdy/analyzer/status/online",
                dict(now=datetime.datetime.now(tz=datetime.UTC).isoformat()),
            )

            if consumer:
                await consumer.setup(
                    ["queuing.recordings.unanalyzed"], background_tasks
                )

            if producer:
                await producer.setup(background_tasks, loop=asyncio.get_running_loop())

            if server != None:
                await server.setup()
                await server.run()
            else:
                while True:
                    await asyncio.sleep(1)

    asyncio.run(_main())


if __name__ == "__main__":
    main()
