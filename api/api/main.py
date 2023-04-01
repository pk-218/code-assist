
from fastapi import FastAPI

from controllers.get_unit_test import get_unit_test
from models.UnitTestRequest import UnitTestRequest


from controllers.optimize_code import optimize_code
from models.optimize_code_input import OptimizeCodeInput

from controllers.get_documentation import extract_docs
from models.Docs_CodeInput import DocsCodeInput


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post('/optimize-code')
def optimize_code_route(body: OptimizeCodeInput):
    return {"ans": optimize_code(body)}


@app.post("/ut")
async def create_ut(req: UnitTestRequest):
    """
    Creates unit test for given POST request with request body which contains code, test_module, and language.
    """
    return get_unit_test(req)


@app.post('/docs')
async def create_docs(req: DocsCodeInput):
    """
    Returns documentation for given POST request with request body containing code and corresponding language
    """
    return await extract_docs(req)