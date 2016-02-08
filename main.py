# -*- coding: utf-8 -*-
"""
Simple notepad.exe notes parser. 

Aims to convert .txt file to a datastructure of tasks 
with subtasks/timestamps. Similar in spririt to *todotxt.com*
"""

import yaml
from datetime import datetime
import re

doc1 = """worktitle:
- subtask description 23:30 06.02.2016
- 23:30 06.02.2016 23:36 06.02.2016 subtask description 2
- [s] 23:30 06.02.2016 subtask description 3"""

doc2 = """worktitle
    subtask description 23:30 06.02.2016
    23:30 06.02.2016 23:36 06.02.2016 subtask description 2
    [s] 23:30 06.02.2016 subtask description 3"""
#rules for parsing doc2:
#    text starting with no offset (at start of string) is title
#    four spaces offset is subtask line 
#    single letter in square brackets anywhere in subtask line is status flag 
#    one timestamp is 'last checked' date and time 
#    two timestamps is 'started' and 'ended' date and time 
#    remaining text after popping out status and timestamp(s) is 'desc'

subtask_dict_sample = {'status':'s', 
'last checked': None, 
'started': datetime(2016, 2, 6, 23, 30), 
'ended': datetime(2016, 2, 9, 2, 30),
'desc': 'subtask description 3'}

assert subtask_dict_sample == parse_subtask('[s] 23:30 06.02.2016 ... 2:30 09.02.2016 subtask description 3') 
assert subtask_dict_sample == parse_subtask('[s] 23:30 06.02.2016 2:30 09.02.2016 subtask description 3')
assert subtask_dict_sample == parse_subtask('[s] subtask description 3 23:30 06.02.2016 2:30 09.02.2016')

ref_yaml_parsed = {'worktitle': [   
  [ '', '23:30 06.02.2016', '', 'subtask description 1']
, [ '', '23:30 06.02.2016', '23:36 06.02.2016', 'subtask description 2']
, ['s', '23:30 06.02.2016', '', 'subtask description 3']
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
