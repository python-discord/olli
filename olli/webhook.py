"""This module contains the logic for sending webhooks to Discord."""
from datetime import datetime
from typing import Any

import httpx
from loguru import logger

from olli.config import CONFIG
from olli.structures import TokenMatch


def send_with_backoff(url: str, json: dict[str, Any], n: int = 5) -> None:
    """Send a webhook payload with configurable retries."""
    i = 0
    while True:
        try:
            httpx.post(url, json=json).raise_for_status()
            break
        except Exception:
            i += 1
            if i == n:
                logger.exception(f"Could not POST to URL {url}")
                break


def send_olli_error(error: str) -> None:
    """Send an error embed containing the passed error message to Discord."""
    logger.info("Sending error payload to Discord")
    send_with_backoff(CONFIG.discord.webhook_url, {
        "embeds": [{
            "title": "Olli Error",
            "color": 0xff5f5f,
            "description": f"Olli encountered an error: {error}",
            "timestamp": datetime.utcnow().isoformat()
        }]
    })


def send_token_matches(matches: list[TokenMatch]) -> None:
    """Send the found token matches to Discord.

    The method checks that each token has at least 1 match and then merges
    together up to 10 embeds into one webhook payload.
    """
    embeds = []

    for match in matches:
        if sum(match.services.values()) == 0:
            continue

        embed = {
            "title": f"Logs - {match.token.token}",
            "description": f"`{sum(match.services.values())}` events matching",
            "color": int(match.token.color[1:], 16),
            "author": {
                "name": "Olli"
            },
            "footer": {
                "text": f"Last {CONFIG.olli.interval_minutes} minutes"
            },
            "timestamp": datetime.utcnow().isoformat(),
            "fields": []
        }

        for service, count in match.services.items():
            embed["fields"].append({
                "name": service,
                "value": f"`{count:,}` logs",
                "inline": True
            })

        embeds.append(embed)

    if len(embeds) > 0:
        logger.info("Sending alerts payload to Discord")
        send_with_backoff(CONFIG.discord.webhook_url, {
            "embeds": embeds
        })
    else:
        logger.info("No alerts to send to Discord")
