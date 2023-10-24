from fastapi_serverless_app import app
from fastapi.testclient import TestClient

client = TestClient(app)


### Summarize
def test_summarize():
    with TestClient(app) as client:
        response = client.post(
            "/ai_assistant/summarize",
            json={
                "input_text" : """E-commerce platform Shopify is suing a 'John Doe' defendant for sending numerous false copyright complaints. The DMCA takedown notices have targeted a variety of vendors, who had their legitimate products taken offline as a result of the fraudulent actions. In addition, these vendors risked losing their entire accounts due to multiple false claims.

    shopifyThe DMCA takedown process gives copyright holders the option to remove infringing content from the web.

    It's a powerful, widely-used tool that takes millions of URLs and links offline every day. This often happens for a good reason, but some takedown efforts are questionable."""
            }
        )

        print(response.status_code)

        assert response.status_code == 200 # Correct operation


def test_summarize_incorrect_input_value():
    with TestClient(app) as client:
        response = client.post(
            "/ai_assistant/summarize",
            json={
                "input_text" : ["hi", "this", "is", 4]
            }
        )

        print(response)

        assert response.status_code == 422 # Unprocessable Entity with correct key but a non-transformable string format
        

def test_summarize_incorrect_input_key():
    with TestClient(app) as client:
        response = client.post(
            "/ai_assistant/summarize",
            json={
                "other_input_key" : "This is a valid text but no the expected key"
            }
        )

        assert response.status_code == 422 # Unprocessable Entity with incorrect key which is required


def test_summarize_incorrect_multiple_input_with_one_correct_key():
    with TestClient(app) as client:
        response = client.post(
            "/ai_assistant/summarize",
            json={
                "input_text" : "This is a valid text", 
                "input_text_alt" : "This is another valid text that will be ignored"
            }
        )

        print(response)

        assert response.status_code == 200 # Success since it has the correct key and will ignore incorrect ones


def test_summarize_incorrect_multiple_input_with_incorrect_keys():
    with TestClient(app) as client:
        response = client.post(
            "/ai_assistant/summarize",
            json={
                "input_text_incorrect" : "This is a valid text but ignored since key is not the expected", 
                "input_text_alt" : "This is another valid text that also will be ignored"
            }
        )

        print(response)

        assert response.status_code == 422 # Unprocessable Entity since there is no required correct  key


### Rephrase
def test_rephrase():
    with TestClient(app) as client:
        response = client.post(
            "/ai_assistant/rephrase",
            json={
                "input_text" : """E-commerce platform Shopify is suing a 'John Doe' defendant for sending numerous false copyright complaints. The DMCA takedown notices have targeted a variety of vendors, who had their legitimate products taken offline as a result of the fraudulent actions. In addition, these vendors risked losing their entire accounts due to multiple false claims.

    shopifyThe DMCA takedown process gives copyright holders the option to remove infringing content from the web.

    It's a powerful, widely-used tool that takes millions of URLs and links offline every day. This often happens for a good reason, but some takedown efforts are questionable."""
            }
        )

        print(response)

        assert response.status_code == 200 # Correct operation


def test_rephrase_incorrect_input_value():
    with TestClient(app) as client:
        response = client.post(
            "/ai_assistant/rephrase",
            json={
                "input_text" : ["hi", "this", "is", 4]
            }
        )

        print(response)

        assert response.status_code == 422 # Unprocessable Entity with correct key but a non-transformable string format
        

def test_rephrase_incorrect_input_key():
    with TestClient(app) as client:
        response = client.post(
            "/ai_assistant/rephrase",
            json={
                "other_input_key" : "This is a valid text but no the expected key"
            }
        )

        assert response.status_code == 422 # Unprocessable Entity with incorrect key which is required


def test_rephrase_incorrect_multiple_input_with_one_correct_key():
    with TestClient(app) as client:
        response = client.post(
            "/ai_assistant/rephrase",
            json={
                "input_text" : "This is a valid text", 
                "input_text_alt" : "This is another valid text that will be ignored"
            }
        )

        print(response)

        assert response.status_code == 200 # Success since it has the correct key and will ignore incorrect ones


def test_rephrase_incorrect_multiple_input_with_incorrect_keys():
    with TestClient(app) as client:
        response = client.post(
            "/ai_assistant/rephrase",
            json={
                "input_text_incorrect" : "This is a valid text but ignored since key is not the expected", 
                "input_text_alt" : "This is another valid text that also will be ignored"
            }
        )

        print(response)

        assert response.status_code == 422 # Unprocessable Entity since there is no required correct  key
