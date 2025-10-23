import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Config:
    """Centralized configuration for API and app behavior."""
    TEQUILA_BASE: str = os.getenv("TEQUILA_BASE", "https://tequila-api.kiwi.com")
    KIWI_API_KEY: str = os.getenv("KIWI_API_KEY", "fUfVhV-v87mtISxkJPlasopiB3mmosJ1")
    DEFAULT_CURRENCY: str = os.getenv("DEFAULT_CURRENCY", "USD")

config = Config()
