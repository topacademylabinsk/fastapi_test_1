import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.db import db_con
from app.utils import feedback_logger_to_file, validate_form_data

load_dotenv()

app = FastAPI()
app.mount("/static", StaticFiles(directory="./app/static"), name="static")
templates = Jinja2Templates("./app/templates")


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.post("/auth")
async def post_auth(request: Request):
    admin_pass = os.getenv("ADMIN_PASS")

    form_data = await request.json()
    form_pass = form_data["password"]

    if admin_pass == form_pass:
        list_data = db_con.get_all_data("form_data")
        return templates.TemplateResponse(
            request=request, name="data.html", context={"list_data": list_data}
        )
    else:
        return templates.TemplateResponse(request=request, name="incorrect_pass.html")


@app.get("/data")
async def get_data(request: Request):
    return templates.TemplateResponse(request=request, name="auth.html")


@app.post("/feedback_form")
async def test_post(request: Request):
    form_data = await request.json()
    name = form_data["name"]
    email = form_data["email"]
    number = form_data["phone"]

    result_validate_data = validate_form_data(name, email, number)

    if not result_validate_data["name"]:
        return "Неправильное имя"
    elif not result_validate_data["email"]:
        return "Неправильная почта"
    elif not result_validate_data["number"]:
        return "Неправильный номер"
    else:
        str_for_logger = f"Имя: {name} Почта:{email} Телефон: {number}"
        feedback_logger_to_file(str_for_logger)
        db_con.add_data(name, email, number)
        return templates.TemplateResponse(
            request=request, name="success_form_status.html"
        )
