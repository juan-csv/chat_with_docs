"""Retriever and vector store"""
if True:
    import sys

    sys.path.append("../")
import os
import chromadb
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from src.utils.config import load_config


class Retriever:
    """Retriever class"""

    def __init__(self, debug=False):
        """Retriever class"""
        self.debug = debug

        # Load config
        self.config = load_config(debug=self.debug)
        self.collection_name = self.config['retriever']['collection_name']

        # Define vector store connection to the DB
        self.db_client = chromadb.HttpClient(
            host=os.getenv("CHROMADB_HOST"), port=os.getenv("CHROMADB_PORT")
        )

        self.vector_store = Chroma(
            client=self.db_client,
            collection_name= self.collection_name, 
            embedding_function=OpenAIEmbeddings()
        )

    def __call__(self, session_id):
        """Return retriever"""
        return self.vector_store.as_retriever(
            search_type="mmr", search_kwargs={"filter": {"session_id": session_id}}
        )

    def store_document(self, docs: list, session_id: str, replace_docs: bool = False):
        """add session_id to docs in docs_lst -> store in chroma"""

        # Adding session as metadata for each piece of document
        for doc in docs:
            doc.metadata["session_id"] = session_id

        if replace_docs: 
            # Search documents
            to_replace = self.vector_store.get(where={'session_id':session_id})
            print('Documents to replace: ', to_replace)
            # Remove documents
            # TODO

        # Store in vector store
        self.vector_store.add_documents(documents=docs)
