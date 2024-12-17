from functools import wraps
from typing import Any, Callable


def filter_empty_values(func: Callable) -> Callable:
    """
    Decorador para eliminar valores vacíos (None, '', {}, []) de un diccionario.
    """

    @wraps(func)
    def wrapper(*args: tuple, **kwargs: dict[str, Any]) -> Any:
        data = func(*args, **kwargs)
        if isinstance(data, dict):
            return remove_empty_values(data)
        return data

    return wrapper


def remove_empty_values(data: Any) -> Any:
    """
    Elimina recursivamente los valores vacíos (None, '', {}, []) de un diccionario o lista.
    """
    if isinstance(data, dict):
        return {k: remove_empty_values(v) for k, v in data.items() if v not in (None, "", {}, [])}
    elif isinstance(data, list):
        return [remove_empty_values(item) for item in data if item not in (None, "", {}, [])]
    return data
