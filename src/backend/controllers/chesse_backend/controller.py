import itertools

import chess

from backend.controllers.chesse_backend import interface
from utils.encoding import activity_encoding, connectivity_encoding, naive_encoding


class CheSSEBackendController(interface.AbstractCheSSEBackendController):
    def __init__(self) -> None:
        ...

    def get_similar_positions(self, fen: str) -> None:
        position_encodings = list(
            itertools.chain(
                activity_encoding.get_activity_encodings(fen),
                connectivity_encoding.get_connectivity_encodings(fen),
                naive_encoding.get_naive_encodings(fen),
            )
        )
        position_encoding = " ".join(position_encodings)

        print(position_encoding)
