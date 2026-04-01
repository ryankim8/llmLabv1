import os
from pyexpat.errors import messages
from groq import Groq

from dotenv import load_dotenv
load_dotenv()

class Chat:
    client = Groq()
    def __init__(self, message):
        self.messages = [
                {
                    "role": "system",
                    "content": "Write the output in 1-2 sentences."
                },
                {
                    "role": "user",
                    "content": message,
                }
            ]
    def send_message(self, message):
        self.messages.append({
            "role": "user",
            "content": message
        })
        chat_completion = self.client.chat.completions.create(
            messages=self.messages,
            model="llama-3.1-8b-instant",
        )
        result =  chat_completion.choices[0].message.content
        self.messages.append({
            "role": "assistant",
            "content": result
        })
        return result


'''
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),  # This is the default and can be omitted
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "Write the output in 1-2 sentences."
        },
        {
            "role": "user",
            "content": "Explain the importance of low latency LLMs",
        }
    ],
    model="llama-3.1-8b-instant",
)
print(chat_completion.choices[0].message.content)
'''