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
            streaming=streaming,
            model_kwargs={'top_p': 0.09}
        )

    def __call__(self):
        """Return chain"""
        return self.llm


if __name__ == "__main__":
    from langchain.prompts import PromptTemplate
    from langchain.chains import LLMChain

    base_llm = BaseLLM(debug=True)
    query = "create history about a wizard"

    prompt = PromptTemplate(
        template="""You are an assiant,
        {query}""",
        input_variables=["query"],
    )

    # llm_chain = LLMChain(
    #     llm=base_llm(), prompt=prompt, llm_kwargs={"temperature": 0.0})
    # llm_chain.run(query=query)
    base_llm.llm.predict(query)
