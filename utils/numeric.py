def is_int(elem: str) -> bool:
    """Checks if a string element is a valid int."""
    return elem.isdigit()


def is_float(elem: str) -> bool:
    """Checks if a string element is a valid float."""
    try:
        float(elem)
        return True
    except ValueError:
        return False
