import chainlit as cl
import yaml
import requests
from openai import OpenAI

# Load config
config = yaml.safe_load(open("config.yaml"))

# Initialize OpenAI client
client = OpenAI(api_key=config['openai']['api_key'])

@cl.on_chat_start
def on_chat_start():
    cl.user_session.set("hist", "")

@cl.on_message
async def on_message(message: cl.Message):
    hist = cl.user_session.get("hist")

    # Generate response
    response = generate_response(message.content)

    # Update the chat history
    cl.user_session.set("hist", hist + ' ' + response)

    # Send the response back to the user
    await cl.Message(content=response).send()

def generate_response(message):
    # Define the payload for the FastAPI endpoint
    payload = {"text": message}

    # Send a POST request to the FastAPI backend
    response = requests.post("http://localhost:8000/generate_response", json=payload)

    # Return the response from the FastAPI backend
    return response.text

if __name__ == "__main__":
    from chainlit.cli import run_chainlit
    run_chainlit("app.py")