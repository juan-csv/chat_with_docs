""" FAST API Hubsync AI Assistant Backend """

import aiofiles
import os
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from contextlib import asynccontextmanager
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from base_llm import BaseLLM
from src.conversational_chain import ChatRetrieval
from src.prompts.prompts_template import INIT_QUERY
from src.splitter import Splitter
from src.retriever import Retriever, RetrieverException
from src.base_llm import BaseLLM
from text_analysis_chains import (
    summarize_text, 
    SummarizeException,
    change_of_tone_text,
    ChangeOfToneException, 
    rephrase_text,
    RephraseException,
    parragraph_suggestion,
    ParagraphSuggestionException
)
from src.sugestion_generator import SuggestionGenerator

def instance_chat(debug=False):
    # Instance retriever when app is started
    splitter = Splitter(debug=debug)
    retriever = Retriever(debug=debug)
    base_llm = BaseLLM(debug=debug, streaming=True)
    chat_retrieval = ChatRetrieval(retriever=retriever, base_llm=base_llm)
    suggester = SuggestionGenerator(
        llm=chat_retrieval.llm, type_llm=base_llm.type_llm, debug=debug)
    return splitter, retriever, chat_retrieval, suggester

# Main components of the API
components = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the Conversational Modules:
    splitter, retriever, chat_retrieval, suggester = instance_chat(debug=True)
    components['splitter'] = splitter
    components['retriever'] = retriever
    components['chat_retrieval'] = chat_retrieval
    components['suggester'] = suggester
    yield
    # Clear the resources
    components.clear()

### App Declaration
DOCS_URL = "/swagger/index.html"
app = FastAPI(
    # docs_url=DOCS_URL, 
    lifespan=lifespan
)

### Exceptions definition:
@app.exception_handler(RetrieverException)
async def handle_retriever_exception(_, exc: RetrieverException):
    return JSONResponse(status_code=500, content={"error": str(exc)})


@app.exception_handler(SummarizeException)
async def handle_summary_exception(_, exc:SummarizeException):
    return JSONResponse(status_code=500, content={"error": str(exc)})


@app.exception_handler(RephraseException)
async def handle_rephrase_exception(_, exc:RephraseException):
    return JSONResponse(status_code=500, content={"error": str(exc)})


@app.exception_handler(ChangeOfToneException)
async def handle_change_of_tone_exception(_, exc:ChangeOfToneException):
    return JSONResponse(status_code=500, content={"error": str(exc)})


@app.exception_handler(ParagraphSuggestionException)
async def handle_paragraph_suggestion_exception(_, exc:ParagraphSuggestionException):
    return JSONResponse(status_code=500, content={"error": str(exc)})


### Endpoints: 
# @app.post('/document/upload_document', tags=['documents'])
# async def upload_document_to_db(
#         session_id: str = Form(...),
#         file: UploadFile = File(...)
# ):
#     # TMP file definition 
#     if os.path.exists('tmp') == False:
#         os.mkdir('tmp')
    
#     # File handling
#     tmp_filename = f'{session_id}-{file.filename}.pdf'
#     async with aiofiles.open(f'tmp/{tmp_filename}', 'wb') as out_file:
#         contents = await file.read()
#         await out_file.write(contents)
#     # File processing
#     splitted_docs = components.splitter.process_document(path_file=f'tmp/{tmp_filename}')
#     # Adding document to the OpenSearchServerless DB
#     store = components.retriever.store_document(
#         docs=splitted_docs,
#         session_id=session_id,
#         replace_docs=True
#     )
#     if store:
#         response = {
#             'response': True
#         },  HTTPException(status_code=200)
#     else:
#         response = {
#             'response': False, 
#             'error': 'error' # debug only
#         }, HTTPException(status_code=500)
    
#     return response

# Summary
class SummarizeItem(BaseModel):
    input_text : str 
    
    class Config:
        
        schema_extra = {
            "examples": [
                {
                    "input_text": """E-commerce platform Shopify is suing a 'John Doe' defendant for sending numerous false copyright complaints. The DMCA takedown notices have targeted a variety of vendors, who had their legitimate products taken offline as a result of the fraudulent actions. In addition, these vendors risked losing their entire accounts due to multiple false claims.

shopifyThe DMCA takedown process gives copyright holders the option to remove infringing content from the web.

It's a powerful, widely-used tool that takes millions of URLs and links offline every day. This often happens for a good reason, but some takedown efforts are questionable."""
                }
            ]
        }

@app.post('/ai_assistant/summarize', tags=['assistant'])
async def summarize(
        summarize : SummarizeItem
):
    summary = summarize_text(
        text=summarize.input_text,
        llm=components['chat_retrieval'].llm, 
        verbose=True # Testing Purposes
    )
    return {'response' : summary}, HTTPException(status_code=200)


# Paraphrase
class RephraseItem(BaseModel):
    input_text : str

    class Config:
        
        schema_extra = {
            "examples" : [
                {
                    "input_text" : """E-commerce platform Shopify is suing a 'John Doe' defendant for sending numerous false copyright complaints. The DMCA takedown notices have targeted a variety of vendors, who had their legitimate products taken offline as a result of the fraudulent actions. In addition, these vendors risked losing their entire accounts due to multiple false claims.

shopifyThe DMCA takedown process gives copyright holders the option to remove infringing content from the web.

It's a powerful, widely-used tool that takes millions of URLs and links offline every day. This often happens for a good reason, but some takedown efforts are questionable."""
                }
            ]
        }

@app.post('/ai_assistant/rephrase', tags=['assistant'])
async def rephrase(
        rephrase_item : RephraseItem
):
    rephrase = rephrase_text(
        text=rephrase_item.input_text,
        llm=components['chat_retrieval'].llm, 
        verbose=True # Testing Purposes
    )
    return {'response' : rephrase}, HTTPException(status_code=200)
    

# # Change of Tone
# class ChangeToneItem(BaseModel):
#     input_text : str 
#     tone_description : str 

# @app.post('/ai_assistant/change_tone', tags=['assistant'])
# async def change_of_tone(
#         change_tone_item : ChangeToneItem
# ):
#     changed_tone = change_of_tone_text(
#         text=change_tone_item.input_text,
#         tone_description=change_tone_item.tone_description,
#         llm=components['chat_retrieval'].llm, 
#         verbose=True # Testing Purposes
#     )
#     return {'response' : changed_tone}, HTTPException(status_code=200)
