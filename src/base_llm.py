from langchain.chat_models import ChatOpenAI
if True:
    import sys
    sys.path.append("../")
from src.utils.config import load_config


class BaseLLM:
    """Chat retrieval"""

    def __init__(self, debug=False, streaming=False) -> None:
        """Chat retrieval"""
        self.debug = debug
        self.config = load_config(debug=self.debug)

        # Instance LLM
        self.llm = ChatOpenAI(
            temperature=self.config['base_llm']['temperature'],
            model_name=self.config['base_llm']['model_name'],
            streaming=True
        )

    def __call__(self):
        """Return chain"""
        return self.llm
