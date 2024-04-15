# syntax=docker/dockerfile:1.2.1-labs

# --- global arguments ----------------------------------------------------------------------------

ARG NODE_VERSION=21.7.3-alpine3.18@sha256:2d77508808463f835e81f103aa6693ce929cce73d234e9fd4dae9e062af08748
ARG PYTHON_VERSION=3.12.3-alpine3.18@sha256:24680ddf8422899b24756d62b31eb5de782fbb42e9c2bb1c70f1f55fcf891721
ARG BUF_VERSION=1.30.1@sha256:fe441f13aa28d6a14400af1393ddc18e907ba30fdf146628bbabead45ff71ce0
ARG ALPINE_VERSION=3.18.6@sha256:11e21d7b981a59554b3f822c49f6e9f57b6068bb74f49c4cd5cc4c663c7e5160

# --- layers --------------------------------------------------------------------------------------

FROM node:${NODE_VERSION} AS node

FROM python:${PYTHON_VERSION} AS python

FROM bufbuild/buf:${BUF_VERSION} AS buf

FROM alpine:${ALPINE_VERSION}

COPY --from=node /usr/lib/ /usr/lib/
COPY --from=node /usr/local/bin/ /usr/local/bin/
COPY --from=node /usr/local/lib/ /usr/local/lib/
COPY --from=node /usr/local/include/ /usr/local/include/

COPY --from=python /usr/lib/ /usr/lib/
COPY --from=python /usr/local/bin/ /usr/local/bin/
COPY --from=python /usr/local/lib/ /usr/local/lib/
COPY --from=python /usr/local/include/ /usr/local/include/

COPY --from=buf /usr/local/bin/buf /usr/local/bin/buf

RUN apk update && \
    apk add --no-cache \
      g++ \
      musl-dev \
      libffi-dev && \
    \
    npm install --global \
      @bufbuild/protobuf \
      @bufbuild/protoc-gen-es \
      @connectrpc/connect@^1.4.0 \
      google-protobuf@^3.21.2 && \
    \
    python -m pip install \
      grpcio==1.62.1

ENTRYPOINT [ "/usr/local/bin/buf" ]
