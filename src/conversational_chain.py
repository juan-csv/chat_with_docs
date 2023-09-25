"""Conversational chain"""
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI

if True:
    import sys
    sys.path.append("../")

from src.retriever_and_vectorstore import Retriever
from src.prompts.prompts_template import CONVERSATIONAL_RETRIEVAL_CHAIN
from src.base_llm import BaseLLM


class ChatRetrieval:
    """Chat retrieval"""

    def __init__(self, retriever, base_llm, session_id) -> None:
        """Chat retrieval"""

        # Instance retriever
        self.retriever = retriever

        self.debug = self.retriever.debug
        self.config = self.retriever.config

        # Instance variables chat_history
        self.chat_history = []

        # Instance LLM
        self.llm = base_llm()

        self.llm_condense_question = ChatOpenAI(
            temperature=self.config['conversational_chain']['condense_question_llm']['temperature'],
            model_name=self.config['conversational_chain']['condense_question_llm']['model_name']
        )

        # Create chain
        self.qa = ConversationalRetrievalChain.from_llm(
            self.llm,
            self.retriever(session_id=session_id),
            verbose=self.debug,
            # condense_question_llm=self.llm_condense_question,
            combine_docs_chain_kwargs={
                "prompt": CONVERSATIONAL_RETRIEVAL_CHAIN}
        )

    def run(self, query, chat_history: list = None, callbacks=None):
        """Run chat retrieval
        Args:
            query (str): query
            chat_history (list, optional): chat history. Defaults to None. list of tuples (query, answer)
            callbacks ([type], optional): callbacks. Defaults to None.
        Returns:
            str: answer
        """

        if chat_history is None:
            chat_history = self.chat_history

        inputs = {
            "question": query,
            "chat_history": chat_history
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
    base_llm = BaseLLM(debug=debug)
    retriever = Retriever(debug=debug)
    retriever.store_document(path_file=path_file)

    # Instance chat retrieval
    chat_retrieval = ChatRetrieval(retriever=retriever, base_llm=base_llm)

    # Run
    answer = chat_retrieval.run(query=query)
    print(answer)
