from email_validator import validate_email, EmailNotValidError
import re


def feedback_logger_to_file(data: str):
    with open(file="./feedback_logs.txt", mode="+a", encoding="UTF-8") as file:
        file.write(f"{data}\n")


def parse_htmx_requests(raw_data: str) -> dict[str, str]:
    data_list = raw_data.split("&")
    data_dict = {}
    for i in data_list:
        param = i.split("=")
        data_dict[param[0]] = param[1]
    return data_dict


def validate_form_data(name: str, email: str, number: str) -> dict[str, str]:
    result = {}
    if name:
        result["name"] = True
    else:
        result["name"] = False

    try:
        validate_email(email)
        result["email"] = True
    except EmailNotValidError:
        result["email"] = False

    number_result = re.match(
        r"^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$",
        number,
    )
    if number_result:
        result["number"] = True
    else:
        result["number"] = False

    return result
