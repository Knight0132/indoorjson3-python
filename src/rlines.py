"""
File Name: rlines.py

Copyright (c) 2023 - 2024 IndoorJson

Author: Ziwei Xiang <knightzz1016@gmail.com>
Create Date: 2024/3/14
"""

import json
from functools import wraps
from typing import List, Dict


def type_check(func):
    @wraps(func)
    def wrapper(self, rlines_id: str, cell: str, ins: List[str], outs: List[str], closure: List[str], *args, **kwargs):
        if not isinstance(rlines_id, str):
            raise TypeError("rlines_id must be a string")
        if not isinstance(cell, str):
            raise TypeError("cells must be a string")
        if not isinstance(ins, list):
            raise TypeError("ins must be a list")
        if not isinstance(outs, list):
            raise TypeError("outs must be a list")
        if not isinstance(closure, list):
            raise TypeError("closure must be a list")
        return func(self, rlines_id, cell, ins, outs, closure, *args, **kwargs)
    return wrapper


class Rlines:

    @type_check
    def __init__(self, rlines_id: str, cell: str, ins: List[str], outs: List[str], closure: List[str]):
        self.__id: str = rlines_id
        self.__cell: str = cell
        self.__ins: List[str] = ins
        self.__outs: List[str] = outs
        self.__closure: List[str] = closure

    @property
    def id(self) -> str:
        return self.__id

    @property
    def cell(self) -> str:
        return self.__cell

    @property
    def ins(self) -> List[str]:
        return self.__ins

    @property
    def outs(self) -> List[str]:
        return self.__outs

    @property
    def closure(self) -> List[str]:
        return self.__closure

    def to_json(self) -> Dict:
        result = {}
        for key, value in self.__dict__.items():
            json_key = key.split('__')[-1]
            if json_key == 'id':
                json_key = '$id'
            result[json_key] = value
        return result

    @classmethod
    def from_json(cls, json_dict: Dict) -> 'Rlines':
        json_dict['rlines_id'] = json_dict.pop('$id')
        return cls(**json_dict)
