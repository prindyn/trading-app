from abc import ABC, abstractmethod
from typing import Dict, List, Any
import httpx
from app.core.logger import logger


class BaseClient(ABC):
    endpoint: str = ""
    request_fields: Dict[str, str] = {}

    def __init__(self, base_url: str, name: str = ""):
        """
        Base class for all data clients.
        :param base_url: Base URL of the API
        :param payload: Dictionary of input config/params
        :param name: Name of the client
        """
        self._params: Dict[str, Any] = {}
        self.base_url = base_url.rstrip("/")
        self.name = self.name = f"{self._name}_{name}" if name else self._name

    def map_params(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map standard payload keys to API-specific parameter names.
        :param payload: Dictionary of input config/params
        """
        if not self.request_fields:
            logger.warning(f"No request fields defined for this client: {self.name}")
            return payload

        return {
            api_key: payload.get(internal_key)
            for api_key, internal_key in self.request_fields.items()
            if internal_key in payload
        }

    def build_params(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build the query parameters for the API request.
        :param payload: Input parameters or config
        """
        return self.map_params(payload)

    async def fetch_data(self, payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Fetch raw data from the API and return parsed normalized result.
        :param payload: Dictionary of input
        :return: List of parsed dictionaries
        """
        try:
            self._params = self.build_params(payload)
            url = f"{self.base_url}{self.endpoint}"
            logger.info(f"Requesting: {url} with params: {self._params}")

            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=self._params)
                response.raise_for_status()
                raw_data = response.json()

            return self.parse_data(raw_data)

        except Exception as e:
            logger.error(f"Error fetching data from {self.endpoint}: {str(e)}")
            raise

    @abstractmethod
    def parse_data(self, raw: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Parse the raw API response into a normalized list of dictionaries.
        :param raw: Raw JSON response from the API
        :return: List of parsed data entries
        """
        raise NotImplementedError

    @property
    def _name(self):
        return self.__class__.__name__.replace("Client", "").lower()
