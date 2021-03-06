import AST
from AST import addToClass
from functools import reduce

operations = {
    '+' : lambda x,y: x.value + y.value,
    '-' : lambda x,y: x.value - y.value,
    '*' : lambda x,y: x.value * y.value,
    '/' : lambda x,y: x.value / y.value,
}

conditions = {
    '<=' : lambda x,y: x.value <= y.value,
    '>=' : lambda x,y: x.value >= y.value,
    '<' : lambda x,y: x.value < y.value,
    '>' : lambda x,y: x.value > y.value,
    'cochon_egal_porc' : lambda x,y: x.value == y.value,
    'je_passe_mon_annee' : lambda x,y: x.value != y.value,
}

typeEnum = {
    'heberline' : 'int',
    'number' : 'float',
    'papier_crayon' : 'str',
    'jav' : 'bool',
}
class myToken:    
    value = None
    type = None
    def __init__(self, myType, value=None):        
            self.type = myType
            self.value = value     
    def setValue(self, val):
        #check for type when assignating value
        if self.type == type(val).__name__:
            self.value = val
        else:
            print ("*** Error: assignation error type aren't the same")
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
        #if it's a between quotes it's a string and note and identifier
        if self.tok[0] != '"' and self.tok[-1] != '"':            
            try:
                return vars[self.tok]
            except KeyError:
                print ("*** Error: variable %s undefined!" % self.tok)
        else:
            #remove the quotes
            return self.tok[1:-1]
    return self.tok

@addToClass(AST.OpNode)
def execute(self):
    args = [c.execute() for c in self.children]
    if len(args) == 1:
        args.insert(0,0)
    if checkType(args):
        return reduce(operations[self.op], args)
    else:
        return False


@addToClass(AST.AssignNode)
def execute(self):
    try:
        vars[self.children[0].tok].setValue(self.children[1].execute())
    except:
         print ("*** Error: variable %s assign before declaration!" % self.children[0].tok)

@addToClass(AST.DeclarationNode)
def execute(self):
    #create a new token with the language type translaein "real" type
    vars[self.children[0].tok] = myToken(typeEnum[self.children[1]])

@addToClass(AST.PrintNode)
def execute(self):
    print (self.children[0].execute())

@addToClass(AST.ConditionNode)
def execute(self):
    #evaluate every child and put result in list
    args = [c.execute() for c in self.children]
    #the type of the two values must be the same
    if checkType(args):
        return reduce(conditions[self.cOp], args)
    else:
        print ("*** Error: condition error type aren't the same")
        return False
        
@addToClass(AST.WhileNode)
def execute(self):
    while self.children[0].execute():
        self.children[1].execute()

@addToClass(AST.IfNode)
def execute(self):
    b = self.children[0].execute()
    if b:
        self.children[1].execute()

@addToClass(AST.IfElseNode)
def execute(self):
    #evaluate the condition 
    b = self.children[0].execute()
    if b:
        self.children[1].execute()
    else:
        self.children[2].execute()

@addToClass(AST.ForNode)
def execute(self):
    self.children[0].execute()
    while self.children[1].execute():
        self.children[2].execute()
        self.children[3].execute()

@addToClass(AST.IncrementNode)
def execute(self):
    try:
        #value must be set before incrementation
        if isSet(self.children[0].tok):
            if vars[self.children[0].tok].type == 'int':
                if self.op == "one_point":
                    vars[self.children[0].tok].value = vars[self.children[0].tok].value+1
                elif self.op == "pas_terrible":
                    vars[self.children[0].tok].value = vars[self.children[0].tok].value-1
            else:
                print("*** Error only integer(heberline) type can be incremented ")
    except:
        print("*** Error ", self.children[0].tok, " does not exist")

def isSet(token):
    ''' check if the value of the given token is set in vars dictionnary '''
    if vars[token].value == None:
        print("*** Error ", token, " must be set before used")
        return False
    else:
        return True

def checkType(args):    
    ''' check every type in args value and return true if they are all the same and false otherwise '''
    opType = None
    for i, tok in enumerate(args):        
        if type(tok) == myToken:     
            #if operation type is the same as the value type we check the nex one       
            if opType == type(tok.value):
                continue
            #if optype is None it take the token value type
            elif opType == None:
                opType = type(tok.value)   
            #if operatin type is set and not the same as token value type we can't aply operation           
            else :
                return False       
        #if the value is not a token we create a new myToken object with the token value and type          
        else:
            if type(tok) == int:
                args[i] = myToken('int', tok)
            if type(tok) == float:
                args[i] = myToken('float', tok)
            if type(tok) == bool:
                args[i] = myToken('bool', tok)
            if type(tok) == str:
                args[i] = myToken('str', tok)
            if opType == type(tok):
                continue
            elif opType == None:
                opType = type(tok)
            else :
                return False
    #if we reach here every token value are the same type
    return True
 

if __name__ == "__main__":
    from parser5 import parse
    import sys
    prog = open(sys.argv[1]).read()
    ast = parse(prog)
    
    ast.execute()