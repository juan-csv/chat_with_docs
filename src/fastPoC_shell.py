if True:
    import sys
    sys.path.append("../")

from src.conversational_chain import ChatRetrieval
from src.retriever_and_vectorstore import Retriever

# Args
debug = True
path_file = "../docs_example/contract.pdf"

# Instance retriever
retriever = Retriever(debug=debug)
retriever.store_document(path_file=path_file)

# Instance chat retrieval
chat_retrieval = ChatRetrieval(retriever=retriever)

# create loop for chat
while True:
    print("Bot: What is your question?")
    query = input("You: ")

    if query == "exit":
        break

    response = chat_retrieval.run(query=query)
    print(f"Bot: {response}")
