# dockerhub-util

## Synopsis

Utilities for working with hub.docker.com registry and repositories.

## Overview

The [dockerhub-util.py](dockerhub-util.py) python script works with DockerHub metadata.

To see all of the subcommands, run:

```console
$ ./dockerhub-util.py --help
usage: dockerhub-util.py [-h]
                         {print-latest-versions,sleep,version,docker-acceptance-test}
                         ...

Reports from DockerHub. For more information, see
https://github.com/Senzing/dockerhub-util

positional arguments:
  {print-latest-versions,sleep,version,docker-acceptance-test}
                        Subcommands (SENZING_SUBCOMMAND):
    print-latest-versions
                        Print latest versions of Docker images.
    sleep               Do nothing but sleep. For Docker testing.
    version             Print version of program.
    docker-acceptance-test
                        For Docker acceptance testing.

optional arguments:
  -h, --help            show this help message and exit
```

### Contents

1. [Preamble](#preamble)
    1. [Legend](#legend)
1. [Related artifacts](#related-artifacts)
1. [Expectations](#expectations)
1. [Demonstrate using Command Line Interface](#demonstrate-using-command-line-interface)
    1. [Prerequisites for CLI](#prerequisites-for-cli)
    1. [Download](#download)
    1. [Run command](#run-command)
1. [Demonstrate using Docker](#demonstrate-using-docker)
    1. [Prerequisites for Docker](#prerequisites-for-docker)
    1. [Run Docker container](#run-docker-container)
1. [Develop](#develop)
    1. [Prerequisites for development](#prerequisites-for-development)
    1. [Clone repository](#clone-repository)
    1. [Build Docker image](#build-docker-image)
1. [Examples](#examples)
    1. [Examples of CLI](#examples-of-cli)
    1. [Examples of Docker](#examples-of-docker)
1. [Advanced](#advanced)
    1. [Configuration](#configuration)
1. [Errors](#errors)
1. [References](#references)

## Preamble

At [Senzing](http://senzing.com),
we strive to create GitHub documentation in a
"[don't make me think](https://github.com/Senzing/knowledge-base/blob/main/WHATIS/dont-make-me-think.md)" style.
For the most part, instructions are copy and paste.
Whenever thinking is needed, it's marked with a "thinking" icon :thinking:.
Whenever customization is needed, it's marked with a "pencil" icon :pencil2:.
If the instructions are not clear, please let us know by opening a new
[Documentation issue](https://github.com/Senzing/dockerhub-util/issues/new?template=documentation_request.md)
describing where we can improve.   Now on with the show...

### Legend

1. :thinking: - A "thinker" icon means that a little extra thinking may be required.
   Perhaps there are some choices to be made.
   Perhaps it's an optional step.
1. :pencil2: - A "pencil" icon means that the instructions may need modification before performing.
1. :warning: - A "warning" icon means that something tricky is happening, so pay attention.

## Related artifacts

1. [DockerHub](https://hub.docker.com/r/senzing/dockerhub-util)

## Expectations

- **Space:** This repository and demonstration require 3 MB free disk space.
- **Time:** Budget 20 minutes to get the demonstration up-and-running, depending on CPU and network speeds.
- **Background knowledge:** This repository assumes a working knowledge of:
  - [Docker](https://github.com/Senzing/knowledge-base/blob/main/WHATIS/docker.md)

## Demonstrate using Command Line Interface

### Prerequisites for CLI

:thinking: The following tasks need to be complete before proceeding.
These are "one-time tasks" which may already have been completed.

1. Install system dependencies:
    1. Use `apt` based installation for Debian, Ubuntu and
       [others](https://en.wikipedia.org/wiki/List_of_Linux_distributions#Debian-based)
        1. See [apt-packages.txt](src/apt-packages.txt) for list
    1. Use `yum` based installation for Red Hat, CentOS, openSuse and
       [others](https://en.wikipedia.org/wiki/List_of_Linux_distributions#RPM-based).
        1. See [yum-packages.txt](src/yum-packages.txt) for list
1. Install Python dependencies:
    1. See [requirements.txt](requirements.txt) for list
        1. [Installation hints](https://github.com/Senzing/knowledge-base/blob/main/HOWTO/install-python-dependencies.md)

### Download

1. Get a local copy of
   [template-python.py](template-python.py).
   Example:

    1. :pencil2: Specify where to download file.
       Example:

        ```console
        export SENZING_DOWNLOAD_FILE=~/dockerhub-util.py
        ```

    1. Download file.
       Example:

        ```console
        curl -X GET \
          --output ${SENZING_DOWNLOAD_FILE} \
          https://raw.githubusercontent.com/Senzing/dockerhub-util/main/dockerhub-util.py
        ```

    1. Make file executable.
       Example:

        ```console
        chmod +x ${SENZING_DOWNLOAD_FILE}
        ```

1. :thinking: **Alternative:** The entire git repository can be downloaded by following instructions at
   [Clone repository](#clone-repository)

### Run command

1. Run the command.
   Example:

   ```console
   ${SENZING_DOWNLOAD_FILE} --help
   ```

1. For more examples of use, see [Examples of CLI](#examples-of-cli).

## Demonstrate using Docker

### Prerequisites for Docker

:thinking: The following tasks need to be complete before proceeding.
These are "one-time tasks" which may already have been completed.

1. The following software programs need to be installed:
    1. [docker](https://github.com/Senzing/knowledge-base/blob/main/HOWTO/install-docker.md)

### Run Docker container

Although the `Docker run` command looks complex,
it accounts for all of the optional variations described above.
Unset `*_PARAMETER` environment variables have no effect on the
`docker run` command and may be removed or remain.

1. Run Docker container.
   Example:

    ```console
    sudo docker run \
      --rm \
      senzing/dockerhub-util
    ```

1. For more examples of use, see [Examples of Docker](#examples-of-docker).

## Develop

The following instructions are used when modifying and building the Docker image.

### Prerequisites for development

:thinking: The following tasks need to be complete before proceeding.
These are "one-time tasks" which may already have been completed.

1. The following software programs need to be installed:
    1. [git](https://github.com/Senzing/knowledge-base/blob/main/HOWTO/install-git.md)
    1. [make](https://github.com/Senzing/knowledge-base/blob/main/HOWTO/install-make.md)
    1. [docker](https://github.com/Senzing/knowledge-base/blob/main/HOWTO/install-docker.md)

### Clone repository

For more information on environment variables,
see [Environment Variables](https://github.com/Senzing/knowledge-base/blob/main/lists/environment-variables.md).

1. Set these environment variable values:

    ```console
    export GIT_ACCOUNT=senzing
    export GIT_REPOSITORY=template-docker
    export GIT_ACCOUNT_DIR=~/${GIT_ACCOUNT}.git
    export GIT_REPOSITORY_DIR="${GIT_ACCOUNT_DIR}/${GIT_REPOSITORY}"
    ```

1. Using the environment variables values just set, follow steps in [clone-repository](https://github.com/Senzing/knowledge-base/blob/main/HOWTO/clone-repository.md) to install the Git repository.

### Build Docker image

1. **Option #1:** Using `docker` command and GitHub.

    ```console
    sudo docker build \
      --tag senzing/template \
      https://github.com/senzing/template-docker.git#main
    ```

1. **Option #2:** Using `docker` command and local repository.

    ```console
    cd ${GIT_REPOSITORY_DIR}
    sudo docker build --tag senzing/template .
    ```

1. **Option #3:** Using `make` command.

    ```console
    cd ${GIT_REPOSITORY_DIR}
    sudo make docker-build
    ```

    Note: `sudo make docker-build-development-cache` can be used to create cached Docker layers.

## Examples

### Examples of CLI

The following examples require initialization described in
[Demonstrate using Command Line Interface](#demonstrate-using-command-line-interface).

#### Create reports

1. Create `knowledge-base/lists/docker-versions-latest.sh`
   Example:

    ```console
    ~/senzing.git/dockerhub-util/dockerhub-util.py print-latest-versions \
        > ~/senzing.git/knowledge-base/lists/docker-versions-latest.sh
    ```

1. Create `knowledge-base/lists/docker-image-names.json`
   Example:

    ```console
    ~/senzing.git/dockerhub-util/dockerhub-util.py print-image-names \
        > ~/senzing.git/knowledge-base/lists/docker-image-names.json
    ```

1. Create `knowledge-base/lists/docker-active-image-names.json`
   Example:

    ```console
    ~/senzing.git/dockerhub-util/dockerhub-util.py print-active-image-names \
        > ~/senzing.git/knowledge-base/lists/docker-active-image-names.json
    ```

### Examples of Docker

The following examples require initialization described in
[Demonstrate using Docker](#demonstrate-using-docker).

1. Print contents of `knowledge-base/lists/docker-versions-latest.sh` to terminal.
   Example:

    ```console
    sudo docker run \
      --rm \
      senzing/dockerhub-util \
        print-latest-versions
    ```

## Advanced

### Configuration

Configuration values specified by environment variable or command line parameter.

- **[SENZING_DEBUG](https://github.com/Senzing/knowledge-base/blob/main/lists/environment-variables.md#senzing_debug)**
- **[SENZING_DOCKERHUB_API_ENDPOINT_V1](https://github.com/Senzing/knowledge-base/blob/main/lists/environment-variables.md#senzing_dockerhub_api_endpoint_v1)**
- **[SENZING_DOCKERHUB_API_ENDPOINT_V2](https://github.com/Senzing/knowledge-base/blob/main/lists/environment-variables.md#senzing_dockerhub_api_endpoint_v2)**
- **[SENZING_DOCKERHUB_ORGANIZATION](https://github.com/Senzing/knowledge-base/blob/main/lists/environment-variables.md#senzing_dockerhub_organization)**
- **[SENZING_DOCKERHUB_PASSWORD](https://github.com/Senzing/knowledge-base/blob/main/lists/environment-variables.md#senzing_dockerhub_password)**
- **[SENZING_DOCKERHUB_USERNAME](https://github.com/Senzing/knowledge-base/blob/main/lists/environment-variables.md#senzing_dockerhub_username)**
- **[SENZING_SLEEP_TIME_IN_SECONDS](https://github.com/Senzing/knowledge-base/blob/main/lists/environment-variables.md#senzing_sleep_time_in_seconds)**
- **[SENZING_SUBCOMMAND](https://github.com/Senzing/knowledge-base/blob/main/lists/environment-variables.md#senzing_subcommand)**

## Errors

1. See [docs/errors.md](docs/errors.md).

## References

1. [Bitnami's Best Practices for Securing and Hardening Container Images](https://docs.bitnami.com/tutorials/bitnami-best-practices-hardening-containers)
