from dotenv import load_dotenv
import re
import os
import openai
from models.Docs_CodeInput import DocsCodeInput

openai.api_key = os.getenv('OPENAI_API_KEY')
load_dotenv()


async def extract_docs(body: DocsCodeInput):
    code = body.code 
    language = body.language
    code = f"Generate 4 lines Documentation for {language} code:"+code
    
    completion = {
        "choices": [
            {
            "finish_reason": "stop",
            "index": 0,
            "message": {
                "content": "As an AI language model, I do not have the complete context of the code, but I can explain the functionality of the code:\n\nThis code defines a method `play_next_song(self)` inside a class which takes no parameters except the instance self. This method performs the following actions:\n\n1. It initializes an empty list named `songs_to_suggest`.\n2. It iterates through each `song` in `self.library` and applies some filtering logic that is not included in the code snippet. This filtered `song` is then appended to the `songs_to_suggest` list.\n3. It prompts the user interface to ask for the next song to play using the filtered list `songs_to_suggest`. The user must choose a song from this list.\n4. It calls a method `request_money()` with an argument `PRICE_PER_SONG`. This method deducts the cost of one song from the user's account.\n5. It calls another method `play_song(chosen_song)` from an object `self.audio_output`. This will play the chosen song.\n\nOverall, this code is a part of a larger program that plays songs according to some specific filtering parameters and deducts money from the user's account.",
                "role": "assistant"
            }
            }
        ],
        "created": 1680338832,
        "id": "chatcmpl-70RBAVAzh9LrmvSO9hBL8biZ1U0nm",
        "model": "gpt-3.5-turbo-0301",
        "object": "chat.completion",
        "usage": {
            "completion_tokens": 245,
            "prompt_tokens": 79,
            "total_tokens": 324
        }
    }
    code_with_docs = ''
    # completion = await openai.ChatCompletion.acreate(messages=[{"role": "user", "content": code}], model="gpt-3.5-turbo")
    if completion:
        doc_string = completion['choices'][0]['message']['content']
        
        # regxe search
        indx = re.search(r'def.*?(.*?)\s?:',code)

        # if pattern found
        if indx:
            print(indx.span())
            func_declaration = code[indx.span()[0]:indx.span()[1]]
            inside_def_code = code[indx.span()[1]:]
            code_with_docs= func_declaration+'\n'+"'''"+doc_string+"'''"+'\n'+inside_def_code
    return code_with_docs