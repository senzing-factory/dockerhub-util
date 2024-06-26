# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
[markdownlint](https://dlaa.me/markdownlint/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.8] - 2024-06-24

### Changed in 1.2.8

- In `Dockerfile`, updated FROM instruction to `debian:11.9-slim@sha256:acc5810124f0929ab44fc7913c0ad936b074cbd3eadf094ac120190862ba36c4`
- In `requirements.txt`, updated:
  - requests==2.32.3
  - packaging==24.1

## [1.2.7] - 2024-05-22

### Changed in 1.2.7

- In `Dockerfile`, updated FROM instruction to `debian:11.9-slim@sha256:0e75382930ceb533e2f438071307708e79dc86d9b8e433cc6dd1a96872f2651d`
- In `requirements.txt`, updated:
  - requests==2.32.2
  - packaging==24.0

## [1.2.6] - 2024-01-16

### Changed in 1.2.6

- Update non-Senzing docker versions
- Migrated from `senzing` to `senzing-factory` GitHub Repository
- In `requirements.txt`, updated:
  - packaging==23.2

## [1.2.5] - 2023-09-30

### Changed in 1.2.5

- In `Dockerfile`, updated FROM instruction to `debian:11.7-slim@sha256:c618be84fc82aa8ba203abbb07218410b0f5b3c7cb6b4e7248fda7785d4f9946`
- In `requirements.txt`, updated:
  - requests==2.31.0
  - packaging==23.1

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
