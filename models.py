# from elevenlabs import generate, voices
import os

from dotenv import load_dotenv
from openai import OpenAI

class LLMManager():
    def __init__(self, model: str = 'gpt-3.5-turbo'):
        self.model = model

        load_dotenv("secrets.env")
        openai_api_key = os.getenv("OPENAI_API_KEY")
        print("openai_api_key should be defined and this should print before the error")
        print(openai_api_key)
        self.client = OpenAI(api_key=openai_api_key)

    def call_llm(self, user_prompt: str) -> str:
        response = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            model=self.model,
            temperature=1
        )
        message = response.choices[0].message.content
        print(response)
        return message

# voices = voices()
# voice_names = [voice.name for voice in voices]
# print(voice_names)