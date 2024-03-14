"""
File Name: rlines.py

Copyright (c) 2023 - 2024 IndoorJson

Author: Ziwei Xiang <knightzz1016@gmail.com>
Create Date: 2024/3/14
"""


class Rlines:
    def __init__(self, rlines_id, cells, ins, outs, closure):
        self.__id = rlines_id
        self.__cells = cells
        self.__ins = ins
        self.__outs = outs
        self.__closure = closure

    @property
    def id(self):
        return self.__id

    @property
    def cells(self):
        return self.__cells

    @property
    def ins(self):
        return self.__ins

    @property
    def outs(self):
        return self.__outs

    @property
    def closure(self):
        return self.__closure

    @classmethod
    def from_json(cls, json_data):
        return cls(json_data['$id'], json_data['cell'], json_data['ins'], json_data['outs'], json_data['closure'])

    def to_json(self):
        return {
            '$id': self.__id,
            'cell': self.__cells,
            'ins': self.__ins,
            'outs': self.__outs,
            'closure': self.__closure
        }
