import os
import openai

from dotenv import load_dotenv
from models.optimize_code_input import OptimizeCodeInput

load_dotenv()

API_KEY = os.getenv('OPENAI_API_KEY')

openai.api_key = API_KEY


def optimize_code(body: OptimizeCodeInput):
    language = body.language
    code_to_optimize = body.code

    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                              messages=[{
                                                  "role": "user",
                                                  "content": f'''Give me just the optimized {language} code for the following: \n{code_to_optimize}'''}
                                              ])

    return completion
