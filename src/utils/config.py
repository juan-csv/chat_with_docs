import yaml
import os
from pathlib import Path


def load_config(debug=False):
    """Load config file"""
    if debug:
        root_path = Path(__file__).parent.parent.parent
    else:
        root_path = Path("/")

    with open(root_path / "config/config.yaml", mode="r") as fileyaml:
        config = yaml.load(fileyaml, Loader=yaml.FullLoader)

    # load secrets
    secrets = load_secrets(debug)

    # add secrets (dict) to config
    config.update(secrets)

    # set env variables
    set_env_var(config)

    return config


def load_secrets(debug):
    """Load secrets"""
    if debug:
        root_path = Path(__file__).parent.parent.parent
    else:
        root_path = Path("/")

    with open(root_path / "config/secrets.yaml", mode="r") as fileyaml:
        secrets = yaml.load(fileyaml, Loader=yaml.FullLoader)

    return secrets


def set_env_var(config):
    """Set env variables"""
    os.environ['OPENAI_API_KEY'] = config['OPENAI_API_KEY']
    os.environ["OPENSEARCH_HOST"] = config['OPENSEARCH_HOST']
    os.environ["OPENSEARCH_PORT"] = config['OPENSEARCH_PORT']
    os.environ["OPENSEARCH_USER"] = config['OPENSEARCH_USER']
    os.environ["OPENSEARCH_PWD"] = config['OPENSEARCH_PWD']


if __name__ == "__main__":
    config = load_config(debug=True)
    print(config)
