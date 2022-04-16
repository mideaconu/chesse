import os

from backend.search_engine import controller
from backend.search_engine import controller_interface as search_engine_if


class CheSSEBackendFactory:
    @classmethod
    def get_search_engine_controller(cls) -> search_engine_if.AbstractSearchEngineController:
        """Returns the search engine controller based on environment
        configuration.

        Raises:
            NotImplementedError: If the configuration doesn't match any
            existing conrollers.
        """
        search_engine = os.getenv("SEARCH_ENGINE")

        match search_engine:
            case "elasticsearch":
                return controller.ESController()
            case _:
                raise NotImplementedError(
                    f"Could not find implementation for search engine type {search_engine}."
                )
