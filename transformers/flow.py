from transformers import *
from .helper import id_generator

# CFLOW TRANSFORMER        
class Flow(NodeTransformer):
    def __init__(self):
        ast.NodeTransformer.__init__(self)
		
        # Added to the end of every "switch" variable
        self.switch_var_num = 0

    def visit_Module(self, node):

        # Apply cflow
        self.change_node_body_flow(node, node.body)
        
        self.generic_visit(node)
        return node
    
    def visit_While(self, node):

        # Stop recursion
        if not isinstance(node.body[0], If):
            self.change_node_body_flow(node, node.body)
            
        self.generic_visit(node)
        return node
    
    def visit_For(self, node):

        # Stop recursion
        if not isinstance(node.body[0], If):
            self.change_node_body_flow(node, node.body)
            
        self.generic_visit(node)
        return node
    
    def visit_FunctionDef(self, node):
        
        self.change_node_body_flow(node, node.body)
            
        self.generic_visit(node)
        return node
    
    def visit_ClassDef(self, node):
        
        self.change_node_body_flow(node, node.body)
            
        self.generic_visit(node)
        return node
    
    def visit_If(self, node):
        
        # Stop recursion
        if not isinstance(node.body[-1], Assign) and not isinstance(node.body[-1], Break):
            self.change_node_body_flow(node, node.body)
        if not len(node.orelse) == 0 and not isinstance(node.orelse[-1], Assign) and not isinstance(node.orelse[-1], Break):
            self.change_node_body_flow(node, node.orelse)
            
        self.generic_visit(node)
        return node

    def change_node_body_flow(self, node, body):

        if (len(body) == 0):
            return
        
        blocks = []

        indexes = {}
        index = 0
        
        # Create new Block set
        for b_node in body:
            blocks.append(Block(b_node, index, b_node == body[-1]))
            indexes[str(index)] = id_generator(random.randint(6, 15))
            index += 1
            
        first_index = indexes[str(blocks[0].get_index())]

        # Shuffle blocks
        random.shuffle(blocks)

        # Clear node body
        body.clear()

        while_loop = While(test=NameConstant(value=True), body=[], orelse=[]);
        switch_var = Name(id=id_generator(random.randint(4, 12)) + str(self.switch_var_num), ctx=Load())

        self.switch_var_num += 1
        
        # Assign to first index in blocks
        body.append(Assign(targets=[Name(id=switch_var.id, ctx=Store())], value=Str(s=first_index)))
        
        # Build if statements
        for x in blocks:
            next_index = str(x.get_next_index())

            if (next_index in indexes):
                next_index = indexes[next_index]
                
            while_loop.body.append(If(test=x.get_compare(switch_var, indexes[str(x.get_index())]),
                body=[
                    x.get_node(),
                    x.get_update_instr(switch_var, next_index)
                ], orelse=[]));

        body.append(while_loop)
