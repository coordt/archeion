"""
Automatically detect the true Python type of a string and cast it to the correct type.

Based on https://github.com/cgreer/cgAutoCast/blob/master/cgAutoCast.py
"""

import contextlib
from typing import Any


def boolify(s: str) -> bool:
    """Convert a string to a boolean."""
    if s in {"True", "true"}:
        return True
    if s in {"False", "false"}:
        return False
    raise ValueError("Not Boolean Value!")


def noneify(s: str) -> None:
    """Convert a string to None."""
    if s == "None":
        return None
    raise ValueError("Not None Value!")


def listify(s: str) -> list:
    """
    Convert a string representation of a list into list of homogenous basic types.

    Type of elements in list is determined via first element. Successive elements are
    cast to that type.

    Args:
        s: String representation of a list.

    Raises:
        ValueError: If string does not represent a list.
        TypeError: If string does not represent a list of homogenous basic types.

    Returns:
        List of homogenous basic types.
    """
    if "," not in s:
        raise ValueError("Not a List")

    # derive the type of the variable
    str_list = s.split(",")
    element_caster = str
    for caster in (boolify, int, float, noneify, element_caster):
        with contextlib.suppress(ValueError):
            caster(str_list[0])  # type: ignore[operator]
            element_caster = caster  # type: ignore[assignment]
            break
    # cast all elements
    try:
        return [element_caster(x) for x in str_list]
    except ValueError as e:
        raise TypeError("Autocasted list must be all same type") from e


def autocast_value(var: Any) -> Any:
    """
    Guess the string representation of the variable's type.

    Args:
        var: Value to autocast.

    Returns:
        The autocasted value.
    """
    if not isinstance(var, str):  # don't need to guess non-string types
        return var

    # guess string representation of var
    for caster in (boolify, int, float, noneify, listify):
        with contextlib.suppress(ValueError):
            return caster(var)  # type: ignore[operator]

    return var
