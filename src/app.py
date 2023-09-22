import base64
import os
import tempfile

import langchain
import streamlit as st
from langchain.callbacks.base import BaseCallbackHandler
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from src.conversational_chain import ChatRetrieval
from src.prompts.prompts_template import INIT_QUERY
from src.retriever_and_vectorstore import Retriever
from src.base_llm import BaseLLM


def save_tmp_file(uploaded_file):
    # Define the path where the temporary file will be saved
    temp_dir = tempfile.mkdtemp()

    # Save the uploaded PDF to the temporary directory
    with open(os.path.join(temp_dir, uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())
    return os.path.join(temp_dir, uploaded_file.name)


class StreamHandler(BaseCallbackHandler):
    def __init__(self, container: st.delta_generator.DeltaGenerator, initial_text: str = ""):
        self.container = container
        self.text = initial_text
        self.run_id_ignore_token = None

    def on_llm_start(self, serialized: dict, prompts: list, **kwargs):
        # Workaround to prevent showing the rephrased question as output
        if prompts[0].startswith("Human"):
            self.run_id_ignore_token = kwargs.get("run_id")

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        if self.run_id_ignore_token == kwargs.get("run_id", False):
            return
        self.text += token
        self.container.markdown(self.text)


class PrintRetrievalHandler(BaseCallbackHandler):
    def __init__(self, container):
        self.status = container.status("**Context Retrieval**")

    def on_retriever_start(self, serialized: dict, query: str, **kwargs):
        self.status.write(f"**Question:** {query}")
        self.status.update(label=f"**Context Retrieval:** {query}")

    def on_retriever_end(self, documents, **kwargs):
        for idx, doc in enumerate(documents):
            source = os.path.basename(doc.metadata["source"])
            self.status.write(f"**Document {idx} from {source}**")
            self.status.markdown(doc.page_content)
        self.status.update(state="complete")


def displayPDF(file):
    # Opening file from file path
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    # Embedding PDF in HTML
    pdf_display = F'<embed src="data:application/pdf;base64,{base64_pdf}" width="500" height="600" type="application/pdf">'

    # Displaying File
    st.sidebar.markdown(pdf_display, unsafe_allow_html=True)


@st.cache_resource
def insntance_chat(debug=False):
    # Instance retriever when app is started
    retriever = Retriever(debug=debug)
    base_llm = BaseLLM(debug=debug, streaming=True)
    chat_retrieval = ChatRetrieval(retriever=retriever, base_llm=base_llm)
    return retriever, chat_retrieval


st.set_page_config(page_title="HubSync: AI Assitant")
st.title("HubSync: AI Assitant")
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 700px !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
)


langchain.verbose = True
# Instance chat retrieval
retriever, chat_retrieval = insntance_chat(debug=True)
# set chat history
chat_history = []
# Setup memory for contextual conversation
msgs = StreamlitChatMessageHistory()
# define avatar
avatars = {"human": "user", "ai": "assistant"}


if __name__ == "__main__":

    # File uploader widget
    uploaded_file = st.sidebar.file_uploader("Upload a PDF file", type=["pdf"])

    if not uploaded_file:
        st.info("Please upload PDF documents to continue.")
        st.stop()
    else:
        # check if a file already was uploaded
        if len(msgs.messages) == 0:
            # save as a temporary file
            temp_file_path = save_tmp_file(uploaded_file)
            # save temp_file_path variable
            st.session_state.temp_file_path = temp_file_path

            st.success("File uploaded and saved as a temporary file.")
            st.text("The temporary directory will be removed when the app is closed.")
            # load the file
            with st.spinner("Creating embeddings for document..."):
                retriever.store_document(path_file=temp_file_path)

        # preview the file
        if st.session_state.temp_file_path:
            displayPDF(st.session_state.temp_file_path)

    # show a message if there are no messages
    if len(msgs.messages) == 0:
        # create
        # msgs.clear()
        # add loader message
        with st.spinner("Processing document suggestions..."):
            # run chat retrieval
            # response = chat_retrieval.run(INIT_QUERY)
            response = "Hi"
            # add message to chat history
            msgs.add_ai_message(response)
            # add chat_history
            chat_history.append((INIT_QUERY, response))

    # show chat history
    for msg in msgs.messages:
        st.chat_message(avatars[msg.type]).write(msg.content)

    # When user sends a message
    if user_query := st.chat_input(placeholder="Ask me anything!"):
        # add message to chat history
        st.chat_message("user").write(user_query)
        # add message to message history
        msgs.add_user_message(user_query)

        # run chat retrieval
        with st.chat_message("assistant"):
            # setup callback
            stream_handler = StreamHandler(st.empty())
            retrieval_handler = PrintRetrievalHandler(st.container())
            # run chat retrieval
            response = chat_retrieval.run(
                user_query,
                chat_history=chat_history,
                callbacks=[stream_handler, retrieval_handler])

        # add message to chat history
        msgs.add_ai_message(response)
        # force to respond
        st.chat_message("assistant").write(response)
        # add chat_history
        chat_history.append((user_query, response))
