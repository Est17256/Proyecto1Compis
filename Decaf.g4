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
	|   'return' expressionOR';' #regRet
	|   methodCall 	';' #regMethS							
	|   block #regBloc							
	|   location '=' expression';' #regAssigS										
	|   (expression)? ';' #RegExp	; 
location  
	:	(ID|ID '[' expression ']') ('.' location)?    ;
expressionOR
	:	expression 
	|;
expression
	:   location #regLocE				
	|   methodCall #regMethE								
	|   literal	#regLitE						
	|   '-' expression #reg_E
	|   '!' expression #regDistE
	|   '(' expression ')' #regClosE
	| 	expression arith_op_5 expression #regAr5
    | 	expression arith_op_4 expression #regAr4
    | 	expression arith_op_3 expression #regAr3
    | 	expression arith_op_2 expression #regAr2
    | 	expression arith_op_1 expression #regAr1;
methodCall
	:	ID '(' (expression(','expression )*)? ')'	;
rel_op
	:	'<'		|	 '>' 	| 	'<=' 	|	 '>=' 	;
eq_op
	: 	'=='	|	 '!='	;
arith_op_5
	:	'*'		|	 '/' 	| 	'%'		;
arith_op_4
	: 	'+' 	| 	 '-'	;
arith_op_3
	: 	rel_op  | 	eq_op	;	
arith_op_2
	: 	'&&'	;
arith_op_1
	: 	'||'	;
literal
	:	int_literal    |    char_literal	|	bool_literal	;
int_literal
	:	NUM		;
char_literal 
    :   '\'' CHAR '\''      ;
bool_literal 
	:	'true'	|	'false'		; 