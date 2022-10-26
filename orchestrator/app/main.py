import logging
import customer
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.logger import logger as fastapi_logger
from starlette.middleware.cors import CORSMiddleware
from db import database
from models import AmountPayload

from business import money_to_balance, execute_withdraw
from exeptions import BankIssue, InsufficientBalance

log_levels_handler = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING
}



app = FastAPI()

formatter = logging.Formatter(
    "[ %(levelname)s %(asctime)s.%(msecs)03d] [%(thread)d] - %(message)s", "%Y-%m-%d %H:%M:%S")  # NOQA
handler = logging.StreamHandler()
logging.getLogger().setLevel(logging.DEBUG)
fastapi_logger.addHandler(handler)
handler.setFormatter(formatter)


@app.get("/")
async def root():
    return {"message": "Orchestrator is working!"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["DELETE", "GET", "POST", "PUT"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(customer.router, prefix="/customer", tags=["customer"])

@app.post("/{customer_id}/deposit/")
async def deposit(customer_id: str, body: AmountPayload):
    sent = money_to_balance(
        customer=customer_id,
        amount=body.amount
    )
    message = "Your money was received" if sent else "There was a problem. Try later"
    status = 200 if sent else 503
    return HTMLResponse(message, status)


@app.post("/{customer_id}/withdraw/")
async def withdraw(customer_id: str, body: AmountPayload):
    amount = body.amount
    try:
        await execute_withdraw(customer_id, amount)
    except InsufficientBalance:
        return HTMLResponse("There is not enough money for this operation", status_code=400)
    except BankIssue:
        return HTMLResponse("There is any problem with your Bank's system" , status_code=503)
    except Exception:
        return HTMLResponse("We are experiencing some problems just now, try later please", status_code=500)

    return HTMLResponse("Your money was sent", status_code=200)
