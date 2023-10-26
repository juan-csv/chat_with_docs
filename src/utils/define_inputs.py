
from pydantic import BaseModel


# Paraphrase
class RephraseItem(BaseModel):
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
    input_text: str = "This is a text to summarize"

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
