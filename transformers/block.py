from transformers import *

class Block(object):
    def __init__(self, node, index, is_last):
        self.index = index
        self.node = node
        self.next_index = index + 1
        self.is_last = is_last

    def get_next_index(self):
        return self.next_index

    def get_index(self):
        return self.index

    def get_node(self):
        return self.node

    def get_compare(self, variable, index):
        return Compare(left=variable, ops=[Eq()], comparators=[Str(s=index)])
    
    def get_update_instr(self, variable, next_index):
        if not self.is_last:
            return Assign(targets=[Name(id=variable.id, ctx=Store())], value=Str(s=next_index))
        else:
            return Break()
    
    def __str__(self):
        return str(self.index) + ': ' + str(self.node) + ' (next: ' + str(self.next_index) + ')'
