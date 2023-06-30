# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
[markdownlint](https://dlaa.me/markdownlint/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.4] - 2023-06-30

### Changed in 1.2.4

- Update non-Senzing docker versions

## [1.2.3] - 2023-04-04

### Changed in 1.2.3

- Update non-Senzing docker versions

## [1.2.2] - 2023-01-16

### Changed in 1.2.2

- Update non-Senzing docker versions

## [1.2.1] - 2022-09-29

### Changed in 1.2.1

- In `Dockerfile`, updated FROM instruction to `debian:11.5-slim@sha256:5cf1d98cd0805951484f33b34c1ab25aac7007bb41c8b9901d97e4be3cf3ab04`

## [1.2.0] - 2022-09-14

### Added in 1.2.0

- Migrated off `v1` DockerHub URLs

## [1.1.0] - 2022-08-26

### Added in 1.1.0

- `print-active-image-names` subcommand

### Changed in 1.1.0

- In `Dockerfile`, bump from `debian:11.3-slim@sha256:fbaacd55d14bd0ae0c0441c2347217da77ad83c517054623357d1f9d07f79f5e` to `debian:11.4-slim@sha256:68c1f6bae105595d2ebec1589d9d476ba2939fdb11eaba1daec4ea826635ce75`
- Update list of Docker images
- Update hard-coded Docker image versions

## [1.0.5] - 2022-05-10

### Changed in 1.0.5

- Added `SENZING_DOCKER_IMAGE_VERSION_ENTITY_SEARCH_WEB_APP_CONSOLE`

## [1.0.4] - 2022-04-22

### Changed in 1.0.4

- Updated pinned versions

## [1.0.3] - 2021-10-12

### Changed in 1.0.3

- Updated pinned versions

## [1.0.2] - 2021-07-22

### Changed in 1.0.2

- Change base to `debian:10.10`
- Use `requirements.txt`
- Fix Semantic Versioning comparison
- Add `SENZING_DOCKER_IMAGE_VERSION_*` variables

## [1.0.1] - 2021-04-09

### Changed in 1.0.1

- Add a list of redacted image versions

## [1.0.0] - 2021-02-22

### Added to 1.0.0

- Subcommand: print-latest-versions
