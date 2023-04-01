from dotenv import load_dotenv
import re
from settings import settings
import os
import openai
from models.Docs_CodeInput import DocsCodeInput

openai.api_key = settings.key
load_dotenv()


async def extract_docs(body: DocsCodeInput):
    print("Helo")
    print(body.code)
    code = body.code 
    language = body.language
    code = f"Generate 4 lines Documentation:"+code
    
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
    messages = [{"role": "user", "content": code}]
    # completion = await openai.ChatCompletion.acreate(messages=messages, model=settings.model,temperature=settings.temperature,
    #     max_tokens=settings.max_tokens)
    
    if completion:
        doc_string = completion['choices'][0]['message']['content']
        # print(f"'''{doc_string}'''")
        # newlines = [m.start() for m in re.finditer('\n', doc_string)]
        # newlines.spli
        # for n in newlines:
        #     print(n)
        #     doc_string = doc_string[:n+1]+'\t'+doc_string[n:]
        lines = doc_string.split('\n')
        
        mod_doc_string=''
        for i in range(0,len(lines)):
            if lines[i]!='':
                mod_doc_string+='\n    '+lines[i]
         
        # regxe search
        indx = re.search(r'def.*?(.*?)\s?:',code)

        # if pattern found
        if indx:
            print(indx.span())
            func_declaration = code[indx.span()[0]:indx.span()[1]]
            inside_def_code = code[indx.span()[1]:]
            code_with_docs= func_declaration+"\n    '''"+mod_doc_string+"\n    '''"+'\n'+inside_def_code
    print(code_with_docs)
    return code_with_docs