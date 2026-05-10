import yaml

from pathlib import Path


# ---------------------------------------------------
# Base Config Directory
# ---------------------------------------------------

CONFIG_DIR = Path(
    "config"
)


# ---------------------------------------------------
# YAML Loader
# ---------------------------------------------------

def load_yaml_config(
    filename: str,
):

    config_path = (
        CONFIG_DIR / filename
    )

    with open(
        config_path,
        "r",
        encoding="utf-8",
    ) as file:

        return yaml.safe_load(
            file
        )


# ---------------------------------------------------
# Shared Config Objects
# ---------------------------------------------------

AGENT_CONFIG = (
    load_yaml_config(
        "agents.yaml"
    )
)

ROUTING_CONFIG = (
    load_yaml_config(
        "routing.yaml"
    )
)

SETTINGS_CONFIG = (
    load_yaml_config(
        "settings.yaml"
    )
)