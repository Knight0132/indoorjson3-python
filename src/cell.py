"""
File Name: cell.py

Copyright (c) 2023 - 2024 IndoorJson

Author: Ziwei Xiang <knightzz1016@gmail.com>
Create Date: 2024/3/14
"""

from shapely.wkt import loads


class Cell:

    def __init__(self, cell_id, properties, space, node):
        self.__id = cell_id
        self._properties = properties
        self.__space = space
        self.__node = node

    @property
    def id(self):
        return self.__id

    @property
    def properties(self):
        return self._properties

    @property
    def space(self):
        return self.__space

    @property
    def node(self):
        return self.__node

    @classmethod
    def from_json(cls, json_data):
        return cls(json_data['$id'], json_data['properties'],
                   loads(json_data['space']), loads(json_data['node']))

    def to_json(self):
        return {
            '$id': self.__id,
            'properties': self._properties,
            'space': self.__space.wkt,
            'node': self.__node.wkt
        }
