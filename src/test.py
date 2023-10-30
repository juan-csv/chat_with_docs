from app import app
from fastapi.testclient import TestClient

client = TestClient(app)


### Summarize
def test_summarize():
    """Test summarize functionality"""
    with TestClient(app) as client:
        response = client.post(
            "/ai_assistant/summarize",
            json={
                "input_text": """E-commerce platform Shopify is suing a 'John Doe' defendant for sending numerous false copyright complaints. The DMCA takedown notices have targeted a variety of vendors, who had their legitimate products taken offline as a result of the fraudulent actions. In addition, these vendors risked losing their entire accounts due to multiple false claims.

    shopifyThe DMCA takedown process gives copyright holders the option to remove infringing content from the web.

    It's a powerful, widely-used tool that takes millions of URLs and links offline every day. This often happens for a good reason, but some takedown efforts are questionable."""
            },
        )

        print(response.status_code)

        assert response.status_code == 200  # Correct operation


def test_summarize_incorrect_input_value():
    """Test summarize functionality with incorrect input value"""
    with TestClient(app) as client:
        response = client.post(
            "/ai_assistant/summarize", json={"input_text": ["hi", "this", "is", 4]}
        )

        print(response)

        assert (
            response.status_code == 422
        )  # Unprocessable Entity with correct key but a non-transformable string format


def test_summarize_incorrect_input_key():
    """Test summarize functionality with incorrect input key"""
    with TestClient(app) as client:
        response = client.post(
            "/ai_assistant/summarize",
            json={"other_input_key": "This is a valid text but no the expected key"},
        )

        assert (
            response.status_code == 422
        )  # Unprocessable Entity with incorrect key which is required


def test_summarize_incorrect_multiple_input_with_one_correct_key():
    """Test summarize functionality with valid and invalid keys"""
    with TestClient(app) as client:
        response = client.post(
            "/ai_assistant/summarize",
            json={
                "input_text": "This is a valid text",
                "input_text_alt": "This is another valid text that will be ignored",
            },
        )

        print(response)

        assert (
            response.status_code == 200
        )  # Success since it has the correct key and will ignore incorrect ones


def test_summarize_incorrect_multiple_input_with_incorrect_keys():
    """Test summarize functionality with only incorrect keys"""
    with TestClient(app) as client:
        response = client.post(
            "/ai_assistant/summarize",
            json={
                "input_text_incorrect": "This is a valid text but ignored since key is not the expected",
                "input_text_alt": "This is another valid text that also will be ignored",
            },
        )

        print(response)

        assert (
            response.status_code == 422
        )  # Unprocessable Entity since there is no required correct  key


### Rephrase
def test_rephrase():
    """Test rephrase functionality"""
    with TestClient(app) as client:
        response = client.post(
            "/ai_assistant/rephrase",
            json={
                "input_text": """E-commerce platform Shopify is suing a 'John Doe' defendant for sending numerous false copyright complaints. The DMCA takedown notices have targeted a variety of vendors, who had their legitimate products taken offline as a result of the fraudulent actions. In addition, these vendors risked losing their entire accounts due to multiple false claims.

    shopifyThe DMCA takedown process gives copyright holders the option to remove infringing content from the web.

    It's a powerful, widely-used tool that takes millions of URLs and links offline every day. This often happens for a good reason, but some takedown efforts are questionable."""
            },
        )

        print(response)

        assert response.status_code == 200  # Correct operation


def test_rephrase_incorrect_input_value():
    """Test rephrase functionality with an incorrect input value"""
    with TestClient(app) as client:
        response = client.post(
            "/ai_assistant/rephrase", json={"input_text": ["hi", "this", "is", 4]}
        )

        print(response)

        assert (
            response.status_code == 422
        )  # Unprocessable Entity with correct key but a non-transformable string format


def test_rephrase_incorrect_input_key():
    """Test rephrase functionality with an incorrect input key"""
    with TestClient(app) as client:
        response = client.post(
            "/ai_assistant/rephrase",
            json={"other_input_key": "This is a valid text but no the expected key"},
        )

        assert (
            response.status_code == 422
        )  # Unprocessable Entity with incorrect key which is required


def test_rephrase_incorrect_multiple_input_with_one_correct_key():
    """Test rephrase functionality with both incorrect and correct keys"""
    with TestClient(app) as client:
        response = client.post(
            "/ai_assistant/rephrase",
            json={
                "input_text": "This is a valid text",
                "input_text_alt": "This is another valid text that will be ignored",
            },
        )

        print(response)

        assert (
            response.status_code == 200
        )  # Success since it has the correct key and will ignore incorrect ones


def test_rephrase_incorrect_multiple_input_with_incorrect_keys():
    """Test rephrase functionality with all input keys being incorrect"""
    with TestClient(app) as client:
        response = client.post(
            "/ai_assistant/rephrase",
            json={
                "input_text_incorrect": "This is a valid text but ignored since key is not the expected",
                "input_text_alt": "This is another valid text that also will be ignored",
            },
        )

        print(response)

        assert (
            response.status_code == 422
        )  # Unprocessable Entity since there is no required correct  key


### Change of Tone
def test_change_of_tone():
    """Test Change of Tone Functionality"""
    with TestClient(app) as client:
        response = client.post(
            "/ai_assistant/change_of_tone",
            json={
                "input_text": """E-commerce platform Shopify is suing a 'John Doe' defendant for sending numerous false copyright complaints. The DMCA takedown notices have targeted a variety of vendors, who had their legitimate products taken offline as a result of the fraudulent actions. In addition, these vendors risked losing their entire accounts due to multiple false claims.

    shopifyThe DMCA takedown process gives copyright holders the option to remove infringing content from the web.

    It's a powerful, widely-used tool that takes millions of URLs and links offline every day. This often happens for a good reason, but some takedown efforts are questionable.""",
                "tone_description": "As an Engagement Letter Law Professional who is about to write a real state contract",
            },
        )

        print(response)

        assert response.status_code == 200  # Correct operation


def test_change_of_tone_one_incorrect_input_value():
    """Test Change of Tone Functionality with one incorrect value type"""
    with TestClient(app) as client:
        response = client.post(
            "/ai_assistant/change_of_tone",
            json={
                "input_text": ["hi", "this", "is", 4],
                "tone_description": "As a correct input value given",
            },
        )

        print(response)

        assert (
            response.status_code == 422
        )  # Unprocessable Entity with correct key but not correct value


def test_change_of_tone_all_incorrect_input_value():
    """Test Change of Tone Functionality with all incorrect input values"""
    with TestClient(app) as client:
        response = client.post(
            "/ai_assistant/change_of_tone",
            json={
                "input_text": ["hi", "this", "is", 4],
                "tone_description": [
                    "This",
                    "is",
                    "also",
                    "an",
                    "incorrect",
                    "parameter",
                    0,
                ],
            },
        )

        print(response)

        assert (
            response.status_code == 422
        )  # Unprocessable Entity with correct keys but incorrect values


def test_change_of_tone_one_incorrect_input_key():
    """Test change of tone functionality with just one incorrect input key"""
    with TestClient(app) as client:
        response = client.post(
            "/ai_assistant/change_of_tone",
            json={
                "input_key": "This is a valid text without the expected key",
                "other_tone_description": [
                    "This",
                    "is",
                    "a",
                    False,
                    0,
                    "valid",
                    "tone",
                ],
            },
        )

        assert (
            response.status_code == 422
        )  # Unprocessable Entity with one incorrect key and correct value


def test_change_of_tone_all_incorrect_input_key():
    """Test change of tone functionality with all input keys being incorrect"""
    with TestClient(app) as client:
        response = client.post(
            "/ai_assistant/change_of_tone",
            json={
                "other_input_key": "This is a valid text without the expected key",
                "other_tone_description": "This is also a valid tone but not the expected key",
            },
        )

        assert (
            response.status_code == 422
        )  # Unprocessable Entity with all keys incorrect


def test_change_of_tone_correct_keys_with_additional_incorrect_key():
    """Test change of tone functionality with additional incorrect parameters"""
    with TestClient(app) as client:
        response = client.post(
            "/ai_assistant/change_of_tone",
            json={
                "input_text": "This is a valid text",
                "tone_description": "As an Engagement Letter Law Professional who is about to write a real state contract",
                "input_text_alt": "This is another valid text that will be ignored",
            },
        )

        print(response)

        assert (
            response.status_code == 200
        )  # Success since it has the correct key and will ignore incorrect ones


### Chat


def test_chat():
    """Test Chat Functionality"""
    with TestClient(app) as client:
        response = client.post(
            "/ai_assistant/chat",
            json={
                "session_id": "123456",
                "chat_history": [
                    ["Hi assistant", "Hi, I'am an AI Assistant. How can I help you?"],
                    [
                        "My name is Carlomagno, could you remember it?",
                        "Sure, I'll remember it.",
                    ],
                ],
                "user_query": "Can you recall what is my name?",
            },
        )

        print(response)

        assert response.status_code == 200  # Correct operation


def test_chat_one_incorrect_input_value():
    """Test Chat Functionality with one incorrect value type"""
    with TestClient(app) as client:
        response = client.post(
            "/ai_assistant/chat",
            json={
                "session_id": ["This", "session", "id", "is", "Invalid", False, 0],
                "chat_history": [
                    ["Hi assistant", "Hi, I'am an AI Assistant. How can I help you?"],
                    [
                        "My name is Carlomagno, could you remember it?",
                        "Sure, I'll remember it.",
                    ],
                ],
                "user_query": "Can you recall what is my name?",
            },
        )

        print(response)

        assert (
            response.status_code == 422
        )  # Unprocessable Entity with correct key but not correct value


def test_chat_all_incorrect_input_value():
    """Test chat functionality with all incorrect value types"""
    with TestClient(app) as client:
        response = client.post(
            "/ai_assistant/chat",
            json={
                "session_id": ["This", "session", "id", "is", "Invalid", False, 0],
                "chat_history": "This is not expected as chat history",
                "user_query": {"IsThisValid?": False},
            },
        )

        print(response)

        assert (
            response.status_code == 422
        )  # Unprocessable Entity with correct keys but incorrect values


def test_chat_one_incorrect_input_key():
    """Test chat functionality with one incorrect input key"""
    with TestClient(app) as client:
        response = client.post(
            "/ai_assistant/chat",
            json={
                "other_session_id": "123456",
                "chat_history": [
                    ["Hi assistant", "Hi, I'am an AI Assistant. How can I help you?"],
                    [
                        "My name is Carlomagno, could you remember it?",
                        "Sure, I'll remember it.",
                    ],
                ],
                "user_query": "Can you recall what is my name?",
            },
        )

        assert (
            response.status_code == 422
        )  # Unprocessable Entity with one incorrect key and correct value


def test_chat_all_incorrect_input_key():
    """Test chat functionality with all input keys being incorrect"""
    with TestClient(app) as client:
        response = client.post(
            "/ai_assistant/chat",
            json={
                "other_session_id": "123456",
                "other_chat_history": [
                    ["Hi assistant", "Hi, I'am an AI Assistant. How can I help you?"],
                    [
                        "My name is Carlomagno, could you remember it?",
                        "Sure, I'll remember it.",
                    ],
                ],
                "other_user_query": "Can you recall what is my name?",
            },
        )

        assert (
            response.status_code == 422
        )  # Unprocessable Entity with all keys incorrect


def test_chat_correct_keys_with_additional_incorrect_key():
    """Test chat functionality with one additional incorrect key"""
    with TestClient(app) as client:
        response = client.post(
            "/ai_assistant/chat",
            json={
                "session_id": "123456",
                "chat_history": [
                    ["Hi assistant", "Hi, I'am an AI Assistant. How can I help you?"],
                    [
                        "My name is Carlomagno, could you remember it?",
                        "Sure, I'll remember it.",
                    ],
                ],
                "user_query": "Can you recall what is my name?",
                "additional_key": "Non existent additional key",
            },
        )

        print(response)

        assert (
            response.status_code == 200
        )  # Success since it has the correct keys and will ignore incorrect ones


### Upload Document
