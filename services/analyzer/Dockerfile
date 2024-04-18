# syntax=docker/dockerfile:1.2.1-labs

# --- global arguments ----------------------------------------------------------------------------

ARG SERVICE_NAME=analyzer
ARG SERVICE_VERSION

ARG PYTHON_BUILD_VERSION=3.11.9-bookworm@sha256:abe34d06fca0165d40375b0e840fd3296ad2d075954d3a400d4efefe0e9b3012
ARG PYTHON_RUNTIME_VERSION=3.11.9-slim-bookworm@sha256:dad770592ab3582ab2dabcf0e18a863df9d86bd9d23efcfa614110ce49ac20e4

ARG PNPM_VERSION
ARG TURBO_VERSION

# --- base layer (full) ---------------------------------------------------------------------------

FROM python:${PYTHON_BUILD_VERSION} AS base

ARG SERVICE_NAME
ENV SERVICE_NAME=${SERVICE_NAME}

ARG SERVICE_VERSION
ENV SERVICE_VERSION=${SERVICE_VERSION}

ENV TZ=UTC

RUN apt-get update && \
    apt-get install --yes --no-install-recommends \
      "ffmpeg=7:5.1.4*" && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# -------------------------------------------------------------------------------------------------

FROM base AS dependencies

COPY ./services/${SERVICE_NAME}/requirements.txt /birdy/services/${SERVICE_NAME}/
WORKDIR /birdy/services/${SERVICE_NAME}
RUN pip install --no-cache-dir -r requirements.txt

# -------------------------------------------------------------------------------------------------

FROM base AS dev

COPY --from=dependencies /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY ./services/${SERVICE_NAME}/src/ /birdy/services/${SERVICE_NAME}/src/
COPY ./packages/protos/gen/py/ /birdy/packages/protos/gen/py/
WORKDIR /birdy/services/${SERVICE_NAME}/src/
ENTRYPOINT [ "python" ]
CMD [ "main.py" ]
