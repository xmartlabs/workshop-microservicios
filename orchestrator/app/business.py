import os
import requests
from fastapi.logger import logger


BALANCE_SERVICE_BASE_URL = os.environ["BALANCE_URL"]


def money_to_balance(*, customer: str, amount: float):
    url = f"{BALANCE_SERVICE_BASE_URL}/register"
    success = False
    data = {
        "customer_id": customer,
        "amount": amount
    }
    try:
        requests.post(url, json=data)
    except Exception as e:
        logger.error(e)
        return False
    return True
