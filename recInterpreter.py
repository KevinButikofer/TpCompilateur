import AST
from AST import addToClass
from functools import reduce
operations = {
    '+' : lambda x,y: x.value + y.value,
    '-' : lambda x,y: x.value - y.value,
    '*' : lambda x,y: x.value * y.value,
    '/' : lambda x,y: x.value / y.value,
}
class myToken:    
    value = None
    type = None
    def __init__(self, type, value=None):
        self.type = type
        self.value = value
        
    def __str__(self):
        return str(self.value)
    

vars ={}

@addToClass(AST.ProgramNode)
def execute(self):
    for c in self.children:
        c.execute()
    
@addToClass(AST.TokenNode)
def execute(self):
    if isinstance(self.tok, str):
        try:
            return vars[self.tok]
        except KeyError:
            print ("*** Error: variable %s undefined!" % self.tok)
    return self.tok

@addToClass(AST.OpNode)
def execute(self):
    args = [c.execute() for c in self.children]
    if len(args) == 1:
        args.insert(0,0)
    opType = None
    for i, tok in enumerate(args):        
        if type(tok) == myToken:
            if opType == type(tok.value):
                continue
            elif opType == None:
                opType = type(tok.value)
            else :
                print("*** Error : value must be of the same type")                
        else:
            if type(tok) == int:
                args[i] = myToken('int', tok)
            if type(tok) == float:
                args[i] = myToken('float', tok)
            if type(tok) == bool:
                args[i] = myToken('bool', tok)
            if type(tok) == str:
                args[i] = myToken('string', tok)
            if opType == type(tok):
                continue
            elif opType == None:
                opType = type(tok)
            else :
                print("*** Error : value must be of the same type")
                
    return reduce(operations[self.op], args)

@addToClass(AST.AssignNode)
def execute(self):
    vars[self.children[0].tok].value = self.children[1].execute()

@addToClass(AST.DeclarationNode)
def execute(self):
    vars[self.children[0].tok] = myToken(self.children[1])

@addToClass(AST.PrintNode)
def execute(self):
    print (self.children[0].execute())
    
@addToClass(AST.WhileNode)
def execute(self):
    while self.children[0].execute():
        self.children[1].execute()

if __name__ == "__main__":
    from parser5 import parse
    import sys
    prog = open(sys.argv[1]).read()
    ast = parse(prog)
    
    ast.execute()