from settings import settings

import openai


def get_unit_test(req):
    messages = [
        {
            "role": "user",
            "content": f"""Write a unit test in {req.language} using {req.test_module} for this function:\n {req.code}""",
        }
    ]
    openai.api_key = settings.key
    res = openai.ChatCompletion.create(
        model=settings.model,
        messages=messages,
        temperature=settings.temperature,
        max_tokens=settings.max_tokens,
    )
    print(res)
    unit_test = ""
    for event in res["choices"]:
        event_text = event["message"]["content"]
        print(event_text, end="\n\n")
        unit_test += event_text

    return unit_test
