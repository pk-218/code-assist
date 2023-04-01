from pydantic import BaseModel


class OptimizeCodeInput(BaseModel):
    language: str
    code: str
