import ply.yacc as yacc

from lex5 import tokens
import AST

vars = {}

def p_programme_statement(p):
    ''' programme : statement '''
    p[0] = AST.ProgramNode(p[1])

def p_programme_recursive(p):
    ''' programme : statement ';' programme '''
    p[0] = AST.ProgramNode([p[1]]+p[3].children)

def p_statement(p):
    ''' statement : assignation
        | declaration
        | structure '''
    p[0] = p[1]
    	
def p_statement_print(p):
    ''' statement : PAS_MAL expression '''
    p[0] = AST.PrintNode(p[2])

def p_structure(p):
    ''' structure : ON_SE_LE_REFAIT_UNE_PETITE_FOIS condition '{' programme '}' '''
    p[0] = AST.WhileNode([p[2],p[4]])

def p_expression_op(p):
    '''expression : expression ADD_OP expression
            | expression MUL_OP expression'''
    p[0] = AST.OpNode(p[2], [p[1], p[3]])
    	
def p_expression_num_or_var(p):
    '''expression : NUMBER
        | INT
        | boolean
        | STRING
        | IDENTIFIER '''
    p[0] = AST.TokenNode(p[1])

def p_expression_paren(p):
    ''' expression : '(' expression ')' '''
    p[0] = p[2]
    	
def p_minus(p):
    ''' expression : ADD_OP expression %prec UMINUS'''
    p[0] = AST.OpNode(p[1], [p[2]])

def p_increment(p):
    ''' assignation : IDENTIFIER INCREMENT_OP '''
    p[0] = AST.IncrementNode(p[2], AST.TokenNode(p[1]))

def p_declaration(p):
    ''' declaration : TYPE IDENTIFIER '''
    p[0] = AST.DeclarationNode([AST.TokenNode(p[2]), p[1]])

def p_assign(p):
    ''' assignation : IDENTIFIER '=' expression '''
    p[0] = AST.AssignNode([AST.TokenNode(p[1]),p[3]])

def p_condition_paren(p):
    ''' condition : '(' expression COMPARISONOP expression ')' '''
    p[0] = AST.ConditionNode(p[3], [p[2], p[4]])    

def p_condition(p):
    ''' condition : expression COMPARISONOP expression '''
    p[0] = AST.ConditionNode(p[2], [p[1], p[3]])    

def p_if_statement(p):
    ''' structure : SERIEUX condition '{' programme '}' '''
    p[0] = AST.IfNode([p[2], p[4]])

def p_if_else_statement(p):
    ''' structure : SERIEUX condition '{' programme '}' SCUSE '{' programme '}' '''
    p[0] = AST.IfElseNode([p[2], p[4], p[8]])

def p_for_statement(p):
    ''' structure : C_EST_EN_FORGEANT_QU_ON_DEVIENT_FORGERON '(' assignation ';' condition ';' assignation ')' '{' programme '}' '''
    p[0] = AST.ForNode([p[3], p[5], p[7], p[10]])

def p_error(p):
    if p:
        print ("Syntax error in line %d" % p.lineno)
        yacc.yacc().errok()
    else:
        print ("Sytax error: unexpected end of file!")


precedence = (
    ('left', 'ADD_OP'),
    ('left', 'MUL_OP'),
    ('right', 'UMINUS'),  
)

def parse(program):
    return yacc.parse(program)

yacc.yacc(outputdir='generated')

if __name__ == "__main__":
    import sys     	
    prog = open(sys.argv[1]).read()
    result = yacc.parse(prog)
    if result:
        print (result)
            
        import os
        graph = result.makegraphicaltree()
        name = os.path.splitext(sys.argv[1])[0]+'-ast.pdf'
        graph.write_pdf(name) 
        print ("wrote ast to", name)
    else:
        print ("Parsing returned no result!")