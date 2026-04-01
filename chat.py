import os
from pyexpat.errors import messages
from groq import Groq

from dotenv import load_dotenv
load_dotenv()

class Chat:
    client = Groq()
    def __init__(self):
        self.messages = [
                {
                    "role": "system",
                    "content": "Write the output in 1-2 sentences."
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

if __name__ == "__main__":
    import readline
    chat = Chat()
    while True:
        message = input("chat> ")
        if message.lower() == "exit":
            break
        response = chat.send_message(message)
        print(f"Assistant: {response}")