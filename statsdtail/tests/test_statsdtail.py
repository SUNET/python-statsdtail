# -*- coding: utf-8 -*-

import unittest
import re
from statsdtail.main import load_config

from os import path

__author__ = 'lundberg'


class StatsdTailTest(unittest.TestCase):

    def test_load_config(self):
        try:
            config = load_config('./tests/data/python-statsdtail.yaml')
        except FileNotFoundError:
            raise Exception('No config found in {}'.format(path.abspath(path.dirname(__file__))))
        self.assertEqual(config['core']['working_directory'], '/tmp/')
        self.assertEqual(len(config['patterns']), 2)
        self.assertTrue(isinstance(config['patterns']['test']['match'], type(re.compile(''))))

