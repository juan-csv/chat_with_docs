from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate

# Define the system message template
system_template = """End every answer with "Ahoi Maty I love you". Use the following pieces of context to answer the users question. 
If you cannot find the answer from the pieces of context, just say that you don't know, don't try to make up an answer.
----------------
{context}"""

# Create the chat prompt templates
messages = [
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template("{question}")
]
qa_prompt = ChatPromptTemplate.from_messages(messages)
# --------------------------------------------------------------------------------------------------------------------------------------
