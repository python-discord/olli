"""Structures for auto-completion and data storage."""
from dataclasses import dataclass

from olli.config import TokenConfig


@dataclass
class TokenMatch:
    """
    A dataclass representing a searched token.

    The token is an instance of TokenConfig which contains the information on which token
    was found. The services dictionary contains a map of service names to the number of times
    this specific token appeared in their logs.
    """

    token: TokenConfig
    services: dict[str, int]
