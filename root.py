# -*- coding: utf-8 -*-

"""todolist data structure in todo_item.go
type Todo struct {
	Id            int      `json:"id"`
	Subject       string   `json:"subject"`
	Projects      []string `json:"projects"`
	Contexts      []string `json:"contexts"`
	Due           string   `json:"due"`
	Completed     bool     `json:"completed"`
	CompletedDate string   `json:"completedDate"`
	Archived      bool     `json:"archived"`
	IsPriority    bool     `json:"isPriority"`
}
"""

from collections import OrderedDict

# requirements.txt: dataset, docopt
import dataset

# TODO: 
# testing of cli interface
#     python todo new subj: <subj> +<project> @<context> due: <date_tag> s: <status>
#     python todo e # subj:
#     python todo l # 

    
# cli interface for
#    new task
#    list all tasks
#    edit task by number
#    list task by project 
#    list task by context

# query database:    
#    filter by project
#    filter by context
#    filter by dates    

# database:    
#    dump database to file         
#    read file from database

    
# LATER:
#    rebase item names as 1, 2, 3...    
#    no subtasks
#    compile to exe
#    2 [?>w+xf] Write more code +whole new project 
"""
? > not specified, no todo
...
"""


# LIMITATIONS:
#    one project per task
#    one context per task
#    flat tasks, not subtasks    
#    no clocker 
#    no color
#    no priority

def mask_None_with_empty_string(v: str):
    if v is not None:
        return str(v)
    else:
        return '' 

assert mask_None_with_empty_string('a') == 'a'
assert mask_None_with_empty_string(None) == ''
assert mask_None_with_empty_string(1) == '1'

 
def format_output(key, value):
    if key == 'project':
        if value:
            return key, "+{}".format(value)
    if key == 'context':
        if value:
            return key, "@{}".format(value)
    return key, mask_None_with_empty_string(value)       

assert format_output('id', '1') == ('id', '1')
assert format_output('project', 'interview') == ('project', '+interview')
assert format_output('context', 'home') == ('context', '@home') 

def supported_keys():
    return list(get_default_dict().keys())
    
def get_default_dict():
    return OrderedDict(id=None
                , subject=''
                , project=''
                , context=''
                , due=None
                , completed=False
                , completed_date=None
                , archived = False
                , is_priority = False)
    
def check_keys(input_dict):
    not_supported = [key for key in input_dict.keys() 
                     if key not in Task.FIELDS]        
    if not_supported:
         raise KeyError("{} must be in {}".format(not_supported,
                                                  supported_keys))        

class Task: 
    
    FIELDS = supported_keys()
    
    def __init__(self, input_dict):
        check_keys(input_dict)
        self.dict = input_dict

    def as_dict(self):
        return self.dict
    
    def as_formatted_dict(self):
        odict = OrderedDict()
        for key in self.FIELDS:
            if key in self.dict.keys():
                value = self.dict[key]
                k, v = format_output(key, value)
                odict.update({k: v})
        return odict    
    
    def __repr__(self):
        return "Task({})".format(self.dict.__repr__())        
    
    def __str__(self):
        row = [v for v in self.as_formatted_dict().values()]
        return " ".join(row)
        
    def __eq__(self, x):
        return bool(self.dict == x.dict)


#fixture
d1 = dict(context='home', subject='repair kitchen sink', id=0)
t1 = Task(d1)

#test Task methods
assert t1.as_dict() == d1
assert t1.as_formatted_dict() == OrderedDict([('id', '0'),
             ('subject', 'repair kitchen sink'),
             ('context', '@home')])
assert str(t1) == '0 repair kitchen sink @home'
assert repr(t1).startswith("Task")
class MockDict:
    dict = d1
assert t1 == MockDict     


class TaskList:
    
    def __init__(self, table):
        """Set *table* pointer to work with database."""
        self.table = table

    def _insert(self, **kwarg):
        """
        Usage:
            
            tasklist.add(subject='Wash laundry', context='home')
        
        will do:
            
            table.insert(dict(subject='Wash laundry', context='home'))

        """        
        return self.table.insert(kwarg)
    
    def _update(self, dictionary):
        return self.table.update(dictionary, keys=['id'])
   
    def save_new_task(self, task):
        """Save *task* to database. Ignores 'id' field
        
        Can make duplicates of existing rows.
        
        Returns:
            integer: task identificator
        """        
        d = task.as_dict()
        try:
            del d['id']
        except KeyError:
            pass
        return self._insert(**d)

    def save_existing_task(self, task):
        """Save existing *task* to database.
        
        Returns:
            integer: task identificator
        """        
        return self._update(task.as_dict())

    def get_task(self, i: int): 
        """Get task with identificator *i*.
        
        Returns:
            Task instance, or
            False, if *i* is not a valid id.` 
        """
        row_dict = self.table.find_one(id=i)
        if row_dict is not None:
            return Task(row_dict)
        else:
            return False
        
    def query(self, project=None, context=None):
        """Yields:
            Task instance
        """
        search_dict = {}
        if project:
            search_dict['project'] = project  
        if context:
            search_dict['context'] = context
        results = self.table.find(**search_dict)    
        for res in results:
            yield Task(res)
        
    def yield_all(self):
        """Yields:
            Task instance
        """
        results = self.table.all()
        for res in results:
            yield Task(res)

            
class Presentation:     
    
    def __init__(self, tasklist):
        self.tasklist = tasklist        
    
    def print(self):
        for t in self.tasklist.yield_all():            
            print (t)

    def filter(self, project=None, context=None):
        for t in self.tasklist.query(project, context):            
            print (t)




# sample entries - a fixture
db = dataset.connect('sqlite:///:memory:')
table = db['tasks']
tasklist = TaskList(table)

a = table.insert(dict(subject='Wash laundry', context='home'))
b = table.insert(dict(subject='Write more code', project='github'))
table.delete(id=1)
c = table.insert(dict(subject='Iron clothes', context='home'))
tasklist._insert(subject='Развесить одежду сушиться', context='home')

# get item, alter item, save to database, query again 
t = tasklist.get_task(2)
t.dict['project'] = "whole new project"
tasklist.save_existing_task(t)
z = tasklist.get_task(2)
assert t == z

#make task
tasklist.save_new_task(t)

# test print() method is callable
presentation = Presentation(tasklist)
presentation.print()
print("---")
presentation.filter(context='home')