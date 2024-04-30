import sys
import signal
import asyncio
import click
import datetime

from loguru import logger
from contextlib import AsyncExitStack

from birdy_analyzer.analyzer import Analyzer
from birdy_analyzer.config import Config
from birdy_analyzer.mqtt.service import MqttService
from birdy_analyzer.grpc.service import GrpcService
from birdy_analyzer.grpc.servicer import GrpcServicer
from birdy_analyzer.kafka.service import KafkaService
from birdy_analyzer.kafka.consumers import QueuingRecordingsUnanalyzedConsumer

from birdy_mqtt import AnalyzerTopic


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


def setup_signal_handlers(mqtt: MqttService) -> None:
    loop = asyncio.get_running_loop()

    async def _shutdown(sig: signal.Signals) -> None:
        await mqtt.publish(
            AnalyzerTopic.ANALYZER_SERVICE_OFFLINE,
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

    async def _main() -> None:
        async with AsyncExitStack() as stack:
            mqtt = await stack.enter_async_context(MqttService(config))
            kafka = await stack.enter_async_context(KafkaService(config))
            grpc = await stack.enter_async_context(GrpcService(config))

            analyzer = Analyzer(config, mqtt=mqtt, kafka=kafka)

            setup_signal_handlers(mqtt)

            await mqtt.publish(
                AnalyzerTopic.ANALYZER_SERVICE_ONLINE,
                dict(now=datetime.datetime.now(tz=datetime.UTC).isoformat()),
            )

            await kafka.subscribe(
                ["queuing.recordings.unanalyzed"],
                consumer=QueuingRecordingsUnanalyzedConsumer(analyzer),
            )

            await grpc.listen(servicer=GrpcServicer(analyzer=analyzer))

    asyncio.run(_main())


if __name__ == "__main__":
    main()
