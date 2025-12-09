ARG BASE_IMAGE=debian:13.2-slim@sha256:e711a7b30ec1261130d0a121050b4ed81d7fb28aeabcf4ea0c7876d4e9f5aca2
# hadolint ignore=DL3006
FROM ${BASE_IMAGE}

ENV REFRESHED_AT=2024-06-24

LABEL name="senzing/dockerhub-util" \
  maintainer="support@senzing.com" \
  version="1.2.8"

HEALTHCHECK CMD ["/app/healthcheck.sh"]

# Run as "root" for system installation.

USER root

# Install packages via apt.

RUN apt-get update \
  && apt-get -y install --no-install-recommends \
  python3-dev \
  python3-pip \
  python3-venv \
  && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment.

RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

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
