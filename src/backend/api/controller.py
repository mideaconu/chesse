from loguru import logger

from backend import factory
from utils import encoding
from utils.typing import JSON


class CheSSEBackendController:
    def __init__(self) -> None:
        self.search_engine_controller = factory.CheSSEBackendFactory.get_search_engine_controller()

    def get_search_position_results(self, fen: str) -> JSON:
        """_summary_

        Args:
            fen (str): _description_

        Returns:
            _type_: _description_
        """
        position_encoding = encoding.get_similarity_encoding(fen)

        logger.debug(f"Similarity encoding for position {fen}: {position_encoding}")

        similar_positions = self.search_engine_controller.get_similar_positions(position_encoding)

        fen_list = [position["fen"] for position in similar_positions]

        postion_stats = self.search_engine_controller.get_positions_stats(fen_list)

        for position in similar_positions:
            position["stats"] = postion_stats[position["fen"]]

        return similar_positions
