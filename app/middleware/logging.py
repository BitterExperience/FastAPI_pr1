import logging
import time

from fastapi import Request


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start

    logger.info(
        "log: method=%s path=%s status=%s time=%.4fs",
        request.method,
        request.url.path,
        response.status_code,
        process_time,
    )
    response.headers["X-Process-Time"] = f"{process_time:.4f}"
    return response