from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from random import randint
import json


app = FastAPI()
app.mount("/static", StaticFiles(directory="./static"), name="static")
templates = Jinja2Templates("./templates")


@app.get("/")
def root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/index2")
def index2(request: Request):
    return templates.TemplateResponse(request=request, name="index2.html")


@app.get("/test_json")
def test_json(request: Request):
    number = randint(0, 100000)
    with open(file="./json_test.txt", mode="+a") as file:
        file.write(f"{number}\n")
    return number

@app.post("/test_post")
async def test_post(request: Request):
    bb = await request.body()
    print(bb)
    print("OK")


if __name__ == "__main__":
    uvicorn.run(app=app, port=80, host="192.168.88.60")
