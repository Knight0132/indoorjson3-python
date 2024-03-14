"""
File Name: layer.py

Copyright (c) 2023 - 2024 IndoorJson

Author: Ziwei Xiang <knightzz1016@gmail.com>
Create Date: 2024/3/14
"""


class Layer:
    def __init__(self, layer_id, cells):
        self.__id = layer_id
        self.__cells = cells

    @property
    def id(self):
        return self.__id

    @property
    def cells(self):
        return self.__cells

    @classmethod
    def from_json(cls, json_data):
        return cls(json_data['$id'], json_data['cells'])

    def to_json(self):
        return {
            '$id': self.__id,
            'cells': self.__cells
        }
