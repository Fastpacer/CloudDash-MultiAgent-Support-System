import yaml

from pathlib import Path


# ---------------------------------------------------
# Resolve Project Root
# ---------------------------------------------------

BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
    .parent
)

# ---------------------------------------------------
# Config Directory
# ---------------------------------------------------

CONFIG_DIR = (
    BASE_DIR / "app" /"config"
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

    if not config_path.exists():

        raise FileNotFoundError(
            (
                f"YAML config file not found: "
                f"{config_path}"
            )
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