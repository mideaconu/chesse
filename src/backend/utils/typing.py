from typing import List, Mapping, Union

JSON = Union[str, int, float, bool, None, Mapping[str, "JSON"], List["JSON"]]
