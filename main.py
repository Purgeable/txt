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
    'last checked': datetime(2016, 2, 6, 23, 30),
    'started':      None,
    'ended':        None,
    'desc':         'subtask description 3'
}


def is_task(s):
    return not s.startswith((' ', '\t'))

def is_subtask(s):
    return s.startswith((' ', '\t'))

def lines(doc):
    # question: что делает filter
    #           что такое False в .splitlines(False)
    #           чем это лучше doc.split('\n')
    #
    # answer:   filter в данном случае отбросит все пустые строки.
    #           А вообще фильтр filter(ff, collection) оставляет только 
    #           те элементы коллекции на которых функция ff принимает значение True.
    #           Если ff это None, то используется id функция, возвращающая сам объект.
    #           Такое использование не очень то наглядно, но вполне общепринято,
    #           насколько я могу судить.
    #
    #           False означает, что в конце разбитых строчек \n не нужен
    #
    #           splitlines разобъет строчки и в случае использования в тексте 
    #           Windows переносов строк ('\r\n')
    return filter(None, doc.splitlines(False))

def parse_tasks(doc):
    tasks = []
    for line in lines(doc):
        if is_task(line):
            # note: line.strip() may be substituted with parse_subtask(line), but different test is needed
            tasks.append({'title': line.strip(),
                       'subtasks': []})
        elif is_subtask(line):
            # add to previous element in list 
            tasks[-1]['subtasks'].append(parse_subtask(line))
    return tasks

z = parse_tasks(doc2) 
ref = [{'title':'worktitle', 'subtasks':[ds,ds]},
                            {'title':'worktitle2', 'subtasks':[ds,ds]}]
assert z == ref


# alternative rules:
#
# timestamp
# some work
# empty line - do nothing 
#

# workflow:
#    reorder and overwrite 
#    file statistics
#
