import requests
import logging


def wrap_text(text):
    return f" {text} "


def get_logger():
    Log_Format = "%(levelname)s %(asctime)s - %(message)s"
    logging.basicConfig(
        filename="logfile.log", filemode="w", format=Log_Format, level=logging.INFO
    )
    logger = logging.getLogger()
    return logger


# TODO: make async
async def get_fresh_quote(quotes: int):
    result = ""
    for _ in range(quotes):
        quotable_api_url = "https://api.quotable.io/random"  # Don't Abuse the apis :)
        try:
            response = requests.get(quotable_api_url)
        except ConnectionError as cer:
            raise cer
        except Exception as e:
            raise Exception(
                "Could not fetch your typing data !! Sorry for the inconvenience"
            )
        if response.status_code == 200:
            data = response.json()
            quote = data["content"]
            result += quote + " "
        else:
            raise Exception(
                "Could not fetch your typing data !! Sorry for the inconvenience"
            )
    return result[: len(result) - 1]  # removes last space
