from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn


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
    return {"test":123}

if __name__ == "__main__":
    uvicorn.run(app=app, port=8555)
