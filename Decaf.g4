grammar Decaf;

fragment DIGIT: '0'..'9'	;
fragment LETTER
	: ('a'..'z'|'A'..'Z'|'_') ;
ID
	:LETTER (LETTER|DIGIT)*	;
NUM:DIGIT(DIGIT)*;
CHAR: '\'' ( ~['\r\n\\] | '\\' ['\\] ) '\'';
SPACE
    :	[ \t\r\n\u000C]+ -> skip	;

program 
	:	'class' ID '{' (declaration)* '}'	;
declaration 
	:   structDeclaration
	|   varDeclaration
	|   methodDeclaration	; 
varDeclaration 
	:	varType ID ';'	|	varType  ID '[' NUM ']' ';'	;
structDeclaration
	:   'struct' ID '{' (varDeclaration)* '}' (';')?	;
varType
	:   'int'														
	|   'char'														
	|   'boolean'													
	|   'struct' ID												
	|   structDeclaration;
methodDeclaration
	:	methodType ID '(' (parameter(','parameter)*)* ')' block	;
methodType
	:   'int'														
	|   'char'														
	|   'boolean'																																	
    |   'void'	;
parameter
	:	parameterType ID   |    parameterType ID '[' ']'	|	'void'	;
parameterType
	:   'int'
	|   'char'
	|   'boolean'	;
block
	:   '{'(varDeclaration)* (statement)* '}'	;
statement
   	:   'if' '(' expression ')' block ('else' block)? #regIfS
	|   'while' '(' expression ')' block #regElseS
	|   'return' expression';' #temp1
	|   methodCall 	';' #regMethS							
	|   block #temp2							
	|   location '=' expression';' #regAssigS										
	|   (expression)? ';' #temp3	; 
location  
	:	(ID|ID '[' expression ']') ('.' location)?    ;
expression
	:   location #regLocE				
	|   methodCall #regMethE								
	|   literal	#regLitE						
	|   '-' expression #reg_E
	|   '!' expression #regDistE
	|   '(' expression ')' #regClosE
	|	expression op expression #regOps ;
methodCall
	:	ID '(' (expression(','expression )*)? ')'	;

op
	:	arith_op   |	rel_op	|	eq_op	|	cond_op	;
arith_op
    :	'*'		|	 '/'	|	'%' |	'+'		|	'-'		;
rel_op
	:	'<'		|	 '>' 	| 	'<=' 	|	 '>=' 	;
eq_op
	: 	'=='	 |	 '!='	 ;
cond_op
	:	'&&'	|	'||'	;
literal
	:	int_literal    |    char_literal	|	bool_literal	;
int_literal
	:	NUM		;
char_literal 
    :   '\'' CHAR '\''      ;
bool_literal 
	:	'true'	|	'false'		; 