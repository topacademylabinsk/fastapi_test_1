from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from utils import feedback_logger, validate_form_data


app = FastAPI()
app.mount("/static", StaticFiles(directory="./static"), name="static")
templates = Jinja2Templates("./templates")


@app.get("/")
def root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


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
        feedback_logger(str_for_logger)
        return templates.TemplateResponse(
            request=request, name="success_form_status.html"
        )


if __name__ == "__main__":
    uvicorn.run(app=app, port=80, host="192.168.88.60")
