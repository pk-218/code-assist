from fastapi import FastAPI
from controllers.optimize_code import optimize_code
from models.optimize_code_input import OptimizeCodeInput

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get('/optimize-code')
def optimize_code_route(body: OptimizeCodeInput):
    return {"ans": optimize_code(body)}
