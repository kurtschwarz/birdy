<p align="center">
  <img src="../../docs/images/logo.png" width="300" />
</p>

# Recorder Service &ndash; `@birdy/recorder`

## Features

### MQTT

The `@birdy/recorder` service supports publishing and subscribing to messages/events via [MQTT](https://mqtt.org/).

To enable [MQTT](https://mqtt.org/) for `@birdy/recorder` you can use:

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

- `birdy/recorder/:recorderId/status/online` – The recorder service has started

  ```json
  {
    "recorderId": "<id of the recorder>",
    "now": "<current date/time>"
  }
  ```

- `birdy/recorder/:recorderId/status/offline` – The recorder service has stopped

  ```json
  {
    "recorderId": "<id of the recorder>",
    "now": "<current date/time>"
  }
  ```
