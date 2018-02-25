from transformers import *
from .helper import id_generator
import astor
from astor import codegen

# PROXY CALL TRANSFORMER
class Proxy(NodeTransformer):
    def __init__(self):
        ast.NodeTransformer.__init__(self)
        self.injected_dict = False
        
        self.call_dict_name = id_generator(random.randint(6, 18))
        self.call_dict_node = None
        self.call_dict = {}
        self.call_dict_data = []
        
        self.module_node = None
        self.skip_calls = 0

        
    def visit_Module(self, node):
        
        # Inject dict containing blank calls into module if not done
        if not self.injected_dict:
            tmp = node
            self.module_node = tmp
            self.call_dict_node = Assign(targets=[Name(id=self.call_dict_name, ctx=Store())], value=Dict(keys=[], values=[]))

            node.body.insert(0, self.call_dict_node)
            self.injected_dict = True

        #parent = None
        for n in ast.walk(node):
            
            if isinstance(n, Call):
                n = self.handle_Call_eval(n)
                
        return node

    def handle_Call(self, node):

        (parent, child_in_parent) = self.find_parent(node)
        print('Parent:',parent,'First Child:',child_in_parent)
        print('-'*36)
        # Add call to dict
        key = id_generator(random.randint(16, 32))
        while key in self.call_dict.keys():
            key = id_generator(random.randint(16, 32))

        self.call_dict[key] = node.func
        
        # Write to dictionary
        self.call_dict_data.append(Assign(targets=[Subscript(value=Name(id=self.call_dict_name, ctx=Load()), slice=Index(value=Str(s=key)), ctx=Store())], value=node.func))

        # Insert the element to dict after it is defined.
        (field, index) = self.find_index(parent, child_in_parent)
        
        parent.body.insert(index, self.call_dict_data[-1])
        
        
        # Return new call
        node.func = Subscript(value=Name(id=self.call_dict_name, ctx=Load()), slice=Index(value=Str(s=key)), ctx=Load())
        return node
    
    def handle_Call_eval(self, node):

        #(parent, child_in_parent) = self.find_parent(node)
        
        
        # Return new call
        e = self.get_eval_node(node)
        node.func = e.func
        node.args = e.args
        node.keywords = e.keywords
        return node
    
    def get_eval_node(self, call):
        e = codegen.to_source(call)
        e = e.strip()
        return Call(func=Name(id='eval', ctx=Load()), args=[Str(s=e)], keywords=[])

    def find_index(self, parent, child):
        index = 0

        for field, value in ast.iter_fields(parent):
            print(field, value)
            if isinstance(value, list):
                index = self.find_index_internal(value, child)
                if index != -1:
                    return (field, index) 
            elif child == value:
                return ('NoList', -1)
            
        return ('None', index)
    
    def find_index_internal(self, body, child):
        index = -1
        try:
            index = body.index(child)
        except ValueError:
            index = -1
        return index
        
    def find_parent(self, node):
        
        parent = self.find_parent_internal(node, self.module_node)
        n = parent
        child_in_parent = n


        child_parent_same = False
        while child_parent_same or not (isinstance(n, Module) or isinstance(n, ClassDef) or isinstance(n, FunctionDef) \
           or isinstance(n, IfExp) or isinstance(n, If) or isinstance(n, For) \
           or isinstance(n, While) or isinstance(n, Try) or isinstance(n, ExceptHandler) \
           or isinstance(n, With) \
           or isinstance(n, Lambda) or isinstance(n, AsyncFunctionDef) or isinstance(n, AsyncFor) \
           or isinstance(n, AsyncWith)):
            child_in_parent = n
            n = self.find_parent_internal(n, self.module_node)
            child_parent_same = child_in_parent == n
##        else:
##            child_parent_same = True
##            while child_parent_same or not (isinstance(n, Module) or isinstance(n, ClassDef) or isinstance(n, FunctionDef) \
##               or isinstance(n, IfExp) or isinstance(n, If) or isinstance(n, For) \
##               or isinstance(n, While) or isinstance(n, Try) or isinstance(n, ExceptHandler) \
##               or isinstance(n, With) \
##               or isinstance(n, Lambda) or isinstance(n, AsyncFunctionDef) or isinstance(n, AsyncFor) \
##               or isinstance(n, AsyncWith)):
##                child_in_parent = n
##                n = self.find_parent_internal(n, self.module_node)
##                child_parent_same = child_in_parent == n
            
        # Need to determine whether it is in a test list (condition for a while)
        # If it is, do not use the "parent", but instead the parents parent.
##        (field, index) = self.find_index(n, child_in_parent)
##        print(field)
##        if (field == 'NoList'):
##            return self.find_parent(n)
        
        return (n, child_in_parent)
    
    def find_parent_internal(self, node, iter_node):
        f = None
        for n in ast.iter_child_nodes(iter_node):
            if n == node:
                return iter_node
            f = self.find_parent_internal(node, n)
            if f != None:
                return f

        return f
