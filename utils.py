from re import sub
from typing import Union

import toml


def update_dict_key(dict_to_update: dict, old_key: str, new_key: str, new_value=None) -> dict:
    return {
        (new_key if k == old_key else k): (new_value if k == old_key and new_value else v)
        for k, v in dict_to_update.items()
    }


# Define a function to convert a string to snake case
def snake_case(s: str) -> str:
    """
    Function to convert a string to snake case.
    Replace hyphens with spaces, then apply regular expression substitutions for title case conversion
    and add an underscore between words, finally convert the result to lowercase.

    Parameters
    ----------
    s: str
        String to convert.

    Returns
    -------
    str
        Converted string.
    """
    return '_'.join(
        sub('([A-Z][a-z]+)', r' \1',
            sub('([A-Z]+)', r' \1',
                s.replace('-', ' '))).split()).lower()

def parse_toml(path: str) -> Union[dict, list]:
    with open(path, 'r') as f:
        config = toml.load(f)
    return config
