"""This module contains utility functions for the chat_with_docs app."""

import os
import tempfile


def save_tmp_file(uploaded_file):
    # Define the path where the temporary file will be saved
    temp_dir = tempfile.mkdtemp()

    # Save the uploaded PDF to the temporary directory
    with open(os.path.join(temp_dir, uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())
    return os.path.join(temp_dir, uploaded_file.name)
