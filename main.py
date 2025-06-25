from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from utils import feedback_logger, parse_htmx_requests


app = FastAPI()
app.mount("/static", StaticFiles(directory="./static"), name="static")
templates = Jinja2Templates("./templates")


@app.get("/")
def root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.post("/feedback_form")
async def test_post(request: Request):
    body = await request.body()
    raw_str_data = body.decode()
    form_data = parse_htmx_requests(raw_str_data)
    str_for_logger = f"Имя: {form_data['name']} Почта:{form_data['email']} Телефон: {form_data['phone']}"
    feedback_logger(str_for_logger)


if __name__ == "__main__":
    uvicorn.run(app=app, port=80, host="192.168.88.60")
