from abc import abstractmethod

from utils import meta


class AbstractDataController(metaclass=meta.SingletonABCMeta):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        raise NotImplementedError
