##test

import openai
from openai import OpenAI
import os
import time

PINK = '\033[95m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
NEON_GREEN = '\033[92m'
RESET_COLOR = '\033[0m'

client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")

def chatgpt_streamed(user_input):
    streamed_completion = client.chat.completions.create(
        model="local-model",
        messages=[
            {"role": "user", "content" : user_input}
        ],
        stream = True
    )

    full_response = ""
    line_buffer = ""

    for chunk in streamed_completion :
        delta_content = chunk.choices[0].delta.content

        if delta_content is not None:

            line_buffer += delta_content

            if '\n' in line_buffer:
                lines = line_buffer.split('\n')
                for line in lines[:-1]:
                    print(NEON_GREEN + line + RESET_COLOR)
                    full_response += line + '\n'
                line_buffer = lines[-1]

    if line_buffer:
        print(NEON_GREEN + line_buffer + RESET_COLOR)
        full_response += line_buffer

    return full_response

prompt = "Write an article:"
solution = chatgpt_streamed(prompt)
