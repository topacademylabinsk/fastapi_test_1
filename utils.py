def feedback_logger(data: str):
    with open(file="./feedback_logs.txt", mode="+a", encoding="UTF-8") as file:
        file.write(f"{data}\n")


def parse_htmx_requests(raw_data: str) -> dict[str, str]:
    data_list = raw_data.split("&")
    data_dict = {}
    for i in data_list:
        param = i.split("=")
        data_dict[param[0]] = param[1]
    return data_dict