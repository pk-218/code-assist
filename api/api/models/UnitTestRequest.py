from pydantic import BaseModel


class UnitTestRequest(BaseModel):
    code: str
    test_module: str
    language: str
