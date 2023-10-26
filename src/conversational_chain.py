"""Conversational chain"""
from langchain.chains import ConversationalRetrievalChain
if True:
    import sys

    sys.path.append("../")

from src.prompts.prompts_template_bedrock import CONVERSATIONAL_RETRIEVAL_CHAIN_V2
from src.base_llm import BaseLLM, BaseLLMException
from src.retriever import RetrieverException
from langchain.chains.question_answering import load_qa_chain
from src.utils.logger import Logger
# set logger
logger = Logger(__name__).get_logger()

class ChatRetrievalException(Exception): 
    """Custom exception handling for ChatRetrieval module"""

class ChatRetrieval:
    """Chat retrieval"""

    def __init__(self, retriever, base_llm) -> None:
        """Chat retrieval"""
        try:
            # Instance retriever
            self.retriever = retriever

            self.debug = self.retriever.debug
            self.config = self.retriever.config

            # Instance variables chat_history
            self.chat_history = []

            # Instance LLM
            self.llm = base_llm()
        except Exception as error:
            logger.error(f"Error in ChatRetrieval: {error}")
            raise ChatRetrievalException(
                f"Exception caught in ChatRetrieval - init: {error}"
            )

    def run(
        self, query, chat_history: list = None, callbacks=None, session_id: str = ""
    ):
        """Run chat retrieval
        Args:
            query (str): query
            chat_history (list, optional): chat history. Defaults to None. list of tuples (query, answer)
            callbacks ([type], optional): callbacks. Defaults to None.
        Returns:
            str: answer
        """
        try:
            # Create chain
            qa = ConversationalRetrievalChain.from_llm(
                self.llm,
                self.retriever(session_id=session_id),
                verbose=self.debug,
                # condense_question_llm=self.base_llm,
                combine_docs_chain_kwargs={
                    "prompt": CONVERSATIONAL_RETRIEVAL_CHAIN_V2},
            )

            if chat_history is None:
                chat_history = self.chat_history

            inputs = {"question": query, "chat_history": chat_history}

            result = qa(inputs=inputs, callbacks=callbacks)

            # update chat history
            self.chat_history.append((query, result["answer"]))

            return result["answer"]
        
        except Exception as error:
            logger.error(f"Error in ChatRetrieval: {error}")
            raise ChatRetrievalException(
            f"Exception caught in ChatRetrieval module - run: {error}"
        )
        
