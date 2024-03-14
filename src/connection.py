"""
File Name: connection.py

Copyright (c) 2023 - 2024 IndoorJson

Author: Ziwei Xiang <knightzz1016@gmail.com>
Create Date: 2024/3/14
"""

from shapely.wkt import loads


class Connection:

    def __init__(self, connections_id, properties, source, target, bound,
                 edge):
        self.__id = connections_id
        self._properties = properties
        self.__source = source
        self.__target = target
        self.__bound = bound
        self.__edge = edge

    @property
    def id(self):
        return self.__id

    @property
    def properties(self):
        return self._properties

    @property
    def source(self):
        return self.__source

    @property
    def target(self):
        return self.__target

    @property
    def bound(self):
        return self.__bound

    @property
    def edge(self):
        return self.__edge

    @classmethod
    def from_json(cls, json_data):
        return cls(json_data['$id'], json_data['properties'],
                   json_data['fr'], json_data['to'],
                   loads(json_data['bound']), loads(json_data['edge']))

    def to_json(self):
        return {
            '$id': self.__id,
            'properties': self._properties,
            'source': self.__source,
            'target': self.__target,
            'bound': self.__bound.wkt,
            'edge': self.__edge.wkt
        }
