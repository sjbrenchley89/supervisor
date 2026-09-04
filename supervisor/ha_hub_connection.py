"""Home Assistant Hub Connection Configuration."""

import os
from typing import Optional

from .exceptions import HassioError


class HAHubConfig:
    """Configuration for Home Assistant Hub connection."""

    def __init__(self):
        """Initialize Home Assistant Hub configuration."""
        self._url: Optional[str] = None
        self._token: Optional[str] = None
        self._load_from_env()

    def _load_from_env(self) -> None:
        """Load configuration from environment variables."""
        self._url = os.getenv("HA_HUB_URL")
        self._token = os.getenv("HA_HUB_TOKEN")

    @property
    def url(self) -> Optional[str]:
        """Return Home Assistant Hub URL."""
        return self._url

    @property
    def token(self) -> Optional[str]:
        """Return Home Assistant Hub access token."""
        return self._token

    @property
    def is_configured(self) -> bool:
        """Check if Home Assistant Hub connection is configured."""
        return bool(self._url and self._token)

    def validate(self) -> None:
        """Validate Home Assistant Hub configuration."""
        if not self._url:
            raise HassioError(
                "Home Assistant Hub URL not configured. "
                "Set HA_HUB_URL environment variable."
            )
        if not self._token:
            raise HassioError(
                "Home Assistant Hub token not configured. "
                "Set HA_HUB_TOKEN environment variable."
            )

    async def test_connection(self) -> bool:
        """Test connection to Home Assistant Hub."""
        if not self.is_configured:
            return False

        try:
            import aiohttp

            async with aiohttp.ClientSession() as session:
                headers = {"Authorization": f"Bearer {self._token}"}
                async with session.get(
                    f"{self._url}/api/", headers=headers, timeout=5
                ) as response:
                    return response.status == 200
        except Exception:
            return False


# Global configuration instance
ha_hub_config = HAHubConfig()
