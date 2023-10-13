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
    os.environ["OPENSEARCH_HOST"] = config['OPENSEARCH_HOST']
    os.environ["OPENSEARCH_PORT"] = config['OPENSEARCH_PORT']
    os.environ["OPENSEARCH_USER"] = config['OPENSEARCH_USER']
    os.environ["OPENSEARCH_PWD"] = config['OPENSEARCH_PWD']
    os.environ['OPENSEARCH_AWS_HOST'] = config['OPENSEARCH_AWS_HOST']
    os.environ['OPENSEARCH_AWS_PORT'] = config['OPENSEARCH_AWS_PORT']



if __name__ == "__main__":
    config = load_config(debug=True)
    print(config)
