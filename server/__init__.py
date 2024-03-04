import uvicorn

from .route import app
from loguru import logger

def run():
    # logger.info("server: http://127.0.0.1:8250") # TODO config
    uvicorn.run(app, host="127.0.0.1", port=8250)


