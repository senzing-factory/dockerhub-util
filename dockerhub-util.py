#! /usr/bin/env python3

"""
# -----------------------------------------------------------------------------
# dockerhub-util.py
# -----------------------------------------------------------------------------
"""

# Import from standard library. https://docs.python.org/3/library/

import argparse
import json
import linecache
import logging
import os
import signal
import sys
import time
from datetime import date

import requests
from packaging.version import Version

# Import from https://pypi.org/


# Metadata

__all__ = []
__version__ = "1.2.5"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2021-02-22"
__updated__ = "2024-01-16"

SENZING_PRODUCT_ID = "5018"  # See https://github.com/Senzing/knowledge-base/blob/main/lists/senzing-product-ids.md
LOG_FORMAT = "%(asctime)s %(message)s"

# Working with bytes.

KILOBYTES = 1024
MEGABYTES = 1024 * KILOBYTES
GIGABYTES = 1024 * MEGABYTES

# The "configuration_locator" describes where configuration variables are in:
# 1) Command line options, 2) Environment variables, 3) Configuration files, 4) Default values

CONFIGURATION_LOCATOR = {
    "debug": {"default": False, "env": "SENZING_DEBUG", "cli": "debug"},
    "dockerhub_api_endpoint_v2": {
        "default": "https://hub.docker.com/v2",
        "env": "SENZING_DOCKERHUB_API_ENDPOINT_V2",
        "cli": "dockerhub-api-endpoint-v2",
    },
    "dockerhub_organization": {
        "default": "senzing",
        "env": "SENZING_DOCKERHUB_ORGANIZATION",
        "cli": "dockerhub-organization",
    },
    "dockerhub_password": {
        "default": None,
        "env": "SENZING_DOCKERHUB_PASSWORD",
        "cli": "dockerhub-password",
    },
    "dockerhub_username": {
        "default": None,
        "env": "SENZING_DOCKERHUB_USERNAME",
        "cli": "dockerhub-username",
    },
    "print_format": {
        "default": "{0}",
        "env": "SENZING_PRINT_FORMAT",
        "cli": "print-format",
    },
    "sleep_time_in_seconds": {
        "default": 0,
        "env": "SENZING_SLEEP_TIME_IN_SECONDS",
        "cli": "sleep-time-in-seconds",
    },
    "subcommand": {
        "default": None,
        "env": "SENZING_SUBCOMMAND",
    },
}

# Enumerate keys in 'configuration_locator' that should not be printed to the log.

KEYS_TO_REDACT = [
    "dockerhub_password",
]

REDACT_VERSIONS = ["experimental", "latest", "sha256-", "staging", "test"]

# Docker registries for knowledge-base/lists/docker-versions-latest.sh

DOCKERHUB_REPOSITORIES_FOR_LATEST = {
    "adminer": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_ADMINER",
    },
    "apt": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_APT",
    },
    "aptdownloader": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_APT_DOWNLOADER",
    },
    "configurator": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_CONFIGURATOR",
    },
    "data-encryption-aes256cbc-sample": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_DATA_ENCRYPTION_AES256CBC_SAMPLE",
    },
    "db2-driver-installer": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_DB2_DRIVER_INSTALLER",
    },
    "docker-compose-air-gapper": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_DOCKER_COMPOSE_AIR_GAPPER",
    },
    "dockerhub-util": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_DOCKERHUB_UTIL",
    },
    "entity-search-web-app": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_ENTITY_SEARCH_WEB_APP",
    },
    "entity-search-web-app-console": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_ENTITY_SEARCH_WEB_APP_CONSOLE",
    },
    "file-loader": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_FILE_LOADER",
    },
    "g2command": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_G2COMMAND",
    },
    "g2configtool": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_G2CONFIGTOOL",
    },
    "g2loader": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_G2LOADER",
    },
    "ibm-db2": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_IBM_DB2",
    },
    "init-container": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_INIT_CONTAINER",
    },
    "init-database": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_INIT_DATABASE",
    },
    "init-postgresql": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_INIT_POSTGRESQL",
    },
    "init-mysql": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_INIT_MYSQL",
    },
    "jupyter": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_JUPYTER",
    },
    "phppgadmin": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_PHPPGADMIN",
    },
    "postgresql-client": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_POSTGRESQL_CLIENT",
    },
    "python-demo": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_PYTHON_DEMO",
    },
    "redoer": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_REDOER",
    },
    "resolver": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_RESOLVER",
    },
    "risk-score-calculator": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_RISK_SCORE_CALCULATOR",
    },
    "senzing-api-server": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_SENZING_API_SERVER",
    },
    "senzing-base": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_SENZING_BASE",
    },
    "senzing-console": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_SENZING_CONSOLE",
    },
    "senzing-console-slim": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_SENZING_CONSOLE_SLIM",
    },
    "senzing-listener": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_SENZING_LISTENER",
    },
    "senzing-poc-server": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_SENZING_POC_SERVER",
    },
    "senzing-tools": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_SENZING_TOOLS",
    },
    "senzingapi-runtime": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_SENZINGAPI_RUNTIME",
    },
    "senzingapi-tools": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_SENZINGAPI_TOOLS",
    },
    "serve-chat": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_SERVE_CHAT",
    },
    "serve-grpc": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_SERVE_GRPC",
    },
    "sshd": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_SSHD",
    },
    "stream-loader": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_STREAM_LOADER",
    },
    "stream-logger": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_STREAM_LOGGER",
    },
    "stream-producer": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_STREAM_PRODUCER",
    },
    "web-app-demo": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_WEB_APP_DEMO",
    },
    "xterm": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_XTERM",
    },
    "yum": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_YUM",
    },
    "yumdownloader": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_YUM_DOWNLOADER",
    },
    "x-bitnami-shell": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_BITNAMI_SHELL",
        "image": "bitnami/bitnami-shell",
        "version": "11-debian-11-r136",
    },
    "x-busybox": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_BUSYBOX",
        "image": "busybox",
        "version": "1.36.1",
    },
    "x-confluentinc-cp-kafka": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_CONFLUENTINC_CP_KAFKA",
        "image": "confluentinc/cp-kafka",
        "version": "7.5.3",
    },
    "x-elasticsearch": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_ELASTICSEARCH",
        "image": "elasticsearch",
        "version": "8.11.3",
    },
    "x-ibmcom-db2": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_IBMCOM_DB2",
        "image": "ibmcom/db2",
        "version": "11.5.8.0",
    },
    "x-kafdrop": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_OBSIDIANDYNAMICS_KAFDROP",
        "image": "obsidiandynamics/kafdrop",
        "version": "4.0.0",
    },
    "x-kafka": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_BITNAMI_KAFKA",
        "image": "bitnami/kafka",
        "version": "3.5.2-debian-11-r1",
    },
    "x-kibana": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_KIBANA",
        "image": "kibana",
        "version": "8.11.3",
    },
    "x-logstash": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_LOGSTASH",
        "image": "logstash",
        "version": "8.11.3",
    },
    "x-mssql": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_MSSQL_SERVER",
        "image": "mcr.microsoft.com/mssql/server",
        "url-versions": "https://mcr.microsoft.com/v2/mssql/server/tags/list",
        "version": "2019-GA-ubuntu-16.04",
    },
    "x-mssql-tools": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_MSSQL_TOOLS",
        "image": "mcr.microsoft.com/mssql-tools",
        "reference-url": "https://hub.docker.com/_/microsoft-mssql-tools",
        "version": "latest",
    },
    "x-mysql": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_BITNAMI_MYSQL",
        "image": "bitnami/mysql",
        "version": "8.2.0-debian-11-r4",
    },
    "x-mysql-deprecated": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_MYSQL",
        "image": "bitnami/mysql",
        "version": "8.2.0-debian-11-r4",
    },
    "x-mysql-client": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_AREY_MYSQL_CLIENT",
        "image": "arey/mysql-client",
        "version": "latest",
    },
    "x-nginx": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_BITNAMI_NGINX",
        "image": "bitnami/nginx",
        "version": "1.25.3-debian-11-r4",
    },
    "x-nginx-ingress-controller": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_BITNAMI_NGINX_INGRESS_CONTROLLER",
        "image": "bitnami/nginx-ingress-controller",
        "version": "1.9.1-debian-11-r0",
    },
    "x-pgadmin": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_DPAGE_PGADMIN4",
        "image": "dpage/pgadmin4",
        "version": "8.2",
    },
    "x-phpmyadmin": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_BITNAMI_PHPMYADMIN",
        "image": "bitnami/phpmyadmin",
        "version": "5.2.1-debian-11-r128",
    },
    "x-portainer": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_PORTAINER",
        "image": "portainer/portainer",
        "version": "1.25.0",
    },
    "x-portainer-ce": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_PORTAINER_CE",
        "image": "portainer/portainer-ce",
        "version": "2.19.4",
    },
    "x-postgres": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_BITNAMI_POSTGRESQL",
        "image": "bitnami/postgresql",
        "version": "16.0.0-debian-11-r10",
    },
    "x-rabbitmq": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_BITNAMI_RABBITMQ",
        "image": "bitnami/rabbitmq",
        "version": "3.12.12-debian-11-r3",
    },
    "x-sqlite-web": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_SQLITE_WEB",
        "image": "coleifer/sqlite-web",
        "version": "latest",
    },
    "x-swagger-ui": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_SWAGGERAPI_SWAGGER_UI",
        "image": "swaggerapi/swagger-ui",
        "version": "v5.11.0",
    },
    "x-zookeeper": {
        "environment_variable": "SENZING_DOCKER_IMAGE_VERSION_BITNAMI_ZOOKEEPER",
        "image": "bitnami/zookeeper",
        "version": "3.9.1-debian-11-r5",
    },
}
# -----------------------------------------------------------------------------
# Define argument parser
# -----------------------------------------------------------------------------


def get_parser():
    """Parse commandline arguments."""

    subcommands = {
        "print-active-image-names": {
            "help": "Print image names hosted on DockerHub.",
            "argument_aspects": ["common", "print"],
            "arguments": {},
        },
        "print-image-names": {
            "help": "Print image names used in Senzing demonstrations.",
            "argument_aspects": ["common"],
            "arguments": {},
        },
        "print-latest-versions": {
            "help": "Print latest versions of Docker images.",
            "argument_aspects": ["common"],
            "arguments": {},
        },
        "sleep": {
            "help": "Do nothing but sleep. For Docker testing.",
            "arguments": {
                "--sleep-time-in-seconds": {
                    "dest": "sleep_time_in_seconds",
                    "metavar": "SENZING_SLEEP_TIME_IN_SECONDS",
                    "help": "Sleep time in seconds. DEFAULT: 0 (infinite)",
                },
            },
        },
        "version": {
            "help": "Print version of program.",
        },
        "docker-acceptance-test": {
            "help": "For Docker acceptance testing.",
        },
    }

    # Define argument_aspects.

    argument_aspects = {
        "common": {
            "--debug": {
                "dest": "debug",
                "action": "store_true",
                "help": "Enable debugging. (SENZING_DEBUG) Default: False",
            },
            "--dockerhub-api-endpoint-v2": {
                "dest": "dockerhub_api_endpoint_v2",
                "metavar": "SENZING_DOCKERHUB_API_ENDPOINT_V2",
                "help": "Dockerhub API endpoint Version 2",
            },
        },
        "print": {
            "--print-format": {
                "dest": "print_format",
                "metavar": "SENZING_PRINT_FORMAT",
                "help": "Format of output. Default: '{0}'",
            },
        },
    }

    # Augment "subcommands" variable with arguments specified by aspects.

    for subcommand_value in subcommands.values():
        if "argument_aspects" in subcommand_value:
            for aspect in subcommand_value["argument_aspects"]:
                if "arguments" not in subcommand_value:
                    subcommand_value["arguments"] = {}
                arguments = argument_aspects.get(aspect, {})
                for argument, argument_value in arguments.items():
                    subcommand_value["arguments"][argument] = argument_value

    parser = argparse.ArgumentParser(
        description="Reports from DockerHub. For more information, see https://github.com/Senzing/dockerhub-util"
    )
    subparsers = parser.add_subparsers(
        dest="subcommand", help="Subcommands (SENZING_SUBCOMMAND):"
    )

    for subcommand_key, subcommand_values in subcommands.items():
        subcommand_help = subcommand_values.get("help", "")
        subcommand_arguments = subcommand_values.get("arguments", {})
        subparser = subparsers.add_parser(subcommand_key, help=subcommand_help)
        for argument_key, argument_values in subcommand_arguments.items():
            subparser.add_argument(argument_key, **argument_values)

    return parser


# -----------------------------------------------------------------------------
# Message handling
# -----------------------------------------------------------------------------

# 1xx Informational (i.e. logging.info())
# 3xx Warning (i.e. logging.warning())
# 5xx User configuration issues (either logging.warning() or logging.err() for Client errors)
# 7xx Internal error (i.e. logging.error for Server errors)
# 9xx Debugging (i.e. logging.debug())


MESSAGE_INFO = 100
MESSAGE_WARN = 300
MESSAGE_ERROR = 700
MESSAGE_DEBUG = 900

MESSAGE_DICTIONARY = {
    "100": "senzing-" + SENZING_PRODUCT_ID + "{0:04d}I",
    "292": "Configuration change detected.  Old: {0} New: {1}",
    "293": "For information on warnings and errors, see https://github.com/Senzing/dockerhub-util",
    "294": "Version: {0}  Updated: {1}",
    "295": "Sleeping infinitely.",
    "296": "Sleeping {0} seconds.",
    "297": "Enter {0}",
    "298": "Exit {0}",
    "299": "{0}",
    "300": "senzing-" + SENZING_PRODUCT_ID + "{0:04d}W",
    "499": "{0}",
    "500": "senzing-" + SENZING_PRODUCT_ID + "{0:04d}E",
    "696": "Bad SENZING_SUBCOMMAND: {0}.",
    "697": "No processing done.",
    "698": "Program terminated with error.",
    "699": "{0}",
    "700": "senzing-" + SENZING_PRODUCT_ID + "{0:04d}E",
    "899": "{0}",
    "900": "senzing-" + SENZING_PRODUCT_ID + "{0:04d}D",
    "901": "In repository '{0}', Non-semantic-version {1}",
    "998": "Debugging enabled.",
    "999": "{0}",
}


def message(index, *args):
    """Return an instantiated message."""
    index_string = str(index)
    template = MESSAGE_DICTIONARY.get(
        index_string, "No message for index {0}.".format(index_string)
    )
    return template.format(*args)


def message_generic(generic_index, index, *args):
    """Return a formatted message."""
    return "{0} {1}".format(message(generic_index, index), message(index, *args))


def message_info(index, *args):
    """Return an info message."""
    return message_generic(MESSAGE_INFO, index, *args)


def message_warning(index, *args):
    """Return a warning message."""
    return message_generic(MESSAGE_WARN, index, *args)


def message_error(index, *args):
    """Return an error message."""
    return message_generic(MESSAGE_ERROR, index, *args)


def message_debug(index, *args):
    """Return a debug message."""
    return message_generic(MESSAGE_DEBUG, index, *args)


def get_exception():
    """Get details about an exception."""
    exception_type, exception_object, traceback = sys.exc_info()
    frame = traceback.tb_frame
    line_number = traceback.tb_lineno
    filename = frame.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, line_number, frame.f_globals)
    return {
        "filename": filename,
        "line_number": line_number,
        "line": line.strip(),
        "exception": exception_object,
        "type": exception_type,
        "traceback": traceback,
    }


# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------


def get_configuration(subcommand, args):
    """Order of precedence: CLI, OS environment variables, INI file, default."""
    result = {}

    # Copy default values into configuration dictionary.

    for key, value in list(CONFIGURATION_LOCATOR.items()):
        result[key] = value.get("default", None)

    # "Prime the pump" with command line args. This will be done again as the last step.

    for key, value in list(args.__dict__.items()):
        new_key = key.format(subcommand.replace("-", "_"))
        if value:
            result[new_key] = value

    # Copy OS environment variables into configuration dictionary.

    for key, value in list(CONFIGURATION_LOCATOR.items()):
        os_env_var = value.get("env", None)
        if os_env_var:
            os_env_value = os.getenv(os_env_var, None)
            if os_env_value:
                result[key] = os_env_value

    # Copy 'args' into configuration dictionary.

    for key, value in list(args.__dict__.items()):
        new_key = key.format(subcommand.replace("-", "_"))
        if value:
            result[new_key] = value

    # Add program information.

    result["program_version"] = __version__
    result["program_updated"] = __updated__

    # Special case: subcommand from command-line

    if args.subcommand:
        result["subcommand"] = args.subcommand

    # Special case: Change boolean strings to booleans.

    booleans = [
        "debug",
    ]
    for boolean in booleans:
        boolean_value = result.get(boolean)
        if isinstance(boolean_value, str):
            boolean_value_lower_case = boolean_value.lower()
            if boolean_value_lower_case in ["true", "1", "t", "y", "yes"]:
                result[boolean] = True
            else:
                result[boolean] = False

    # Special case: Change integer strings to integers.

    integers = ["sleep_time_in_seconds"]
    for integer in integers:
        integer_string = result.get(integer)
        result[integer] = int(integer_string)

    return result


def validate_configuration(config):
    """Check aggregate configuration from commandline options, environment variables, config files, and defaults."""

    user_warning_messages = []
    user_error_messages = []

    # Perform subcommand specific checking.

    subcommand = config.get("subcommand")

    if subcommand in ["comments"]:
        if not config.get("github_access_token"):
            user_error_messages.append(message_error(701))

    # Log warning messages.

    for user_warning_message in user_warning_messages:
        logging.warning(user_warning_message)

    # Log error messages.

    for user_error_message in user_error_messages:
        logging.error(user_error_message)

    # Log where to go for help.

    if len(user_warning_messages) > 0 or len(user_error_messages) > 0:
        logging.info(message_info(293))

    # If there are error messages, exit.

    if len(user_error_messages) > 0:
        exit_error(697)


def redact_configuration(config):
    """Return a shallow copy of config with certain keys removed."""
    result = config.copy()
    for key in KEYS_TO_REDACT:
        try:
            result.pop(key)
        except Exception:
            pass
    return result


# -----------------------------------------------------------------------------
# Class DockerHubClient
# Inspired by https://github.com/amalfra/docker-hub/blob/master/src/libs/docker_hub_client.py
# -----------------------------------------------------------------------------


class DockerHubClient:
    """Wrapper to communicate with docker hub API"""

    def __init__(self, config):
        self.auth_token = config.get("auth_token")
        self.dockerhub_api_endpoint_v2 = config.get("dockerhub_api_endpoint_v2")
        self.valid_methods = ["GET", "POST"]

    def do_request(self, url, method="GET", data=None):
        """Make an HTTP request."""
        result = {}
        if not data:
            data = {}
        if method not in self.valid_methods:
            raise ValueError("Invalid HTTP request method")
        headers = {"Content-type": "application/json"}
        if self.auth_token:
            headers["Authorization"] = "JWT " + self.auth_token
        request_method = getattr(requests, method.lower())
        if len(data) > 0:
            data = json.dumps(data, indent=2, sort_keys=True)
            response = request_method(url, data, headers=headers)
        else:
            response = request_method(url, headers=headers)
        if response.status_code == 200:
            result = json.loads(response.content.decode())
        return result

    def get_repositories(self, organization):
        """Return a list of repositories."""
        url = "{0}/repositories/{1}/?page_size=200".format(
            self.dockerhub_api_endpoint_v2, organization
        )
        return self.do_request(url)

    def get_repository_tags(self, organization, repository_name):
        """Return a list repository tags for a repository."""
        url = "{0}/repositories/{1}/{2}/tags".format(
            self.dockerhub_api_endpoint_v2, organization, repository_name
        )
        return self.do_request(url)


# -----------------------------------------------------------------------------
# Utility functions
# -----------------------------------------------------------------------------


def create_signal_handler_function(args):
    """Tricky code.  Uses currying technique. Create a function for signal handling.
    that knows about "args".
    """

    def result_function(signal_number, frame):
        logging.info(message_info(298, args))
        logging.debug(message_debug(901, signal_number, frame))
        sys.exit(0)

    return result_function


def bootstrap_signal_handler(signal_number, frame):
    """Exit on signal error."""
    logging.debug(message_debug(901, signal_number, frame))
    sys.exit(0)


def entry_template(config):
    """Format of entry message."""
    debug = config.get("debug", False)
    config["start_time"] = time.time()
    if debug:
        final_config = config
    else:
        final_config = redact_configuration(config)
    config_json = json.dumps(final_config, sort_keys=True)
    return message_info(297, config_json)


def exit_template(config):
    """Format of exit message."""
    debug = config.get("debug", False)
    stop_time = time.time()
    config["stop_time"] = stop_time
    config["elapsed_time"] = stop_time - config.get("start_time", stop_time)
    if debug:
        final_config = config
    else:
        final_config = redact_configuration(config)
    config_json = json.dumps(final_config, sort_keys=True)
    return message_info(298, config_json)


def exit_error(index, *args):
    """Log error message and exit program."""
    logging.error(message_error(index, *args))
    logging.error(message_error(698))
    sys.exit(1)


def exit_silently():
    """Exit program."""
    sys.exit(0)


# -----------------------------------------------------------------------------
# Helper functions
# -----------------------------------------------------------------------------


def max_version(versions):
    """Return most recent (highest) version."""

    result = Version("0.0.0")
    for version in versions:
        version_parsed = Version(version)
        if version_parsed > result:
            result = version_parsed
    return result


def redacted(key):
    """Determine if a key is redacted."""

    for redact in REDACT_VERSIONS:
        if key.startswith(redact):
            return True
    return False


def find_latest_version(version_list):
    """Return the latest version after redacting the version_list."""

    # TODO: Perhaps improve with https://pypi.org/project/semver/
    return max_version([x for x in version_list if not redacted(x)])


def get_active_image_names(config):
    """Get the latest version of Docker images."""

    result = []
    organization = config.get("dockerhub_organization")
    dockerhub_client = DockerHubClient(config)
    response = dockerhub_client.get_repositories(organization)
    result = response.get("results", result)
    return result


def get_latest_versions(config, dockerhub_repositories):
    """Get the latest version of Docker images."""

    result = []
    organization_default = config.get("dockerhub_organization")
    dockerhub_client = DockerHubClient(config)

    for key, value in dockerhub_repositories.items():
        organization = value.get("organization", organization_default)
        latest_version = value.get("version")
        if not latest_version:
            repository_name = value.get("repository", key)
            response = dockerhub_client.get_repository_tags(
                organization, repository_name
            )
            response_results = response.get("results")
            version_tags = [x.get("name") for x in response_results]
            try:
                latest_version = find_latest_version(version_tags)
            except Exception as err:
                logging.error(message_error(901, repository_name, err))
                continue

        result.append(
            "export {0}={1}".format(value.get("environment_variable"), latest_version)
        )

    result.sort()
    return result


def get_image_names(dockerhub_repositories):
    """Get Docker images names from DockerHub."""

    result = {}
    for key, value in dockerhub_repositories.items():
        # Skip deprecated keys.

        if "deprecated" in key:
            continue

        # Add to result.

        if "image" in value:
            image_name = value.get("image")
        else:
            image_name = "senzing/{0}".format(key)

        result[image_name] = {"environment_variable": value.get("environment_variable")}

    return result


# -----------------------------------------------------------------------------
# do_* functions
#   Common function signature: do_XXX(args)
# -----------------------------------------------------------------------------


def do_docker_acceptance_test(subcommand, args):
    """For use with Docker acceptance testing."""

    # Get context from CLI, environment variables, and ini files.

    config = get_configuration(subcommand, args)

    # Prolog.

    logging.info(entry_template(config))

    # Epilog.

    logging.info(exit_template(config))


def do_print_image_names(subcommand, args):
    """Do a task."""

    # Get context from CLI, environment variables, and ini files.

    config = get_configuration(subcommand, args)

    # Prolog.

    logging.info(entry_template(config))

    # Do work.

    response = get_image_names(DOCKERHUB_REPOSITORIES_FOR_LATEST)

    response_json = json.dumps(response, sort_keys=True, indent=4)
    print(response_json)

    # Epilog.

    logging.info(exit_template(config))


def do_print_active_image_names(subcommand, args):
    """Do a task."""

    # Get context from CLI, environment variables, and ini files.

    config = get_configuration(subcommand, args)

    # Prolog.

    logging.info(entry_template(config))

    # Pull variables from config.

    print_format = config.get("print_format")

    # Do work.

    response = get_active_image_names(config)

    # Sort response.

    repositories = []
    for item in response:
        repositories.append("{0}/{1}".format(item.get("namespace"), item.get("name")))
    repositories.sort()
    for repository in repositories:
        print(print_format.format(repository))

    # Epilog.

    logging.info(exit_template(config))


def do_print_latest_versions(subcommand, args):
    """Do a task."""

    # Get context from CLI, environment variables, and ini files.

    config = get_configuration(subcommand, args)

    # Prolog.

    logging.info(entry_template(config))

    # Do work.

    response = get_latest_versions(config, DOCKERHUB_REPOSITORIES_FOR_LATEST)

    print("#!/usr/bin/env bash")
    print("")
    print(
        "# Generated on {0} by https://github.com/Senzing/dockerhub-util dockerhub-util.py version: {1} update: {2}".format(
            date.today(), config.get("program_version"), config.get("program_updated")
        )
    )
    print("")

    for line in response:
        print(line)

    # Epilog.

    logging.info(exit_template(config))


def do_sleep(subcommand, args):
    """Sleep.  Used for debugging."""

    # Get context from CLI, environment variables, and ini files.

    config = get_configuration(subcommand, args)

    # Prolog.

    logging.info(entry_template(config))

    # Pull values from configuration.

    sleep_time_in_seconds = config.get("sleep_time_in_seconds")

    # Sleep.

    if sleep_time_in_seconds > 0:
        logging.info(message_info(296, sleep_time_in_seconds))
        time.sleep(sleep_time_in_seconds)

    else:
        sleep_time_in_seconds = 3600
        while True:
            logging.info(message_info(295))
            time.sleep(sleep_time_in_seconds)

    # Epilog.

    logging.info(exit_template(config))


def do_version(subcommand, args):
    """Log version information."""

    logging.info(message_info(294, __version__, __updated__))
    logging.debug(message_debug(902, subcommand, args))


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


if __name__ == "__main__":
    # Configure logging. See https://docs.python.org/2/library/logging.html#levels

    LOG_LEVEL_MAP = {
        "notset": logging.NOTSET,
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "fatal": logging.FATAL,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL,
    }

    LOG_LEVEL_PARAMETER = os.getenv("SENZING_LOG_LEVEL", "info").lower()
    LOG_LEVEL = LOG_LEVEL_MAP.get(LOG_LEVEL_PARAMETER, logging.INFO)
    logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)
    logging.debug(message_debug(998))

    # Trap signals temporarily until args are parsed.

    signal.signal(signal.SIGTERM, bootstrap_signal_handler)
    signal.signal(signal.SIGINT, bootstrap_signal_handler)

    # Parse the command line arguments.

    SUBCOMMAND = os.getenv("SENZING_SUBCOMMAND", None)
    PARSER = get_parser()
    if len(sys.argv) > 1:
        ARGS = PARSER.parse_args()
        SUBCOMMAND = ARGS.subcommand
    elif SUBCOMMAND:
        ARGS = argparse.Namespace(subcommand=SUBCOMMAND)
    else:
        PARSER.print_help()
        if len(os.getenv("SENZING_DOCKER_LAUNCHED", "")) > 0:
            SUBCOMMAND = "sleep"
            ARGS = argparse.Namespace(subcommand=SUBCOMMAND)
            do_sleep(SUBCOMMAND, ARGS)
        exit_silently()

    # Catch interrupts. Tricky code: Uses currying.

    SIGNAL_HANDLER = create_signal_handler_function(ARGS)
    signal.signal(signal.SIGINT, SIGNAL_HANDLER)
    signal.signal(signal.SIGTERM, SIGNAL_HANDLER)

    # Transform subcommand from CLI parameter to function name string.

    SUBCOMMAND_FUNCTION_NAME = "do_{0}".format(SUBCOMMAND.replace("-", "_"))

    # Test to see if function exists in the code.

    if SUBCOMMAND_FUNCTION_NAME not in globals():
        logging.warning(message_warning(696, SUBCOMMAND))
        PARSER.print_help()
        exit_silently()

    # Tricky code for calling function based on string.

    globals()[SUBCOMMAND_FUNCTION_NAME](SUBCOMMAND, ARGS)
