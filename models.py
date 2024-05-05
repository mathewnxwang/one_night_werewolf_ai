# from elevenlabs import generate, voices
import openai

def call_llm(user_prompt: str, model: str = 'gpt-3.5-turbo') -> str:
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "user", "content": user_prompt},
        ],
        temperature=1
    )
    message = response.choices[0].message.content
    return message

# voices = voices()
# voice_names = [voice.name for voice in voices]
# print(voice_names)