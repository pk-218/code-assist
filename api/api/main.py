from typing import Optional
from pydantic import BaseModel
from dotenv import load_dotenv
import re
import os
import openai
from fastapi import FastAPI

load_dotenv()


openai.api_key = os.getenv('OPENAI_API_KEY')
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id:int, q:Optional[str]=None):
    return {"item_id":item_id,"q":q}

class Item(BaseModel):
    name:str

@app.post("/items/")
def create_item(item: Item):
    return item

@app.post("/docs/")
async def extract_docs(item:Item ):
    # create a completion
    # code='''Generate 4 lines Documentation for :
    #         def sendEmail():
    #             sender = 'from@fromdomain.com'
    #             receivers = ['to@todomain.com']

    #             message = """From: From Person <from@fromdomain.com>
    #             To: To Person <to@todomain.com>
    #             Subject: SMTP e-mail test

    #             This is a test e-mail message.
    #             """

    #             try:
    #             smtpObj = smtplib.SMTP('localhost')
    #             smtpObj.sendmail(sender, receivers, message)         
    #             print "Successfully sent email"
    #             except SMTPException:
    #             print "Error: unable to send email"
    # '''
    code='''
    Generate 4 lines Documentation for :
    def play_next_song(self):
        songs_to_suggest = []
        for song in self.library:
            # filter logic
            songs_to_suggest.append(song)
        chosen_song = self.ui.prompt_for_next_song(songs_to_suggest)
        request_money(PRICE_PER_SONG)
        self.audio_output.play_song(chosen_song)
    '''
    # completion= {
    #     "choices": [
    #         {
    #         "finish_reason": "stop",
    #         "index": 0,
    #         "message": {
    #             "content": "Function Name: sendEmail\nParameters: None\nReturns: None\n\nDescription: This function sends a test e-mail message from the sender email address to the receiver email address using the SMTP protocol. It first sets the sender and receiver email addresses and composes a message to be sent. Then it attempts to connect to the local SMTP server and sends the email. If successful, it prints a success message, otherwise it prints an error message.",
    #             "role": "assistant"
    #         }
    #         }
    #     ],
    #     "created": 1680335163,
    #     "id": "chatcmpl-70QDz0rMQ8BLJi4QKc5Qa0cYgkLma",
    #     "model": "gpt-3.5-turbo-0301",
    #     "object": "chat.completion",
    #     "usage": {
    #         "completion_tokens": 88,
    #         "prompt_tokens": 135,
    #         "total_tokens": 223
    #     }
    # }
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
    # completion = await openai.ChatCompletion.acreate(messages=[{"role": "user", "content": code}], model="gpt-3.5-turbo")
    if completion:
        doc_string = completion['choices'][0]['message']['content']
        # print(completion)
        # print(doc_string)
        
        # regxe search
        indx = re.search(r'def.*?(.*?)\s?:',code)

        # if pattern found
        if indx:
            print(indx.span())
            func_declaration = code[indx.span()[0]:indx.span()[1]]
            inside_def_code = code[indx.span()[1]:]
            print(func_declaration+'\n'+"'''"+doc_string+"'''"+'\n'+inside_def_code)
    return item