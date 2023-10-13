"""Retriever and vector store"""
if True:
    import sys

    sys.path.append("../")
import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings import BedrockEmbeddings
from src.utils.open_search_vector_search_cs import OpenSearchVectorSearchCS
from src.utils.config import load_config
import logging
import boto3


class Retriever:
    """Retriever class"""

    def __init__(self, debug=False):
        """Retriever class"""
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

        # Vector Store Init
        self.vector_store = OpenSearchVectorSearchCS(
            opensearch_url=f"https://{ os.getenv('OPENSEARCH_HOST') }:{ os.getenv('OPENSEARCH_PORT') }",
            embedding_function=embedding_function,
            http_auth=(os.getenv("OPENSEARCH_USER"),
                       os.getenv("OPENSEARCH_PWD")),
            index_name=self.index_name,
            use_ssl=True,
            verify_certs=False,
            ssl_assert_hostname=False,
            ssl_show_warn=False,
        )

        # DB Client
        self.client = self.vector_store.client

    def __call__(self, session_id):
        """Return retriever"""
        return self.vector_store.as_retriever(
            search_kwargs={
                "search_type": "script_scoring",
                "pre_filter": {
                    "bool": {"filter": {"term": {"metadata.session_id": session_id}}}
                },
            }
        )

    def store_document(self, docs: list, session_id: str, replace_docs: bool = False):
        """add session_id to docs in docs_lst -> store in chroma"""

        # Adding session as metadata for each piece of document
        for doc in docs:
            doc.metadata["session_id"] = session_id

        if replace_docs:
            # Search documents
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
            logging.info(delete_response)

        # Store in vector store
        self.vector_store.add_documents(documents=docs)
