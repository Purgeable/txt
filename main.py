# -*- coding: utf-8 -*-
"""
Simple windows notepad.exe todo notes parser 
 - makes use of F5 timestamp in notepad.exe: 23:30 06.02.2016
 - aims to convert .txt file to a datastructure of tasks with subtasks/timestamps. 
 - similar in spirit to http://todotxt.com/
"""

# *** Rules section *** 

#Rules for parsing doc2:
#    text starting with no offset (at start of string) is title
#    four spaces offset is subtask line 

# parsing subtasks 
#    single letter in square brackets anywhere in subtask line is status flag + only one [x] is taken 
#    one timestamp is 'last checked' date and time 
#    two timestamps is 'started' and 'ended' date and time 
#    remaining text after popping out status and timestamp(s) is 'desc'


from datetime import datetime
from copy import deepcopy
import re

def ts_to_datetime(timestamp):
    """Converts notepad.exe timestamp to datetime instance"""
    return datetime.strptime(timestamp.strip(), '%H:%M %d.%m.%Y')

# catches one letter inside brackets, like '[d]'
STATUS_PAT = re.compile(r'\s*\[\s*(\w)\s*\]\s*')

# catches notepad.exe F5 timestamp
DATETIME_PAT = re.compile(r'\s*([012]?\d:\d\d [0123]\d\.[01]\d\.\d\d\d\d)\s*')

def get_status_letter(string, status_re = STATUS_PAT):
    """Return a letter inside first brackets"""
    # will skip any '[x]' in '[y] [x] [x]' after first occurence of  '[y]' 
    status_list = status_re.findall(string)
    if len(status_list) > 0:
        return status_list[0]

def get_datetime_list(string, datetime_re = DATETIME_PAT):
    return [ts_to_datetime(ts) for ts in datetime_re.findall(string)]

def get_description(s, status_re = STATUS_PAT, datetime_re = DATETIME_PAT):
    s = datetime_re.sub(' ', s)
    s = status_re.sub(' ', s)
    return s.strip()

def parse_subtask(str_):
    result = {
        'status': None,
        'last checked': None,
        'started': None,
        'ended': None,
        'desc': ''
    }

    # get status letter like 's' from '[s]' 
    result['status'] = get_status_letter(str_)

    # get timestamps, allocate to dictionary 
    datetime_list = get_datetime_list(str_)
    if len(datetime_list) == 1:
        result['last checked'] = datetime_list[0]
    elif len(datetime_list) == 2:
        result['started'] = datetime_list[0]
        result['ended'] = datetime_list[1]
    else:
        # not date provided 
        pass    

    # get test line description for subtask
    result['desc'] = get_description(str_)

    return result


doc2 = """worktitle
    [s] 23:30 06.02.2016 subtask description 3
    [s] 23:30 06.02.2016 subtask description 3
worktitle2
    [s] 23:30 06.02.2016 subtask description 3
    [s] 23:30 06.02.2016 subtask description 3
"""

ds = {
    'status': 's',
    'last checked': None,
    'started':      datetime(2016, 2, 6, 23, 30),
    'ended':        datetime(2016, 2, 9, 2, 30),
    'desc':         'subtask description 3'
}

def is_task(s):
    if len(s) == 0:
        return False
    return (s[0] != ' ') and (s[0] != '\t')


def is_subtask(s):
    if len(s) == 0:
        return False
    return (s[0] == ' ') or (s[0] == '\t')


def parse_tasks(doc):
    tasks = []
    one_task_template = {
        'title': None,
        'subtasks': []
    }
    one_task = deepcopy(one_task_template)
    for line in filter(None, doc.splitlines(False)):
        if is_task(line):
            if one_task['title'] is not None:
                tasks.append(one_task)
                one_task = deepcopy(one_task_template)
            one_task['title'] = line.strip()
        elif is_subtask(line):
            one_task['subtasks'].append(parse_subtask(line))
    if one_task['title'] is not None:
        tasks.append(one_task)
    return tasks


assert parse_tasks(doc2) == [{'title':'worktitle', 'subtasks':[ds,ds]},
                            {'title':'worktitle2', 'subtasks':[ds,ds]}]
