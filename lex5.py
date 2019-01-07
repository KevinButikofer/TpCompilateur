import ply.lex as lex

reserved_words = (
	'on_se_le_refait_une_petite_fois',
	'pas_mal',		
	'troeuw',
	'je_vais_bosser_cette_semaine',
	'Serieux',
	'je_passe_mon_annee',
	'cochon_egal_porc',
	'fermez_vos_ordinateur',
	'one_point',
	'pas_terrible',
	'true',
	'false',
)

tokens = (	
	'BOOL',
	'INT',
	'NUMBER',
	'ADD_OP',
	'MUL_OP',
	'IDENTIFIER',
	'TYPE'
) + tuple(map(lambda s:s.upper(),reserved_words))

literals = '();={}'

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

def t_NUMBER(t):
	#r'\d+(\.\d+)?'
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
