import asyncio
import confluent_kafka


async def consume() -> None:
    consumer = confluent_kafka.Consumer(
        {
            "group.id": "birdy-analyzer",
            "bootstrap.servers": "redpanda.birdy.home.arpa:9092",
            "auto.offset.reset": "earliest",
            "enable.auto.offset.store": False,
        },
    )
    consumer.subscribe(["queuing.recordings.unanalyzed"])

    loop = asyncio.get_running_loop()

    try:
        while True:
            message = await loop.run_in_executor(None, consumer.poll, 0.1)
            if message is None:
                continue
            if message.error():
                continue
            consumer.store_offsets(message=message)
    finally:
        consumer.close()
