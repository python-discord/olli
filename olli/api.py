"""The API logic for interacting with Loki."""
import datetime
from typing import Any

import httpx

from olli.config import LOKI_CONFIG, SERVICE_CONFIG, TokenConfig


class LokiHTTPClient:
    """A class for running queries on a Loki instance via the HTTP API."""

    @staticmethod
    def route(path: str) -> str:
        """Generate the Loki API route for a given path."""
        return LOKI_CONFIG.api_url + "/loki/api/v1/" + path

    def get_token_logs(self, token: TokenConfig) -> dict[str, Any]:
        """
        Fetch the logs from configured services for a matching token.

        The term is searched case-insensitively in the logs for the interval
        configured in the config.toml file.
        """
        td = datetime.timedelta(minutes=SERVICE_CONFIG.interval_minutes)
        start_time = datetime.datetime.now(tz=datetime.UTC) - td
        start_ts = start_time.timestamp() * 1_000_000_000

        job_regex = "|".join(LOKI_CONFIG.jobs)

        case_filter = "(?i)" if not token.case_sensitive else ""

        resp = httpx.get(self.route("query_range"), params={
            "query": f'{{job=~"({job_regex})"}} |~ "{case_filter}{token.token}"',
            "start": f"{start_ts:0.0f}",
            "limit": LOKI_CONFIG.max_logs,
        })

        resp.raise_for_status()

        return resp.json()
