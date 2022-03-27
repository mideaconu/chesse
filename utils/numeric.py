def is_int(element: str) -> bool:
    """Checks if a string element is a valid int."""
    return element.isdigit()


def is_float(element: str) -> bool:
    """Checks if a string element is a valid float."""
    try:
        float(element)
        return True
    except ValueError:
        return False
