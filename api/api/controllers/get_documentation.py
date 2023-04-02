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
    code = body.code 
    language = body.language

    regexPythonFunction = r'def.*?(.*?)\s?:'
    if language=='python':

        # if no function definition exist inside code
        def_exist = re.search(regexPythonFunction,code)
        before_def=""
        if def_exist==None:
            return dict({"code_with_docs":code_with_docs,"more_than_one_def":False})
        else:
            before_def=code[0:def_exist.span()[0]]
    
        more_than_one_def=False
        
        # if more than one function definition found inside code
        find_def = re.findall(regexPythonFunction,code)
        if len(find_def)>1:
            more_than_one_def=True
    
        code = f"Generate 4 lines documentation with request and response with  code details:"+code
        
        # completion = {
        #     "choices": [
        #         {
        #         "finish_reason": "stop",
        #         "index": 0,
        #         "message": {
        #             "content": '''    1. The sendEmail() function is used to send an email using SMTP protocol.
        # 2. The sender and receivers parameters must be specified to define the email addresses of the sender and recipient(s).
        # 3. The message parameter contains the content of the email, including the subject and body.
        # 4. The function attempts to send the email using the specified SMTP server and prints a success or error message depending on the outcome.''',
        #             "role": "assistant"
        #         }
        #         }
        #     ],
        #     "created": 1680338832,
        #     "id": "chatcmpl-70RBAVAzh9LrmvSO9hBL8biZ1U0nm",
        #     "model": "gpt-3.5-turbo-0301",
        #     "object": "chat.completion",
        #     "usage": {
        #         "completion_tokens": 245,
        #         "prompt_tokens": 79,
        #         "total_tokens": 324
        #     }
        # }
        code_with_docs = ''
        messages = [{"role": "user", "content": code}]
        completion = await openai.ChatCompletion.acreate(messages=messages, model=settings.model,temperature=settings.temperature,
            max_tokens=settings.max_tokens)
        
        if completion:
            doc_string = completion['choices'][0]['message']['content']

            lines = doc_string.split('\n')
            
            mod_doc_string=''
            for i in range(0,len(lines)):
                if lines[i]!='':
                    mod_doc_string+='\n    '+lines[i]
            
            # regxe search
            indx = re.search(regexPythonFunction,code)

            # if pattern found
            if indx:
                print(indx.span())
                
                func_declaration = code[indx.span()[0]:indx.span()[1]]
                inside_def_code = code[indx.span()[1]:]
                code_with_docs= before_def+func_declaration+"\n    '''"+mod_doc_string+"\n    '''"+'\n'+inside_def_code
        print(code_with_docs)
        return dict({"code_with_docs":code_with_docs,"more_than_one_def":more_than_one_def})
    
    else:
        print(code)
        tradJs=re.search(r'\n?.*?function.*?(.*?)\s?{',code)
        arrowJs=re.search(r'\n?.*?=\s?(.*?)=>\s?{',code)
        validator=""
        if tradJs:
            validator=r'\n?.*?function.*?(.*?)\s?{'
        
        elif arrowJs:
            validator=r'\n?.*?=\s?(.*?)=>\s?{'
        print(validator)
        before_def=""
        full_def=""
        # if no function definition exist inside code
        def_exist = re.search(validator,code)
        
        if def_exist==None:
            return dict({"code_with_docs":code_with_docs,"more_than_one_def":False})
        else:
            before_def=code[0:def_exist.span()[0]]
            full_def=code[def_exist.span()[0]:]
        more_than_one_def=False
        
        # if more than one function definition found inside code
        find_def = re.findall(validator,code)
        print(find_def)
        if len(find_def)>1:
            more_than_one_def=True

        code = f"Generate 4 lines documentation with request and response with  code details:"+code
        
        # completion = {
        #     "choices": [
        #         {
        #         "finish_reason": "stop",
        #         "index": 0,
        #         "message": {
        #             "content": '''    1. The sendEmail() function is used to send an email using SMTP protocol.
        # 2. The sender and receivers parameters must be specified to define the email addresses of the sender and recipient(s).
        # 3. The message parameter contains the content of the email, including the subject and body.
        # 4. The function attempts to send the email using the specified SMTP server and prints a success or error message depending on the outcome.''',
        #             "role": "assistant"
        #         }
        #         }
        #     ],
        #     "created": 1680338832,
        #     "id": "chatcmpl-70RBAVAzh9LrmvSO9hBL8biZ1U0nm",
        #     "model": "gpt-3.5-turbo-0301",
        #     "object": "chat.completion",
        #     "usage": {
        #         "completion_tokens": 245,
        #         "prompt_tokens": 79,
        #         "total_tokens": 324
        #     }
        # }
        code_with_docs = ''
        messages = [{"role": "user", "content": code}]
        completion = await openai.ChatCompletion.acreate(messages=messages, model=settings.model,temperature=settings.temperature,
            max_tokens=settings.max_tokens)
        
        if completion:
            doc_string = completion['choices'][0]['message']['content']

            lines = doc_string.split('\n')
            
            mod_doc_string=''
            for i in range(0,len(lines)):
                if lines[i]!='':
                    mod_doc_string+='\n'+lines[i]
            
            # regxe search
            indx = re.search(validator,code)

            # if pattern found
            if indx:
                print(indx.span())
                func_declaration = code[indx.span()[0]:indx.span()[1]]
                inside_def_code = code[indx.span()[1]:]
                code_with_docs= before_def+"/**\n"+mod_doc_string+"\n*/\n"+full_def
        print(code_with_docs)
        return dict({"code_with_docs":code_with_docs,"more_than_one_def":more_than_one_def})

