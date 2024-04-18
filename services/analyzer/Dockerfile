# syntax=docker/dockerfile:1.2.1-labs

# --- global arguments ----------------------------------------------------------------------------

ARG SERVICE_NAME=analyzer
ARG SERVICE_VERSION

ARG PYTHON_BUILD_VERSION=3.12.3-bookworm@sha256:c6751fa575260522ca11fbad88394e12cbe31d0d8951d3d29301192745a09aab
ARG PYTHON_RUNTIME_VERSION=3.12.3-slim-bookworm@sha256:541d45d3d675fb8197f534525a671e2f8d66c882b89491f9dda271f4f94dcd06

ARG PNPM_VERSION
ARG TURBO_VERSION

# --- base layer (full) ---------------------------------------------------------------------------

FROM python:${PYTHON_BUILD_VERSION} AS base

ARG SERVICE_NAME
ENV SERVICE_NAME=${SERVICE_NAME}

ARG SERVICE_VERSION
ENV SERVICE_VERSION=${SERVICE_VERSION}

ENV TZ=UTC

# -------------------------------------------------------------------------------------------------

FROM base AS dependencies

COPY ./services/${SERVICE_NAME}/requirements.txt /birdy/services/${SERVICE_NAME}/
WORKDIR /birdy/services/${SERVICE_NAME}
RUN pip install --no-cache-dir -r requirements.txt

# -------------------------------------------------------------------------------------------------

FROM base AS dev

COPY --from=dependencies /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY ./services/${SERVICE_NAME}/ /birdy/services/${SERVICE_NAME}/
COPY ./packages/protos/gen/py/ /birdy/packages/protos/gen/py/

WORKDIR /birdy/services/${SERVICE_NAME}
ENTRYPOINT [ "python" ]
CMD [ "main.py" ]
