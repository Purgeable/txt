import unittest
import datetime

from main import *
from pprint import pprint


doc1 = """worktitle:
- subtask description 23:30 06.02.2016
- 23:30 06.02.2016 23:36 06.02.2016 subtask description 2"""


ref_yaml_parsed = {'worktitle': [
  ['', '23:30 06.02.2016', '', 'subtask description 1']
, ['', '23:30 06.02.2016', '23:36 06.02.2016', 'subtask description 2']
]}


class TestNotesParser(unittest.TestCase):

    def test_subtask_to_list(self):
        subtask1 = 'subtask description 1 23:30 06.02.2016'
        subtask2 = '23:30 06.02.2016 23:36 06.02.2016 subtask description 2'

        self.assertEqual(['', '23:30 06.02.2016', '', 'subtask description 1'],
                         subtask_to_list(subtask1))
        self.assertEqual(['', '23:30 06.02.2016', '23:36 06.02.2016', 'subtask description 2'],
                         subtask_to_list(subtask2))

    def test_ts_to_datetime(self):
        self.assertEqual(ref_dt, ts_to_datetime('23:30 06.02.2016'))

    def test_parse_yml(self):
        self.skipTest('parse_yml function is not finished yet')
        z = yaml.load(doc1)
        pprint(z)
        self.assertEqual(ref_yaml_parsed, parse_yml(doc1))