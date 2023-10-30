
from pydantic import BaseModel
from typing_extensions import List


# Paraphrase
class RephraseItem(BaseModel):
    """BaseModel for Rephrase"""
    input_text: str

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

# Summary


class SummarizeItem(BaseModel):
    """BaseModel for Summarize"""
    input_text: str 

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


# Change of Tone


class ChangeToneItem(BaseModel):
    """BaseModel for Change of Tone"""
    input_text : str 
    tone_description : str 

    class Config:
        """Config"""

        schema_extra={
            "examples" : [
                {
                    "input_text" : """E-commerce platform Shopify is suing a 'John Doe' defendant for sending numerous false copyright complaints. The DMCA takedown notices have targeted a variety of vendors, who had their legitimate products taken offline as a result of the fraudulent actions. In addition, these vendors risked losing their entire accounts due to multiple false claims.

shopifyThe DMCA takedown process gives copyright holders the option to remove infringing content from the web.

It's a powerful, widely-used tool that takes millions of URLs and links offline every day. This often happens for a good reason, but some takedown efforts are questionable.""",
                    "tone_description" : "As an Engagement Letter Law Professional who is about to write a real state contract"
                }
            ]
        }

# Chat 


class ChatItem(BaseModel):
    """BaseModel for Chat"""
    session_id : str 
    chat_history : List
    user_query : str

    class Config:
        """Config"""

        schema_extra={
            "examples" : [
                {
                    "session_id" : "123456",    
                    "chat_history" : [ 
                        ["Hi assistant", "Hi, I'am an AI Assistant. How can I help you?"],
                        ["My name is Carlomagno, could you remember it?", "Sure, I'll remember it."]
                        ],
                    "user_query" : "Can you recall what is my name?"                    
                }
            ]
        }