"""
File Name: connection.py

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
    def wrapper(self, connection_id: str, properties: dict, fr: str, to: str,
                bound: BaseGeometry, edge: BaseGeometry, *args, **kwargs):
        if not isinstance(connection_id, str):
            raise TypeError("connection_id must be a string")
        if not isinstance(properties, dict):
            raise TypeError("properties must be a dictionary")
        if not isinstance(fr, str):
            raise TypeError("source must be a string")
        if not isinstance(to, str):
            raise TypeError("target must be a string")
        if not isinstance(bound, BaseGeometry):
            raise TypeError("bound must be a BaseGeometry instance")
        if not isinstance(edge, BaseGeometry):
            raise TypeError("edge must be a BaseGeometry instance")
        return func(self, connection_id, properties, fr, to, bound, edge, *args, **kwargs)
    return wrapper


class Connection:

    @type_check
    def __init__(self, connections_id: str, properties: Dict, fr: str, to: str,
                 bound: BaseGeometry, edge: BaseGeometry):
        self.__id: str = connections_id
        self.__properties: Dict = properties
        self.__source: str = fr
        self.__target: str = to
        self.__bound: BaseGeometry = bound
        self.__edge: BaseGeometry = edge

    @property
    def id(self) -> str:
        return self.__id

    @property
    def properties(self) -> dict:
        return self.__properties

    @property
    def source(self) -> str:
        return self.__source

    @property
    def target(self) -> str:
        return self.__target

    @property
    def bound(self) -> BaseGeometry:
        return self.__bound

    @property
    def edge(self) -> BaseGeometry:
        return self.__edge

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
    def from_json(cls, json_dict: Dict) -> 'Connection':
        json_dict['connection_id'] = json_dict.pop('$id')
        json_dict['bound'] = loads(json_dict['bound'])
        json_dict['edge'] = loads(json_dict['edge'])
        return cls(**json_dict)
