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
