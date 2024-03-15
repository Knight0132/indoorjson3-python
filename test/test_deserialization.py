"""
File Name: test_deserialization.py

Copyright (c) 2023 - 2024 IndoorJson

Author: Ziwei Xiang <knightzz1016@gmail.com>
Create Date: 2024/3/13
"""

import json
import sys
import os
import unittest

sys.path.append(os.path.abspath('../src'))

from serialization import serialization, deserialization


class TestDeserialization(unittest.TestCase):

    def test_deserialization(self):

        with open('example.json', 'r') as file:
            original_json = json.load(file)

        indoorSpace = deserialization('example.json')

        generated_json = 'test_deserialization.json'

        serialization(generated_json, indoorSpace)

        with open(generated_json, 'r') as file:
            generated_json = json.load(file)

        self.assertEqual(original_json, generated_json)


if __name__ == '__main__':
    unittest.main()
