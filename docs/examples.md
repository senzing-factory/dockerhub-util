# dockerhub-util examples

## Examples of CLI

The following examples require initialization described in
[Demonstrate using Command Line Interface](../README.md#demonstrate-using-command-line-interface).

### Create reports

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

1. Create `knowledge-base/lists/docker-active-image-names.txt`
   Example:

    ```console
    ~/senzing.git/dockerhub-util/dockerhub-util.py print-active-image-names \
        > ~/senzing.git/knowledge-base/lists/docker-active-image-names.txt
    ```

## Examples of Docker

The following examples require initialization described in
[Demonstrate using Docker](../README.md#demonstrate-using-docker).

1. Print contents of `knowledge-base/lists/docker-versions-latest.sh` to terminal.
   Example:

    ```console
    sudo docker run \
      --rm \
      senzing/dockerhub-util \
        print-latest-versions
    ```
