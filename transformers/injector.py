from transformers import *

class Injector(NodeTransformer):

    def __init__(self, target_module_node, func_name, new_name):
        ast.NodeTransformer.__init__(self)
        self.func_name = func_name
        self.target_module_node = target_module_node
        self.new_name = new_name
        
    def visit_FunctionDef(self, node):
        if not node.name == self.func_name:
            return node

        tmp = node
        tmp.name = self.new_name
        
        # Inject into target module
        self.target_module_node.body.insert(0, tmp)

        # Do not generic visit
        return node
