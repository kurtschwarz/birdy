<p align="center">
  <img src="../../docs/images/logo.png" width="300" />
</p>

# Collector Service &ndash; `@birdy/collector`

## Features

### MQTT

The `@birdy/collector` service supports publishing and subscribing to messages/events via [MQTT](https://mqtt.org/).

To enable [MQTT](https://mqtt.org/) for `@birdy/collector` you can use:

  - **Command Line Arguments**

    ```
    --mqtt-enabled
    --mqtt-broker http://mqtt.birdy.home.arpa:1883
    ```

  - **Environmental Variables**

    ```bash
    MQTT_ENABLED=true
    MQTT_BROKER=http://mqtt.birdy.home.arpa:1883
    ```

  - **JSON Config**

    ```json
    {
      "mqttEnabled": true,
      "mqttBroker": "http://mqtt.birdy.home.arpa:1883"
    }
    ```

#### MQTT Topics

- `birdy/collector/:collectorId/status/online` – The collector service has started

  ```json
  {
    "collectorId": "<id of the collector>",
    "now": "<current date/time>"
  }
  ```

- `birdy/collector/:collectorId/status/offline` – The collector service has stopped

  ```json
  {
    "collectorId": "<id of the collector>",
    "now": "<current date/time>"
  }
  ```
