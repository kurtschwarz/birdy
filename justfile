#!/usr/bin/env just --justfile

set shell := ["bash", "-exuo", "pipefail", "-c"]
set export := true
set dotenv-load := false
set positional-arguments := true

toolchain := "docker"

docker-bin  := `which docker ||:`
docker-args := ""
docker      := docker-bin + " " + docker-args

compose-bin  := docker-bin + " " + "compose"
compose-args := "-p birdy"
compose      := compose-bin + " " + compose-args

init:
  #!/usr/bin/env bash
  set -exuo pipefail

  pre-commit install

codegen:
  #!/usr/bin/env bash
  set -exuo pipefail

  just ./packages/data/codegen
  just ./packages/mqtt/codegen
  just ./packages/protos/codegen

build *argv: (codegen)
  #!/usr/bin/env bash
  set -exuo pipefail

  PNPM_VERSION=$(jq -r '.devDependencies.pnpm' package.json)
  TURBO_VERSION=$(jq -r '.devDependencies.turbo' package.json)

  {{compose}} build \
    --progress plain \
    --build-arg PNPM_VERSION=${PNPM_VERSION} \
    --build-arg TURBO_VERSION=${TURBO_VERSION} \
    {{argv}}

run *argv:
  #!/usr/bin/env bash
  set -exuo pipefail

  if [[ "{{argv}}" = third-party ]] ; then
    {{compose}} up minio minio-init redpanda redpanda-console mqtt
  else
    {{compose}} up {{argv}}
  fi

migrate *services='collector':
  #!/usr/bin/env bash
  set -exuo pipefail

  for _service in {{services}} ; do
    {{docker}} exec -it --workdir /birdy/packages/data/ \
      birdy-${_service}-1 \
        pnpm exec prisma migrate deploy
  done

create type service='collector' *args='':
  #!/usr/bin/env bash
  set -exuo pipefail

  if [[ "{{type}}" = migration ]] ; then
    {{docker}} exec -it --workdir /birdy/packages/data/ \
      birdy-{{service}}-1 \
        pnpm exec prisma migrate dev {{args}}
  fi

clean:
  #!/usr/bin/env bash
  set -exuo pipefail

  find . -name node_modules -type d -prune -exec rm -rf '{}' +
  find . -name __pycache__ -type d -prune -exec rm -rf '{}' +
  find . -name .pdm-build -type d -prune -exec rm -rf '{}' +

# Local Variables:
# mode: makefile
# End:
# vim: set ft=make :
