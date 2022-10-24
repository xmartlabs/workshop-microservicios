import logging
from fastapi import FastAPI
from fastapi.logger import logger as fastapi_logger


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

