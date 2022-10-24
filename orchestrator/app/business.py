import asyncio
import os
import requests
from fastapi.logger import logger

from exeptions import BankIssue, InsufficientBalance
import crud

BALANCE_SERVICE_BASE_URL = os.environ["BALANCE_URL"]
BANK_SERVICE = os.environ["BANK_SERVICE"]


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
    if req.status_code == 400 and req.text == "INSUFFICIENT_BALANCE":
        raise InsufficientBalance()

    success = req.status_code == 200
    return success

async def get_bank_account(*, customer):
    customer_data = await crud.get(customer)
    return customer_data.bank_account
    

async def send_to_bank(*, customer: str, amount: float):
    account = await get_bank_account(customer=customer)
    url = f"{BANK_SERVICE}/api/withdraw/"
    success = False
    data = {
        "customer_id": customer,
        "account": account,
        "amount": amount
    }
    try:
        req = requests.post(url, json=data)
    except requests.exceptions.RequestException as e:
        logger.error(e)
        return False
    
    success = req.status_code == 200
    if not success and req.text[:9] == "ERR_BANK_":
        raise BankIssue()


async def execute_withdraw(customer: str, amount: float):
    debited = money_to_balance(customer=customer, amount=-amount)
    if debited:
        await send_to_bank(customer=customer, amount=amount)