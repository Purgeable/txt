from datetime import datetime

from main import ts_to_datetime, get_status_letter, get_datetime_list, get_description, parse_subtask

assert ts_to_datetime('23:30 06.02.2016')    == datetime(2016, 2, 6, 23, 30)
assert ts_to_datetime(' 23:30 06.02.2016  ') == datetime(2016, 2, 6, 23, 30)


assert get_status_letter('[s] [z]') == 's'
assert get_status_letter('[s][z]') == 's'
assert get_status_letter('dd [] sdff [s]  [z]') == 's'
assert get_status_letter('[abc]') is None


assert get_datetime_list(' some [a] 23:30 06.02.2016 description') == [datetime(2016, 2, 6, 23, 30)]


datetime_list_sample = [
    datetime(2016, 2, 6, 23, 30),
    datetime(2016, 2, 6, 23, 31)]
assert get_datetime_list('    some [a] 23:30 06.02.2016 23:31 06.02.2016 description') == datetime_list_sample
assert get_datetime_list('    some [a] 23:30 06.02.2016 fd 23:31 06.02.2016 description') == datetime_list_sample


assert get_description('    some [a] 23:30 06.02.2016 description') == 'some description'
assert get_description('    some [a] 23:30 06.02.2016 23:30 06.02.2016 description') == 'some description'
assert get_description('    [a] some 23:30 06.02.2016 description') == 'some description'
assert get_description('    [a] 23:30 06.02.2016 some description') == 'some description'
assert get_description('    [a] 23:30 06.02.2016 some description ') == 'some description'
assert get_description('    [a]  23:30 06.02.2016 some description ') == 'some description'
assert get_description('    [a] 23:30 06.02.2016  some description ') == 'some description'
assert get_description('    some [a] 23:30 06.02.2016 ... 23:30 06.02.2016 description') == 'some ... description'


subtask_dict_sample = {
    'status': 's',
    'last checked': None,
    'started':      datetime(2016, 2, 6, 23, 30),
    'ended':        datetime(2016, 2, 9, 2, 30),
    'desc':         'subtask description 3'
}


assert subtask_dict_sample == parse_subtask('[s] 23:30 06.02.2016 2:30 09.02.2016 subtask description 3')
assert subtask_dict_sample == parse_subtask('[s] subtask description 3 23:30 06.02.2016 2:30 09.02.2016')
assert subtask_dict_sample == parse_subtask('[s]    subtask description 3     23:30 06.02.2016    2:30 09.02.2016   ')