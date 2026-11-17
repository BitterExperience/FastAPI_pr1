import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

async def send_welcome_email(email: str, username:str):
    await asyncio.sleep(1)
    logger.info("log: email=%s, username=%s", email, username)