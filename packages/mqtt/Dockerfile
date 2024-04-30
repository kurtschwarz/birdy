# syntax=docker/dockerfile:1.2.1-labs

# --- global arguments ----------------------------------------------------------------------------

ARG NODE_BUILD_VERSION=21.7.3-bookworm-slim@sha256:fb82287cf66ca32d854c05f54251fca8b572149163f154248df7e800003c90b5

ARG PNPM_VERSION
ARG TURBO_VERSION

# --- base layer ----------------------------------------------------------------------------------

FROM node:${NODE_BUILD_VERSION} AS base

ARG PNPM_VERSION
ARG TURBO_VERSION

ENV TZ=UTC

RUN npm install --global \
      "pnpm@${PNPM_VERSION}" \
      "turbo@${TURBO_VERSION}" && \
    \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# -------------------------------------------------------------------------------------------------

FROM base AS turbo-prune

COPY . /birdy/
WORKDIR /birdy/
RUN turbo prune --docker --scope="@birdy/mqtt"

# -------------------------------------------------------------------------------------------------

FROM base AS dependencies

COPY --from=turbo-prune /birdy/out/json/ /birdy
COPY ./tsconfig.json /birdy/tsconfig.json

WORKDIR /birdy
RUN --mount=type=cache,target=/home/node/.pnpm-store,uid=1000,gid=1000 \
    pnpm config set store-dir /home/node/.pnpm-store && \
    pnpm install --prefer-offline --frozen-lockfile

# -------------------------------------------------------------------------------------------------

FROM base as codegen

COPY --from=dependencies /birdy /birdy
COPY --from=turbo-prune /birdy/out/full /birdy
WORKDIR /birdy/packages/mqtt/
RUN pnpm exec tsx codegen.ts

# -------------------------------------------------------------------------------------------------

FROM scratch

COPY --from=codegen /birdy/packages/mqtt/gen/ /
