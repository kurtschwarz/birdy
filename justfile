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

build *argv:
  #!/usr/bin/env bash
  set -exuo pipefail

  just ./packages/protos/compile

  {{compose}} build {{argv}}

dev *argv:
  #!/usr/bin/env bash
  set -exuo pipefail

  {{compose}} up {{argv}}
