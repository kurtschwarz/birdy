<p align="center">
  <img src="./docs/images/logo.png" width="300" />
</p>

# Birdy

## Architecture

#### [`@birdy/recorder`](./services/recorder)

[![TypeScript](https://img.shields.io/badge/%3C%2F%3E-TypeScript-%230074c1.svg)](http://www.typescriptlang.org/) [![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=flat-square)](https://github.com/prettier/prettier)

The `@birdy/recorder` service is responsible for collecting audio from a single microphone in a specific location.

 - You should deploy as many `@birdy/recorder` services as you need.
 - View the [📕 Recorder Service Docs](services/recorder/README.md) for details about features, configuration, deployment, etc.

#### [`@birdy/collector`](./services/collector)

[![TypeScript](https://img.shields.io/badge/%3C%2F%3E-TypeScript-%230074c1.svg)](http://www.typescriptlang.org/) [![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=flat-square)](https://github.com/prettier/prettier)

The `@birdy/collector` service is responsible for gathering the raw recordings produced by the `@birdy/recorder` services and storing them in [Minio](https://min.io/).

 - You should only need to deploy a single `@birdy/collector` instance.
 - View the [📕 Collector Service Docs](services/collector/README.md) for details about features, configuration, deployment, etc.

#### [`@birdy/analyzer`](./services/analyzer)

[![Python](https://img.shields.io/badge/%3C%2F%3E-Python-%230074c1.svg)](http://www.python.org/) [![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This is a future machine learning service that will use [BirdNET](https://github.com/kahst/BirdNET-Analyzer) to identify birds via the recordings recorded by `@birdy/recorder` and collected by `@birdy/collector`.

 - View the [📕 Analyzer Service Docs](services/analyzer/README.md) for details about features, configuration, deployment, etc.

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
