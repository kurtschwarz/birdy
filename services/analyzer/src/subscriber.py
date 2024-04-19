import aiomqtt
import json
import logging


async def subscribe() -> None:
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
            if data["EventName"] == "s3:ObjectCreated:Put":
                logging.info(data["Records"])
