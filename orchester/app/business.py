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
        req = requests.post(url, json=data)
    except requests.exceptions.RequestException as e:
        logger.error(e)
        return False

    success = req.status_code == 200
    return success

def send_to_bank(*, customer: str, bank: str, amount: float):
    ...

def withdraw(*, customer: str, amount: float):

    debited = money_to_balance(
        customer=customer,
        amount= -amount
    )
    if not debited:
        return False

    sent = send_to_bank(
        customer=customer,
        bank="National",
        amount=amount
    )
    if not sent:
        money_to_balance(
            customer=customer,
            amount= amount
        )
    return True