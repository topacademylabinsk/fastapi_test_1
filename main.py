from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from app.utils import feedback_logger_to_file, validate_form_data
from app.db import db_con


app = FastAPI()
app.mount("/static", StaticFiles(directory="./app/static"), name="static")
templates = Jinja2Templates("./app/templates")


@app.get("/")
def root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/data")
def get_data(request: Request):
    list_data = db_con.get_all_data("form_data")
    return templates.TemplateResponse(
        request=request, name="data.html", context={"list_data": list_data}
    )


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


if __name__ == "__main__":
    uvicorn.run(app=app, port=80, host="192.168.88.60")
