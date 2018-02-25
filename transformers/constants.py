from transformers import *
from .helper import id_generator

# XOR
from itertools import cycle
from zlib import compress


# CONSTANT TRANSFORMER
# Method could take a type as a parameter
# Cast to that type at end (using str(value), int(value), float(value))
# See injection.py for relevant injected functions
class Constants(NodeTransformer):
    def __init__(self):
        ast.NodeTransformer.__init__(self)
        self.injected_method = False
        
    def visit_Module(self, node):
        
        # Inject decryption method into module if not done
        if not self.injected_method:
            self.decrypter_func_name = id_generator(random.randint(10, 20))                         
            self.inject_method(node, 'decrypt_constant', self.decrypter_func_name)
            self.injected_method = True
            
        self.generic_visit(node)
        return node
    
    def visit_Str(self, node):
        
        value = node.s

        if value == '':
            return node

        key = id_generator(random.randint(16, 32))
        value = self.encrypt_constant(value, key)
        
        dec_call = Call(func=Name(id=self.decrypter_func_name, ctx=Load()), args=[
            Str(s=value),
            Str(s=key),
            Name(id='str', ctx=Load())
          ], keywords=[])
        
        return dec_call
    
    def visit_Num(self, node):

        value = node.n

        key = id_generator(random.randint(16, 32))

        typ = 'int'
        if isinstance(value, float):
            typ = 'float'
            
        value = self.encrypt_constant(value, key)

        dec_call = Call(func=Name(id=self.decrypter_func_name, ctx=Load()), args=[
            Str(s=value),
            Str(s=key),
            Name(id=typ, ctx=Load())
          ], keywords=[])

        return dec_call
    
    def encrypt_constant(self, constant, key):
        return ''.join(chr(ord(c)^ord(k)) for c,k in zip(str(constant), cycle(key)))
        #return compress(''.join(chr(ord(c)^ord(k)) for c,k in zip(str(constant), cycle(key))).encode("utf-8"), 9).hex()    

    def inject_method(self, target_module_node, inject_func_name, new_name):
        inj = Injector(target_module_node, inject_func_name, new_name)
        inj_root = ast.parse(open('payload.py', 'rb').read())
        inj_root = inj.visit(inj_root)
