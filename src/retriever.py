"""Retriever and vector store"""
if True:
    import sys

    sys.path.append("../")
import os
from langchain.embeddings.openai import OpenAIEmbeddings
import boto3
from langchain.embeddings import BedrockEmbeddings
from src.utils.open_search_vector_search_cs import OpenSearchVectorSearchCS
from opensearchpy import RequestsHttpConnection, AWSV4SignerAuth
from opensearchpy.exceptions import NotFoundError
from src.utils.config import load_config
import logging
import boto3
from src.utils.logger import Logger
# set logger
logger = Logger(__name__).get_logger()


class RetrieverException(Exception):
    """Custom Exception class for Retriever Module"""


class Retriever:
    """Retriever class"""

    def __init__(self, debug=False):
        """Retriever class"""
        try:
            self.debug = debug

            # Load config
            self.config = load_config(debug=self.debug)
            self.index_name = self.config['retriever']['opensearch_index_name']
            self.type_llm = self.config['base_llm']['type_llm']

            # Define embedding function
            if self.type_llm == "openai":
                # Instance embedding function
                embedding_function = OpenAIEmbeddings()

            if self.type_llm == "bedrock":
                bedrock_client = boto3.client(
                    "bedrock-runtime",
                    region_name=self.config['bedrock_llm']['region_name'],
                )
                # Instance embedding function
                embedding_function = BedrockEmbeddings(
                    client=bedrock_client,
                    model_id=self.config['bedrock_llm']['embedding_model_name'],
                )

            # Vector Store Init (AWS Based)

            # AWS auth
            service = self.config['retriever']['aws_service']
            region = self.config['retriever']['aws_region']
            credentials = boto3.Session().get_credentials()
            awsauth = AWSV4SignerAuth(credentials, region, service)

            # OpenSearch store
            self.vector_store = OpenSearchVectorSearchCS(
                opensearch_url=f"http://{os.getenv('OPENSEARCH_AWS_HOST')}:{os.getenv('OPENSEARCH_AWS_PORT')}",
                embedding_function=embedding_function,
                http_auth=awsauth,
                index_name=self.index_name,
                use_ssl=True,
                verify_certs=False,
                ssl_assert_hostname=False,
                ssl_show_warn=False,
                connection_class=RequestsHttpConnection,
                timeout=300
            )

            # DB Client
            self.client = self.vector_store.client
        except Exception as error:
            logger.error(f"Error initializing Retriever: {error}")
            raise RetrieverException(
                f"Exception caught in Retriever module - init: {error}"
            )

    def __call__(self, session_id):
        """Return retriever"""
        try:
            return self.vector_store.as_retriever(
                search_kwargs={
                    "search_type": "script_scoring",
                    "pre_filter": {
                        "bool": {"filter": {"term": {"metadata.session_id": session_id}}}
                    },
                }
            )
        except Exception as error:
            raise RetrieverException(
                f"Exception caught in Retriever module - __call__: {error}"
            )

    def ping_document(self, session_id:str):
        """Ping document"""
        response  = self.client.search(
            index = self.index_name,
            body={
                "query": {
                    "bool": {
                        "must": {
                            "match": {
                                "metadata.session_id":  session_id
                                }
                            }
                        }
                    }
                }
        )
        return response


    def store_document(self, docs: list, session_id: str, replace_docs: bool = False):
        """add session_id to docs in docs_lst -> store in OpenSearch"""
        try:
            # Return variable
            completed = False

            # Adding session as metadata for each piece of document
            for doc in docs:
                    doc.metadata["session_id"] = session_id

            # Search documents
            if replace_docs:
                delete_response = self.client.delete_by_query(
                    index=self.index_name,
                    body={
                        "query": {
                            "bool": {
                                "must": {
                                    "match": {
                                        "metadata.session_id":  session_id
                                    }
                                }
                            }
                        }
                    }
                )
                logger.info('Delete documents response: ', delete_response)

                self.vector_store.add_documents(documents=docs)
                
            completed = True
            return completed
        
        except NotFoundError as error: # The exception raised when there is no document with the Session ID provided
            logger.exception('Documents to replace not found - skipping: ', error)
            pass
        
        except Exception as error:
            raise RetrieverException(
                f"Exception caught at Retriever module - store_document: {error}"
            )
