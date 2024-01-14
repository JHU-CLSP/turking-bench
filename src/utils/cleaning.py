from typing import List, Union


def try_numeric(x: str) -> str:
    """Helper function to convert a string to float representation if possible."""
    try:
        float_value = float(x)
        int_value = int(float_value)
        if int_value == float_value:
            return str(int_value)
        else:
            return str(float_value)
    except:
        return x


def clean_values(values: List[str]) -> List[Union[str, int, float]]:
    """
    This function cleans the values by removing empty strings and "nan" values.
    """

    return [
        try_numeric(value) if value is not None else ''
        for value in values
    ]
