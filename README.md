<p align="center">
  <img src="./docs/images/logo.png" width="300" />
</p>

# Birdy

## Architecture

Birdy consists of a few independently scalable services:

#### [`@birdy/recorder`](./services/recorder)

[![TypeScript](https://img.shields.io/badge/%3C%2F%3E-TypeScript-%230074c1.svg)](http://www.typescriptlang.org/) [![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=flat-square)](https://github.com/prettier/prettier)

The `@birdy/recorder` service is responsible for collecting audio from a single microphone in a specific location.

You should deploy as many `@birdy/recorder` services as you need.

##### MQTT

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

###### MQTT Topics

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

#### [`@birdy/collector`](./services/collector)

[![TypeScript](https://img.shields.io/badge/%3C%2F%3E-TypeScript-%230074c1.svg)](http://www.typescriptlang.org/) [![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=flat-square)](https://github.com/prettier/prettier)

The `@birdy/collector` service is responsible for gathering the raw recordings produced by the `@birdy/recorder` services and storing them in [Minio](https://min.io/).

You should only need to deploy a single `@birdy/collector` instance.

##### MQTT

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

###### MQTT Topics

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

#### [`@birdy/analyzer`](./services/analyzer)

[![Python](https://img.shields.io/badge/%3C%2F%3E-Python-%230074c1.svg)](http://www.python.org/) [![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This is a future machine learning service that will use [BirdNET](https://github.com/kahst/BirdNET-Analyzer) to identify birds via the recordings recorded by `@birdy/recorder` and collected by `@birdy/collector`.

#### [`@birdy/api`](./services/api)

This is a future api to interact with the Birdy data.

#### [`@birdy/app`](./services/app)

This is a future web ui/app to view the data collected by Birdy.

## Developing

### macOS

To develop Birdy on macOS you'll need to install the `pulseaudio` package to allow us to listen to the microphone inside of Docker.

1. `brew install pulseaudio`
2. `vim /opt/homebrew/Cellar/pulseaudio/17.0/etc/pulse/default.pa`
    1. find `load-module module-native-protocol-tcp` and uncomment it, and then add `auth-ip-acl=127.0.0.1;192.168.0.0/24` after it, example:
        ```
        ### Network access (may be configured with paprefs, so leave this commented
        ### here if you plan to use paprefs)
        #load-module module-esound-protocol-tcp
        load-module module-native-protocol-tcp auth-ip-acl=127.0.0.1;192.168.0.0/24
        ```
3. start the `pulseaudio` server by running `pulseaudio --exit-idle-time=-1 --daemon`
