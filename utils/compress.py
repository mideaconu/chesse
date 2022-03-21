import base64
import zlib


def gzip_compress(value: str) -> str:
    """Compress a string using gzip.

    Args:
        value (str): String value to encode.

    Returns:
        str: Encoding.
    """
    gzip_bytes = zlib.compress(bytes(value, encoding="utf-8"))
    gzip_str = base64.b64encode(gzip_bytes).decode(encoding="utf-8")

    return gzip_str
