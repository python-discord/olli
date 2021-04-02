"""This module contains API logic for interacting with Loki."""
import datetime
from typing import Any

import httpx

from olli.config import CONFIG


class LokiHTTPClient:
    """A class for running queries on a Loki instance via the HTTP API."""

    @staticmethod
    def route(path: str) -> str:
        """Generate the Loki API route for a given path."""
        return CONFIG.loki.api_url + "/loki/api/v1/" + path

    def get_token_logs(self, token: str) -> dict[str, Any]:
        """
        Fetch the logs from configured services for a matchign token.

        The term is searched case-insensitively in the logs for the interval
        configured in the config.toml file.
        """
        td = datetime.timedelta(minutes=CONFIG.olli.interval_minutes)
        start_time = datetime.datetime.now() - td
        start_ts = start_time.timestamp() * 1_000_000_000

        job_regex = "|".join(CONFIG.loki.jobs)

        resp = httpx.get(self.route("query_range"), params={
            "query": f'{{job=~"({job_regex})"}} |~ "(?i){token}"',
            "start": f"{start_ts:0.0f}",
            "limit": CONFIG.loki.max_logs
        })

        resp.raise_for_status()

        return resp.json()
