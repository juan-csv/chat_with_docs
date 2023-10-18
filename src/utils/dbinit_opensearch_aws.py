""" Chroma DB script to initialize DB with an empty collection"""

import os
from opensearchpy import OpenSearch, RequestsHttpConnection,AWSV4SignerAuth
import boto3
import time


if True:
    import sys

    sys.path.append("../../")
from src.utils.config import load_config, set_env_var

TARGET_INDEX_NAME = 'hubsync-ai-assistant'
BODY_CREATE_INDEX_DEFAULT = {
        "aliases": {},
        "mappings": {
            "properties": {
                "metadata": {
                    "properties": {
                        "session_id": {
                            "type": "text",
                            "fields": {
                                "keyword": {"type": "keyword", "ignore_above": 256}
                            },
                        },
                        "source": {
                            "type": "text",
                            "fields": {
                                "keyword": {"type": "keyword", "ignore_above": 256}
                            },
                        },
                    }
                },
                "text": {
                    "type": "text",
                    "fields": {"keyword": {"type": "keyword", "ignore_above": 256}},
                },
                "vector_field": {
                    "type": "knn_vector",
                    "dimension": 1536,
                    "method": {
                        "engine": "nmslib",
                        "space_type": "l2",
                        "name": "hnsw",
                        "parameters": {"ef_construction": 512, "m": 16},
                    },
                },
            }
        },
        "settings": {
            "index": {
                "number_of_shards": "1",
                "knn.algo_param": {"ef_search": "512"},
                "knn": "true",
                "number_of_replicas": "1",
            }
        },
    }



def main(debug: bool):
    """Main routine to initialize the AI Assistant database"""
    # loading config file:
    config = load_config(debug=debug)
    print('Config loaded')
    # Setting env var for connection
    set_env_var(config)
    print('ENV set')
    # Create the connection
    host = os.getenv("OPENSEARCH_AWS_HOST")
    port = os.getenv("OPENSEARCH_AWS_PORT")
    print('Connection params: ', host, ' - ', port)

    #aws auth4
    service = 'aoss'
    region = 'us-east-1'
    credentials = boto3.Session().get_credentials()
    awsauth = AWSV4SignerAuth(credentials, region, service)
    # Connect to OpenSearch SERVERLESS AWS
    client = OpenSearch(
        hosts=[{'host': host, 'port': port}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection,
        timeout=300
    )
    print('Client OpenSearch created: ', client)

    # Listing all indices:
    print('Existing Aliases: ', client.indices.get_alias())

    # Check if the target index exists. If so, deletes it:
    if client.indices.exists(
        index=TARGET_INDEX_NAME
    ):
        delete_result = client.indices.delete(
            index=TARGET_INDEX_NAME
        )
        print('Delete Result: ', delete_result)
    
    time.sleep(10)
    # Create an index
    create_result = client.indices.create(
        index=TARGET_INDEX_NAME,
        body=BODY_CREATE_INDEX_DEFAULT
    )
    print('Creation Index Result: ', create_result)


if __name__ == "__main__":
    main(debug=True)
