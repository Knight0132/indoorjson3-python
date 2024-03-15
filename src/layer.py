"""
File Name: layer.py

Copyright (c) 2023 - 2024 IndoorJson

Author: Ziwei Xiang <knightzz1016@gmail.com>
Create Date: 2024/3/14
"""

import json
from functools import wraps
from typing import List, Dict


def type_check(func):
    @wraps(func)
    def wrapper(self, layer_id: str, cells: List[str], *args, **kwargs):
        if not isinstance(layer_id, str):
            raise TypeError("layer_id must be a string")
        if not isinstance(cells, list):
            raise TypeError("cells must be a list")
        return func(self, layer_id, cells, *args, **kwargs)
    return wrapper


class Layer:

    @type_check
    def __init__(self, layer_id: str, cells: List[str]):
        self.__id: str = layer_id
        self.__cells: List[str] = cells

    @property
    def id(self) -> str:
        return self.__id

    @property
    def cells(self) -> List[str]:
        return self.__cells

    def to_json(self) -> Dict:
        result = {}
        for key, value in self.__dict__.items():
            json_key = key.split('__')[-1]
            if json_key == 'id':
                json_key = '$id'
            result[json_key] = value
        return result

    @classmethod
    def from_json(cls, json_dict: Dict) -> 'Layer':
        json_dict['layer_id'] = json_dict.pop('$id')
        return cls(**json_dict)
