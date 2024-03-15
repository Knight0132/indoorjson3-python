"""
File Name: serialization.py

Copyright (c) 2023 - 2024 IndoorJson

Author: Ziwei Xiang <knightzz1016@gmail.com>
Create Date: 2024/3/13
"""

import json
from indoorspace import IndoorSpace


def serialization(filepath: str, indoorspace: IndoorSpace):
    indoorSpace_jsondata = indoorspace.to_json()
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(indoorSpace_jsondata)


def deserialization(filepath: str) -> IndoorSpace:
    with open(filepath, 'r', encoding='utf-8') as file:
        indoorSpace_str = file.read()
    return IndoorSpace().from_json(indoorSpace_str)
