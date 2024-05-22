ARG BASE_IMAGE=debian:11.9-slim@sha256:0e75382930ceb533e2f438071307708e79dc86d9b8e433cc6dd1a96872f2651d
# hadolint ignore=DL3006
FROM ${BASE_IMAGE}

ENV REFRESHED_AT=2024-05-22

LABEL name="senzing/dockterhub-util" \
  maintainer="support@senzing.com" \
  version="1.2.5"

HEALTHCHECK CMD ["/app/healthcheck.sh"]

# Run as "root" for system installation.

USER root

# Install packages via apt.

RUN apt-get update \
  && apt-get -y install --no-install-recommends \
  python3-dev \
  python3-pip \
  && rm -rf /var/lib/apt/lists/*

# Install packages via PIP.

COPY requirements.txt /tmp
RUN pip3 install --no-cache-dir --upgrade pip \
  && pip3 install --no-cache-dir -r /tmp/requirements.txt \
  && rm /tmp/requirements.txt

# Copy files from repository.

COPY ./rootfs /
COPY ./dockerhub-util.py /app/

# Make non-root container.

USER 1001

# Runtime execution.

ENV SENZING_DOCKER_LAUNCHED=true

WORKDIR /app
ENTRYPOINT ["/app/dockerhub-util.py"]
CMD ["--help"]
