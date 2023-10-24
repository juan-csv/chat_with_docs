import yaml
import os
import json
from pathlib import Path
import boto3
from botocore.exceptions import ClientError


def load_secrets_aws():
    secret_name = "test-hubsync"
    region_name = "us-east-1"

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


def load_config(debug=False):
    """Load config file"""
    if debug:
        root_path = Path(__file__).parent.parent.parent
    else:
        root_path = Path("/")

    with open(root_path / "config/config.yaml", mode="r") as fileyaml:
        config = yaml.load(fileyaml, Loader=yaml.FullLoader)

    # load secrets
    secrets = load_secrets_aws()

    # add secrets (dict) to config
    config.update(secrets)

    # set env variables
    set_env_var(config)

    return config


def set_env_var(config):
    """Set env variables"""
    os.environ['OPENSEARCH_AWS_HOST'] = config['OPENSEARCH_AWS_HOST']
    os.environ['OPENSEARCH_AWS_PORT'] = config['OPENSEARCH_AWS_PORT']


if __name__ == "__main__":
    config = load_config(debug=True)
    print(config)
