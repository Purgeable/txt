# -*- coding: utf-8 -*-
"""
Simple notepad.exe notes parser. 

Aims to convert .txt file to a datastructure of tasks 
with subtasks/timestamps. Similar in spririt to 
*todotxt.com*

TODO: - see todo1 and todo 2 in code below
      - splitting newly added code to testable/'does 
        one thing' functions highly encoraged 
        
NOT TODO: - read ordered dict from yaml
"""

import yaml
from datetime import datetime
import re


ref_yaml_parsed = {'worktitle': [   
  ['', '23:30 06.02.2016', '', 'subtask description 1']
, ['', '23:30 06.02.2016', '23:36 06.02.2016', 'subtask description 2']
, ['', '23:30 06.02.2016', '', 'subtask description 3']
]}


def subtask_to_list(s):
    result = ['']
    dt_pattern = r'[012]\d:\d\d [0123]\d\.[01]\d\.\d\d\d\d'
    result += re.findall(dt_pattern, s)
    result += [''] if len(result) == 2 else []
    result.append(re.sub(dt_pattern, '', s, count=2).strip())
    return result


# for reference
# print (yaml.dump(ref_yaml_parsed))

doc1 = """worktitle:
- subtask description 23:30 06.02.2016
- 23:30 06.02.2016 23:36 06.02.2016 subtask description 2
- [s] 23:30 06.02.2016 subtask description 3"""


def parse_yml(string):
    parsed = yaml.parse(doc1)
    for k, v in parsed.iteritems():
        if type(v) == list:
            parsed[k] = subtask_to_list(v)
    return parsed

# assert parse_yml(doc1) == ref_yaml_parsed

ref_dt = datetime(2016, 2, 6, 23, 30)

def ts_to_datetime(timestamp):
    return datetime.strptime(timestamp, '%H:%M %d.%m.%Y')

assert ref_dt == ts_to_datetime('23:30 06.02.2016')
