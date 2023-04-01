from pydantic import BaseModel


class DocsCodeInput(BaseModel):
    code: str
    language: str
