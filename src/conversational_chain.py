from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI

if True:
    import sys
    sys.path.append("../")

from src.retriever_and_vectorstore import Retriever


class ChatRetrieval:
    """Chat retrieval"""

    def __init__(self, retriever, streaming=False) -> None:
        """Chat retrieval"""

        # Instance retriever
        self.retriever = retriever

        self.debug = self.retriever.debug
        self.config = self.retriever.config

        # Instance variables chat_history
        # TODO: remove and replace as a input
        self.chat_history = []

        # Instance LLM
        self.llm = ChatOpenAI(
            temperature=self.config['conversational_chain']['llm']['temperature'],
            model_name=self.config['conversational_chain']['llm']['model_name'],
            streaming=streaming
        )
        self.llm_condense_question = ChatOpenAI(
            temperature=self.config['conversational_chain']['condense_question_llm']['temperature'],
            model_name=self.config['conversational_chain']['condense_question_llm']['model_name']
        )

        # Create chain
        self.qa = ConversationalRetrievalChain.from_llm(
            self.llm,
            self.retriever(),
            condense_question_llm=self.llm_condense_question,
            # combine_docs_chain_kwargs={"prompt": qa_prompt}
        )

    def run(self, query, chat_history: list = None, callbacks=None):
        """Run chat retrieval"""
        inputs = {
            "question": query,
            "chat_history": self.chat_history
        }

        result = self.qa(
            inputs=inputs,
            callbacks=callbacks
        )

        # update chat history
        self.chat_history.append(
            (query, result["answer"])
        )

        return result["answer"]


if __name__ == "__main__":
    # Args
    debug = True
    query = "What is the contract about??"

    # Instance retriever
    path_file = "../docs_example/contract.pdf"
    retriever = Retriever(debug=debug)
    retriever.store_document(path_file=path_file)

    # Instance chat retrieval
    chat_retrieval = ChatRetrieval(retriever=retriever)

    # Run
    answer = chat_retrieval.run(query=query)
    print(answer)
