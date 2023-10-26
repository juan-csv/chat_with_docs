import yaml
import os
from pathlib import Path
import boto3
from botocore.exceptions import ClientError
from src.utils.logger import Logger
import json

# set logger
logger = Logger(__name__).get_logger()


def load_config(debug=False):
    """Load config file"""
    if debug:
        root_path = Path(__file__).parent.parent.parent
    else:
        root_path = Path("/")

    with open(root_path / "config/config.yaml", mode="r") as fileyaml:
        config = yaml.load(fileyaml, Loader=yaml.FullLoader)

    # load secrets
    secrets = load_secrets(debug, config)

    # add secrets (dict) to config
    config.update(secrets)

    # set env variables
    set_env_var(config)

    return config


def load_secrets(debug, config):
    """Load secrets"""
    try:  # to get credentials AWS
        secrets = get_secrets_from_aws(config)
        logger.info("Load secrets from AWS")

    except:  # to get credentials from local
        secrets = get_secrets_from_local(debug)
        logger.info("Load secrets from local")

    return secrets


def get_secrets_from_local(debug):
    """Load secrets"""
    if debug:
        root_path = Path(__file__).parent.parent.parent
    else:
        root_path = Path("/")
    with open(root_path / "config/secrets.yaml", mode="r") as fileyaml:
        secrets = yaml.load(fileyaml, Loader=yaml.FullLoader)
    logger.info("Load secrets from local")

    return secrets


def get_secrets_from_aws(config):
    secret_name = config['secret_manager']['secret_name']
    region_name = config['secret_manager']['region_name']

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret_string_json = json.loads(get_secret_value_response['SecretString'])

    # Decrypts secret using the associated KMS key.
    secrets = {}
    secrets['OPENSEARCH_AWS_HOST'] = secret_string_json['OPENSEARCH_AWS_HOST']
    secrets['OPENSEARCH_AWS_PORT'] = secret_string_json['OPENSEARCH_AWS_PORT']

    return secrets


def set_env_var(config):
    """Set env variables"""
    # os.environ['OPENAI_API_KEY'] = config['OPENAI_API_KEY']
    try:
        os.environ['OPENSEARCH_AWS_HOST'] = config['OPENSEARCH_AWS_HOST']
        os.environ['OPENSEARCH_AWS_PORT'] = config['OPENSEARCH_AWS_PORT']
        logger.info("Load secrets from AWS")

    except:
        os.environ['OPENSEARCH_HOST'] = config['OPENSEARCH_HOST']
        os.environ['OPENSEARCH_PORT'] = config['OPENSEARCH_PORT']
        logger.info("Load secrets from local")


if __name__ == "__main__":
    config = load_config(debug=True)
    print(config)
