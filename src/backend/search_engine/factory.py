import os

from backend.search_engine.controller import elasticsearch
from backend.search_engine.controller import interface as controller_if
from backend.utils import meta


class SearchEngineFactory(metaclass=meta.Singleton):
    @classmethod
    def get_controller(cls) -> controller_if.AbstractSearchEngineController:
        """Returns the search engine controller based on environment
        configuration.

        Raises:
            ValueError: If the configuration doesn't match any existing
            conrollers.
        """
        search_engine = os.getenv("SEARCH_ENGINE")

        match search_engine:
            case "elasticsearch":
                return elasticsearch.ElasticsearchController()
            case _:
                raise ValueError(
                    f"Could not find implementation for search engine type {search_engine}."
                )