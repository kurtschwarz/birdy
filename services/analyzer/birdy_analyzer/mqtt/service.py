import aiomqtt
import json
from types import TracebackType
from typing import Self
from urllib.parse import urlparse

from birdy_analyzer.config import Config


class MqttService:
    _config: Config
    _client: aiomqtt.Client | None

    def __init__(self, config: Config) -> None:
        self._config = config

    async def __aenter__(self) -> Self:
        if not self._config.mqtt_enabled:
            return self

        self._client = (
            lambda mqtt_broker_uri: aiomqtt.Client(
                identifier="@birdy/analyzer",
                hostname=mqtt_broker_uri.hostname,
                port=mqtt_broker_uri.port,
                protocol=aiomqtt.ProtocolVersion.V5,
                clean_start=2,
            )
        )(urlparse(self._config.mqtt_broker))

        await self._client.__aenter__()

        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        if not self._config.mqtt_enabled:
            return self

        await self._client.__aexit__(exc_type=exc_type, exc=exc, tb=tb)
        return None

    async def publish(self, topic: str, message: dict) -> None:
        if not self._config.mqtt_enabled:
            return

        await self._client.publish(topic, json.dumps(message))

    async def subscribe(self) -> None:
        if not self._config.mqtt_enabled:
            return

        pass
