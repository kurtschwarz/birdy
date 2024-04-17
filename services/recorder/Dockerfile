# syntax=docker/dockerfile:1.2.1-labs

# --- global arguments ----------------------------------------------------------------------------

ARG SERVICE_NAME=recorder
ARG SERVICE_VERSION

ARG NODE_BUILD_VERSION=21.7.3-bookworm@sha256:162d92c5f1467ad877bf6d8a098d9b04d7303879017a2f3644bfb1de1fc88ff0
ARG NODE_RUNTIME_VERSION=21.7.3-bookworm-slim@sha256:fb82287cf66ca32d854c05f54251fca8b572149163f154248df7e800003c90b5

ARG PNPM_VERSION=8.15.6

# --- base layer (full) ---------------------------------------------------------------------------

FROM node:${NODE_BUILD_VERSION} AS base

ARG SERVICE_NAME
ENV SERVICE_NAME=${SERVICE_NAME}

ARG SERVICE_VERSION
ENV SERVICE_VERSION=${SERVICE_VERSION}

ARG PNPM_VERSION
ENV PNPM_VERSION=${PNPM_VERSION}

ENV TZ=UTC

RUN apt-get update && \
    apt-get install --yes --no-install-recommends \
      ffmpeg && \
    \
    npm install --global \
      pnpm@${PNPM_VERSION} && \
    \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# -------------------------------------------------------------------------------------------------

FROM base AS dependencies

COPY --chown=node:node ./package*.json ./pnpm-*.yaml /birdy/
COPY --chown=node:node services/${SERVICE_NAME}/package*.json /birdy/services/${SERVICE_NAME}/

COPY --chown=node:node ./packages/config/package*.json /birdy/packages/config/
COPY --chown=node:node ./packages/data/package*.json /birdy/packages/data/
COPY --chown=node:node ./packages/protos/package*.json /birdy/packages/protos/

WORKDIR /birdy
RUN pnpm config set store-dir /home/node/.pnpm-store
RUN --mount=type=cache,target=/home/node/.pnpm-store,uid=1000,gid=1000 \
  pnpm install --prefer-offline --frozen-lockfile

# ---

FROM base as dev

COPY --from=dependencies /birdy/ /birdy/
COPY --chown=node:node tsconfig*.json /birdy/
COPY --chown=node:node services/${SERVICE_NAME}/ /birdy/services/${SERVICE_NAME}/

COPY --chown=node:node ./packages/config/ /birdy/packages/config/
COPY --chown=node:node ./packages/data/ /birdy/packages/data/
COPY --chown=node:node ./packages/protos/ /birdy/packages/protos/

WORKDIR /birdy/packages/data/
RUN pnpm exec prisma generate

WORKDIR /birdy/services/${SERVICE_NAME}/
EXPOSE 3000/tcp
ENTRYPOINT [ "pnpm" ]
CMD [ "run", "dev" ]
