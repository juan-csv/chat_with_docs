import yaml
import os
from pathlib import Path


def load_config(debug=False):
    """Load config file"""
    if debug:
        root_path = Path(__file__).parent.parent
    else:
        root_path = Path("/")

    with open(root_path / "config/config.yaml", mode="r") as fileyaml:
        config = yaml.load(fileyaml, Loader=yaml.FullLoader)

    # set env variables
    set_env_var(config)

    return config


def set_env_var(config):
    """Set env variables"""
    os.environ['OPENAI_API_KEY'] = config['OPENAI_API_KEY']


if __name__ == "__main__":
    config = load_config(debug=True)
    print(config)
