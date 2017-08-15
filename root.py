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
import dataset 

# TODO: 
#    dump database to file         
#    read file from database

# LATER:
#    rebase item names as 1, 2, 3...    
#    no subtasks

# LIMITATIONS:
#    one project per task
#    one сщтеуче per task
    

def mask_None_with_empty_string(s: str):
    if s:
        return str(s)
    else:
        return '' 


class Task:
    
    def __init__(self, input_dict):
        self.dict = input_dict
        
    def as_dict(self):
        return self.dict
    
    def get_id(self):
        return self.dict['id']
    
    def __repr__(self):
        return self.dict.__repr__()        
        
    def __str__(self):
        if self.dict['project']:
            self.dict['project'] = "+{}".format(self.dict['project']) 
        if self.dict['context']:
            self.dict['context'] = "@{}".format(self.dict['context'])    
        row = [mask_None_with_empty_string(v) for v in self.dict.values()]
        return " ".join(row)
        
    def __eq__(self, x):
        return bool(self.dict ==  x.dict)

class TaskList:
    
    def __init__(self, table):
        self.table = table
        # FIXME: init with connection 
        # relies on global *table* connection, better if injected

    def add(self, **kwarg):
        return self.table.insert(kwarg)
    
    def update(self, _dict):
        self.table.update(_dict, keys=['id'])

    def get_task(self, _id: int): 
        try:
            row_dict = self.table.find(id=_id).next()
            return Task(row_dict)
        except StopIteration: 
            return False

    def write_task(self, task):
        # write task at same id as before
        self.update(task.as_dict())
    
    def all(self):
        results = self.table.all()
        for res in results:
            yield Task(res)

            
class Presentation:     
    
    def __init__(self, tasklist):
        self.tasklist = tasklist        
    
    def print(self):
        for t in self.tasklist.all():            
            print (t)


# sample entries - a fixture
db = dataset.connect('sqlite:///:memory:')
table = db['tasks']

a = table.insert(dict(subject='Wash laundry', context='home'))
b = table.insert(dict(subject='Write more code', project='github'))
table.delete(id=1)
c = table.insert(dict(subject='Iron clothes', context='home'))
tasklist = TaskList(table)
tasklist.add(subject='Развесить одежду сушиться', context='home')

# test this method is callable
presentation = Presentation(tasklist)
presentation.print()

# get item, alter item, save to database, query again 
t = tasklist.get_task(2)
t.dict['project'] = "whole new project"
tasklist.write_task(t)
z = tasklist.get_task(2)
assert t == z