""" $lic$
Copyright (C) 2016-2017 by The Board of Trustees of Stanford University

This program is free software: you can redistribute it and/or modify it under
the terms of the Modified BSD-3 License as published by the Open Source
Initiative.

If you use this program in your research, we request that you reference the
TETRIS paper ("TETRIS: Scalable and Efficient Neural Network Acceleration with
3D Memory", in ASPLOS'17. April, 2017), and that you send us a citation of your
work.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the BSD-3 License for more details.

You should have received a copy of the Modified BSD-3 License along with this
program. If not, see <https://opensource.org/licenses/BSD-3-Clause>.
"""

import unittest

import os
import subprocess

class TestNNDataflowSearch(unittest.TestCase):
    ''' Tests for NN dataflow search tool. '''

    def setUp(self):
        cwd = os.path.dirname(os.path.abspath(__file__))
        self.cwd = os.path.join(cwd, '..', '..', '..')
        self.assertTrue(os.path.isdir(self.cwd))
        self.assertTrue(os.path.isdir(
            os.path.join(self.cwd, 'nn_dataflow', 'tools')))

        self.args = ['python', 'nn_dataflow/tools/nn_dataflow_search.py',
                     'alex_net', '--batch', '1',
                     '--node', '1', '1', '--array', '16', '16',
                     '--regf', '512', '--gbuf', '131072']

    def test_default_invoke(self):
        ''' Default invoke. '''
        ret = self._call(self.args)
        self.assertEqual(ret, 0)

    def test_3d_mem(self):
        ''' With 3D memory. '''
        ret = self._call(self.args + ['--mem-type', '3D'])
        self.assertEqual(ret, 0)

    def test_no_dataflow(self):
        ''' No dataflow scheme found. '''
        args = self.args[:]
        args[args.index('--gbuf') + 1] = '2'
        args += ['--disable-bypass', 'i', 'o', 'f']
        ret = self._call(args)
        self.assertEqual(ret, 2)

    def _call(self, args):
        return subprocess.call(args, cwd=self.cwd,
                               stderr=subprocess.STDOUT,
                               stdout=open(os.devnull, 'w'))

