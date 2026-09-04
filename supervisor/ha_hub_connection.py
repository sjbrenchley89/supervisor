"""Home Assistant Hub Connection Configuration."""

import os

import aiohttp

from .exceptions import HassioError


class HAHubConfig:
    """Configuration for Home Assistant Hub connection."""

    def __init__(self) -> None:
        """Initialize Home Assistant Hub configuration."""
        self._url: str | None = None
        self._token: str | None = None
        self._load_from_env()

    def _load_from_env(self) -> None:
        """Load configuration from environment variables."""
        self._url = os.getenv("HA_HUB_URL")
        self._token = os.getenv("HA_HUB_TOKEN")

    @property
    def url(self) -> str | None:
        """Return Home Assistant Hub URL."""
        return self._url

    @property
    def token(self) -> str | None:
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
            async with aiohttp.ClientSession() as session:
                # Type assertions for mypy: is_configured ensures these are not None
                assert self._url is not None
                assert self._token is not None
                headers = {"Authorization": f"Bearer {self._token}"}
                timeout = aiohttp.ClientTimeout(total=5)
                async with session.get(
                    f"{self._url}/api/", headers=headers, timeout=timeout
                ) as response:
                    return response.status == 200
        except Exception:
            return False


# Global configuration instance
ha_hub_config = HAHubConfig()
