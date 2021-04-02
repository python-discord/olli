"""This module contains the logic for grepping logs and generating Discord alerts."""
import httpx
from loguru import logger

from olli import webhook
from olli.api import LokiHTTPClient
from olli.config import CONFIG, TokenConfig
from olli.structures import TokenMatch

api_client = LokiHTTPClient()


def get_match(token: TokenConfig) -> TokenMatch:
    """Search the configured service logs for a given token."""
    try:
        logger.debug(f"Searching for token {token.token}")
        svc_logs = api_client.get_token_logs(token.token)
    except httpx.ConnectError:
        logger.error("Could not connect to Loki")
        return webhook.send_olli_error("Loki refused to connect.")
    except httpx.HTTPStatusError as e:
        logger.error(f"Loki returned error status code: {e.response.status_code}")
        return webhook.send_olli_error(
            f"Loki returned a bad status code: `{e.response.status_code}`"
        )

    if svc_logs["status"] != "success":
        logger.error(f"Received an error response from Loki for token {token.token}")
        return webhook.send_olli_error(
            "Loki returned an error, check your service names are correct."
        )

    match = TokenMatch(token, {})

    for service in svc_logs["data"]["result"]:
        app = service["stream"].get("app")
        svc_name = app if app else service["stream"].get("job")

        count = len(service["values"])

        match.services[svc_name] = count

    logger.debug(f"Finished searching for {token.token}")

    return match


def send_alerts(matches: list[TokenMatch]) -> None:
    """Take the found matches and relay them to Discord."""
    # TODO: batch into 10 to avoid embed limits
    logger.info("Sending webhook payload to Discord")
    webhook.send_token_matches(matches)


def run() -> None:
    """Entrypoint for Olli's search process."""
    logger.info("Running Olli search")
    matches = []

    for token in CONFIG.olli.tokens:
        matches.append(get_match(token))

    send_alerts(matches)
    logger.info("Olli search complete.")
