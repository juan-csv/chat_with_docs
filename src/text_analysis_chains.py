"""
Other modules: Summarize, Change of Tone, Rephrase
"""
from langchain.chains import LLMChain
from src.prompts.prompts_template import (
    CHANGE_TONE_CHAIN,
    SUMMARIZE_CHAIN,
    REPHRASE_CHAIN,
    PROMPT_PARRAGRAPH_SUGGESTION
)


def summarize_text(text, llm, verbose: bool = False):
    """
    Summarize text
    """
    summarize_chain = LLMChain(
        llm=llm, output_key="summary", verbose=verbose, prompt=SUMMARIZE_CHAIN
    )
    result = summarize_chain.run(text=text)
    print('Summary result: ', result)
    return result


def change_of_tone_text(text, tone_description, llm, verbose: bool = False):
    """
    Change of tone
    """
    change_tone_chain = LLMChain(
        llm=llm, output_key="changed_tone_text", verbose=verbose, prompt=CHANGE_TONE_CHAIN
    )
    result = change_tone_chain.run(
        tone_description=tone_description, text=text)
    print('Change of tone result: ', result)
    return result


def rephrase_text(text, llm, verbose: bool = False):
    """
    Rephrase
    """
    rephrase_chain = LLMChain(
        llm=llm, output_key="changed_tone_text", verbose=verbose, prompt=REPHRASE_CHAIN
    )
    result = rephrase_chain.run(text=text)
    print('Rephrase result: ', result)
    return result


def parragraph_suggestion(text: str, llm, verbose: bool = False) -> str:
    """
    Suggest a new paragraph
    """
    parragraph_suggestion_chain = LLMChain(
        llm=llm, output_key="suggestion", verbose=verbose, prompt=PROMPT_PARRAGRAPH_SUGGESTION
    )

    result = parragraph_suggestion_chain.run(context=text)
    print('Parragraph suggestion result: ', result)
    return result
