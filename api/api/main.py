from controllers.get_unit_test import get_unit_test
from models.UnitTestRequest import UnitTestRequest

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/ut")
async def create_ut(req: UnitTestRequest):
    """
    Creates unit test for given POST request with request body which contains code, test_module, and language.
    """
    return get_unit_test(req)
