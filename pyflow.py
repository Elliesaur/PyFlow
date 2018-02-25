from __init__ import *
from transformers.injector import Injector
from transformers.block import Block
from transformers.constants import Constants
from transformers.flow import Flow
from transformers.proxy import Proxy

# Can add Flow() to this
obfs = [Proxy(), Flow(), Constants(), Flow(), Proxy(), Constants()]

# Open the test file 
root = ast.parse(open('obftest.py', 'r').read())

for obf in obfs:
    root = obf.visit(root)
    src = codegen.to_source(root)


file = open('test.py', 'w')
file.write(src)
file.close()
