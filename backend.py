from fastapi import FastAPI, Request
from pydantic import BaseModel
import openai
import yaml

app = FastAPI()

# Load config
config = yaml.safe_load(open("config.yaml"))

# Set OpenAI API key
openai.api_key = config['openai']['api_key']

class TextRequest(BaseModel):
    text: str

@app.post("/generate_response")
async def generate_response(request: TextRequest):
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=request.text,
        max_tokens=50
    )
    return {"text": response.choices[0].text.strip()}

#if __name__ == "__main__":
#    import uvicorn
#    uvicorn.run(app, host="localhost", port=4000)