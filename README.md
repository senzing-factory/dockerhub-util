# dockerhub-util

## Synopsis

Utilities for working with hub.docker.com registry and repositories.

## Overview

The [dockerhub-util.py] python script works with DockerHub metadata.

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

1. [Preamble]
   1. [Legend]
1. [Expectations]
1. [Demonstrate using command-line interface]
   1. [Prerequisites for CLI]
   1. [Download]
   1. [Run command]
1. [Demonstrate using Docker]
   1. [Prerequisites for Docker]
   1. [Run Docker container]
1. [Configuration]
1. [References]

## Preamble

At [Senzing], we strive to create GitHub documentation in a
"[don't make me think]" style. For the most part, instructions are copy and paste.
Whenever thinking is needed, it's marked with a "thinking" icon :thinking:.
Whenever customization is needed, it's marked with a "pencil" icon :pencil2:.
If the instructions are not clear, please let us know by opening a new
[Documentation issue] describing where we can improve. Now on with the show...

### Legend

1. :thinking: - A "thinker" icon means that a little extra thinking may be required.
   Perhaps there are some choices to be made.
   Perhaps it's an optional step.
1. :pencil2: - A "pencil" icon means that the instructions may need modification before performing.
1. :warning: - A "warning" icon means that something tricky is happening, so pay attention.

## Expectations

- **Space:** This repository and demonstration require 3 MB free disk space.
- **Time:** Budget 20 minutes to get the demonstration up-and-running, depending on CPU and network speeds.
- **Background knowledge:** This repository assumes a working knowledge of:
  - [Docker]

## Demonstrate using command-line interface

### Prerequisites for CLI

:thinking: The following tasks need to be complete before proceeding.
These are "one-time tasks" which may already have been completed.

1. Install system dependencies:
   1. Use `apt` based installation for [Debian, Ubuntu and others]
      1. See [apt-packages.txt] for list
   1. Use `yum` based installation for [Red Hat, CentOS, openSuse and others].
      1. See [yum-packages.txt] for list
1. Install Python dependencies:
   1. See [requirements.txt] for list
      1. [Installation hints]

### Download

1. Get a local copy of [template-python.py].
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

1. :thinking: **Alternative:** The entire Git repository can be downloaded by following instructions at [Clone repository]

### Run command

1. Run the command.
   Example:

   ```console
   ${SENZING_DOWNLOAD_FILE} --help
   ```

1. For more examples of use, see [Examples of CLI].

## Demonstrate using Docker

### Prerequisites for Docker

:thinking: The following tasks need to be complete before proceeding.
These are "one-time tasks" which may already have been completed.

1. The following software programs need to be installed:
   1. [Docker]

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

1. For more examples of use, see [Examples of Docker].

## Configuration

Configuration values specified by environment variable or command-line parameter.

- **[SENZING_DEBUG]**
- **[SENZING_DOCKERHUB_API_ENDPOINT_V1]**
- **[SENZING_DOCKERHUB_API_ENDPOINT_V2]**
- **[SENZING_DOCKERHUB_ORGANIZATION]**
- **[SENZING_DOCKERHUB_PASSWORD]**
- **[SENZING_DOCKERHUB_USERNAME]**
- **[SENZING_SLEEP_TIME_IN_SECONDS]**
- **[SENZING_SUBCOMMAND]**

## References

1. [Bitnami's Best Practices for Securing and Hardening Container Images]
1. [Development]
1. [Errors]
1. [Examples]
1. Related artifacts:
   1. [DockerHub]

[apt-packages.txt]: src/apt-packages.txt
[Bitnami's Best Practices for Securing and Hardening Container Images]: https://docs.bitnami.com/tutorials/bitnami-best-practices-hardening-containers
[Clone repository]: development.md#clone-repository
[Configuration]: #configuration
[Debian, Ubuntu and others]: https://en.wikipedia.org/wiki/List_of_Linux_distributions#Debian-based
[Demonstrate using command-line interface]: #demonstrate-using-command-line-interface
[Demonstrate using Docker]: #demonstrate-using-docker
[Development]: docs/development.md
[Docker]: https://github.com/Senzing/knowledge-base/blob/main/WHATIS/docker.md
[dockerhub-util.py]: dockerhub-util.py
[DockerHub]: https://hub.docker.com/r/senzing/dockerhub-util
[Documentation issue]: https://github.com/Senzing/dockerhub-util/issues/new?template=documentation_request.md
[don't make me think]: https://github.com/Senzing/knowledge-base/blob/main/WHATIS/dont-make-me-think.md
[Download]: #download
[Errors]: docs/errors.md
[Examples of CLI]: docs/examples.md#examples-of-cli
[Examples of Docker]: docs/examples.md#examples-of-docker
[Examples]: docs/examples.md
[Expectations]: #expectations
[Installation hints]: https://github.com/Senzing/knowledge-base/blob/main/HOWTO/install-python-dependencies.md
[Legend]: #legend
[Preamble]: #preamble
[Prerequisites for CLI]: #prerequisites-for-cli
[Prerequisites for Docker]: #prerequisites-for-docker
[Red Hat, CentOS, openSuse and others]: https://en.wikipedia.org/wiki/List_of_Linux_distributions#RPM-based
[References]: #references
[requirements.txt]: requirements.txt
[Run command]: #run-command
[Run Docker container]: #run-docker-container
[SENZING_DEBUG]: https://github.com/Senzing/knowledge-base/blob/main/lists/environment-variables.md#senzing_debug
[SENZING_DOCKERHUB_API_ENDPOINT_V1]: https://github.com/Senzing/knowledge-base/blob/main/lists/environment-variables.md#senzing_dockerhub_api_endpoint_v1
[SENZING_DOCKERHUB_API_ENDPOINT_V2]: https://github.com/Senzing/knowledge-base/blob/main/lists/environment-variables.md#senzing_dockerhub_api_endpoint_v2
[SENZING_DOCKERHUB_ORGANIZATION]: https://github.com/Senzing/knowledge-base/blob/main/lists/environment-variables.md#senzing_dockerhub_organization
[SENZING_DOCKERHUB_PASSWORD]: https://github.com/Senzing/knowledge-base/blob/main/lists/environment-variables.md#senzing_dockerhub_password
[SENZING_DOCKERHUB_USERNAME]: https://github.com/Senzing/knowledge-base/blob/main/lists/environment-variables.md#senzing_dockerhub_username
[SENZING_SLEEP_TIME_IN_SECONDS]: https://github.com/Senzing/knowledge-base/blob/main/lists/environment-variables.md#senzing_sleep_time_in_seconds
[SENZING_SUBCOMMAND]: https://github.com/Senzing/knowledge-base/blob/main/lists/environment-variables.md#senzing_subcommand
[Senzing]: https://senzing.com
[template-python.py]: template-python.py
[yum-packages.txt]: src/yum-packages.txt
