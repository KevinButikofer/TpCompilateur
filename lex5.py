import ply.lex as lex

reserved_words = (
	'on_se_le_refait_une_petite_fois',
	'pas_mal',
	'true',
	'false',	
	'serieux',
	'scuse',
	'c_est_en_forgeant_qu_on_devient_forgeron'
)

tokens = (	
	'INT',
	'NUMBER',
	'STRING',
	'ADD_OP',
	'MUL_OP',
	'INCREMENT_OP',
	'IDENTIFIER',
	'TYPE',
	'COMPARISONOP',
) + tuple(map(lambda s:s.upper(),reserved_words))

literals = '();={}'

def t_COMMENT(t):
	r'//.*'
	t.lexer.lineno += len(t.value)

def t_INCREMENT_OP(t):
	r'(one_point|pas_terrible)'
	return t

def t_TYPE(t):
	r'(heberline|jav|float|string)'
	return t

def t_TRUE(t):
    r'(troeuw)'
    t.value = True
    return t

def t_FALSE(t):
    r'(je_vais_bosser_cette_semaine)'
    t.value = False
    return t

def t_COMPARISONOP(t):
	r'(<=|>=|>|<|cochon_egal_porc|je_passe_mon_annee)'
	return t

def t_STRING(t):
	r'["]([^\n\\]|\\(.|\n))*["]'
	try:
		t.value = str(t.value)    #delete first and last charactère (quote)
	except ValueError:
		print ("Line %d: Problem while parsing %s!" % (t.lineno,t.value))
		t.value = ""	
	return t

def t_NUMBER(t):
	r'\d+(\.\d+)'
	try:
		t.value = float(t.value)    
	except ValueError:
		print ("Line %d: Problem while parsing %s!" % (t.lineno,t.value))
		t.value = 0
	return t

def t_INT(t):
	r'\d+'
	try:
		t.value = int(t.value)
	except ValueError:
		print ("error for integer", t.value)
		t.value = 0		
	return t
		
def t_ADD_OP(t):
	r'[+-]'
	return t
	
def t_MUL_OP(t):
	r'[*/]'
	return t

def t_IDENTIFIER(t):
	r'[A-Za-z_]\w*'
	if t.value in reserved_words:
		t.type = t.value.upper()
	return t

def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

t_ignore  = ' \t'

def t_error(t):
	print ("Illegal character '%s'" % repr(t.value[0]))
	t.lexer.skip(1)

lex.lex()

if __name__ == "__main__":
	import sys
	prog = open(sys.argv[1]).read()

	lex.input(prog)

	while 1:
		tok = lex.token()
		if not tok: break
		print ("line %d: %s(%s)" % (tok.lineno, tok.type, tok.value))
