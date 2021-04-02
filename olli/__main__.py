"""Entrypoint for the Olli application."""

import time

import schedule
from loguru import logger

from olli.alert import run
from olli.config import CONFIG


@logger.catch
def start() -> None:
    """Start the Olli process."""
    logger.info("Starting Olli")
    schedule.every(CONFIG.olli.interval_minutes).minutes.do(run)

    run()

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    start()
