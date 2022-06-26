import collections
from typing import List, Mapping, Union

JSON = Union[str, int, float, bool, None, Mapping[str, "JSON"], List["JSON"]]


def flatten_dict(d, parent_key="", sep="."):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.abc.MutableMapping):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    flat_dict = dict(items)
    flat_dict = {k: str(v) for k, v in flat_dict.items()}
    return flat_dict
