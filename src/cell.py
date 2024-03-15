"""
File Name: cell.py

Copyright (c) 2023 - 2024 IndoorJson

Author: Ziwei Xiang <knightzz1016@gmail.com>
Create Date: 2024/3/14
"""

import json
from functools import wraps
from typing import Dict
from shapely.wkt import loads
from shapely.geometry.base import BaseGeometry


def type_check(func):
    @wraps(func)
    def wrapper(self, cell_id: str, properties: Dict, space: BaseGeometry, node: BaseGeometry, *args, **kwargs):
        if not isinstance(cell_id, str):
            raise TypeError("cell_id must be a string")
        if not isinstance(properties, dict):
            raise TypeError("properties must be a dictionary")
        if not isinstance(space, BaseGeometry):
            raise TypeError("space must be a BaseGeometry instance")
        if not isinstance(node, BaseGeometry):
            raise TypeError("node must be a BaseGeometry instance")
        return func(self, cell_id, properties, space, node, *args, **kwargs)
    return wrapper


class Cell:

    @type_check
    def __init__(self, cell_id: str, properties: Dict, space: BaseGeometry, node: BaseGeometry):
        self.__id: str = cell_id
        self.__properties: Dict = properties
        self.__space: BaseGeometry = space
        self.__node: BaseGeometry = node

    @property
    def id(self) -> str:
        return self.__id

    @property
    def properties(self) -> Dict:
        return self.__properties

    @property
    def space(self) -> BaseGeometry:
        return self.__space

    @property
    def node(self) -> BaseGeometry:
        return self.__node

    def to_json(self) -> Dict:
        result = {}
        for key, value in self.__dict__.items():
            json_key = key.split('__')[-1]
            if isinstance(value, BaseGeometry):
                result[json_key] = value.wkt
            elif json_key == 'id':
                json_key = '$id'
                result[json_key] = value
            else:
                result[json_key] = value
        return result

    @classmethod
    def from_json(cls, json_dict: Dict) -> 'Cell':
        json_dict['cell_id'] = json_dict.pop('$id')
        json_dict['space'] = loads(json_dict['space'])
        json_dict['node'] = loads(json_dict['node'])
        return cls(**json_dict)
