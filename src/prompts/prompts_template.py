from langchain.prompts.prompt import PromptTemplate

INIT_QUERY = """Create top 3 modifications for improving document and be more secure for the client. 
Provide the sugestion of modifications including the paragraph to modify and the new paragraph modified.
Explain why it's necessary the modification."""


# ---------------------------------------------------------
# ConversationalRetrievalChain
# ---------------------------------------------------------
prompt_template = """Use the following pieces of context to answer the users question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
{context}

Human: {question}"""
CONVERSATIONAL_RETRIEVAL_CHAIN = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)


# ---------------------------------------------------------
# Text Analysis Chains
# ---------------------------------------------------------

summarize_prompt_template = """Summarize the following text. Keep the original language in 
which the text is written.\nText: {text}"""
SUMMARIZE_CHAIN = PromptTemplate.from_template(summarize_prompt_template)

change_of_tone_prompt_template = "Rewrite the following text to match a {tone_description} tone.\nText: {text}"
CHANGE_TONE_CHAIN = PromptTemplate.from_template(change_of_tone_prompt_template)

rephrase_prompt_template = "For the following text, rephrase it.\nText: {text}"
REPHRASE_CHAIN = PromptTemplate.from_template(rephrase_prompt_template)