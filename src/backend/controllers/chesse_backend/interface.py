from abc import abstractmethod

from utils import meta


class AbstractCheSSEBackendController(metaclass=meta.SingletonABCMeta):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def get_similar_positions(self, fen: str) -> None:
        """_summary_

        Args:
            fen (str): _description_
        """
        raise NotImplementedError
