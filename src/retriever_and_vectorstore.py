"""Retriever and vector store"""
if True:
    import sys
    sys.path.append("../")
from src.utils.config import load_config
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.document_loaders import PDFMinerLoader


class Retriever:
    """Retriever class"""

    def __init__(self, debug=False):
        """Retriever class"""
        self.debug = debug

        # Load config
        self.config = load_config(debug=self.debug)
        # parameters
        self.chunk_size = self.config['retriever']['chunk_size']
        self.chunk_overlap = self.config['retriever']['chunk_overlap']

        # Instance
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
        )

        # define embedding function
        self.embedding_function = OpenAIEmbeddings()
        # Instance vector store
        self.vector_store = Chroma(embedding_function=OpenAIEmbeddings())

    def __call__(self, session_id):
        """Return retriever"""
        return self.vector_store.as_retriever(search_type="mmr",search_kwargs={"filter":{"session_id" : session_id}})

    def store_document(self, path_file, session_id):
        """Read document -> split in chunks -> store vector store"""

        # Load document
        doc = PDFMinerLoader(path_file).load()

        # Split in chunks
        # TODO: remove '5' it's just for debugging
        if self.debug:
            chunks = self.splitter.split_documents(doc)[:5]
        else:
            chunks = self.splitter.split_documents(doc)

        # Add metadata to test search within metadata elements in Chroma
        for doc in chunks: 
            doc.metadata['session_id'] = session_id

        # Store in vector store
        self.vector_store.add_documents(chunks)


if __name__ == "__main__":
    path_file = "../docs_example/contract.pdf"
    retriever = Retriever(debug=True)
    retriever.store_document(path_file=path_file)

    # get similar documents
    query = "What are the title of this document?"
    similar_docs = retriever.vector_store.similarity_search(
        query,
        filter={'session_id':'12345'}
    )
    print('similar docs: ', len(similar_docs))
    if len(similar_docs) > 0:
        print(similar_docs[0].page_content)
