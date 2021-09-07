import sys
from antlr4 import *
from antlr4.tree.Trees import TerminalNode
from antlr4.error.Errors import *
from DecafLexer import DecafLexer
from DecafParser import DecafParser
from DecafListener import DecafListener
from table import *

errors=[]
#Posibles errores que pueden ocurrir
errorTable=[
    "Error de tipo incorrecto",
    "Fallo al llamar al metodo",
    "Indefinido",
    "Metodo inexistente",
    "Metodo no declarado",
    "Metodo no valido",
    "Metodo ya existente",
    "No hay valor de retorno",
    "Operado no aceptado",
    "Parametro ya existente",
    "Propiedad no pertenece a estruct",
    "Se declaro como array",
    "Variable no declarada",
    "Variable ya existente",
    "Variables con diferente tipo"
]

class DecafPrinter(DecafListener):
    def __init__(self) -> None:
        #contiene la info de los nodos
        self.nodes = {}
        #Ya encontro el main?
        self.main = False
        #Esctructura actual
        self.aStruct = None
        #lista de estructuras encontradas
        self.structs = []
        #nombre de metodo actual
        self.name = ""
        #en que ambito se ecuentra
        self.aName = "global"
        #nombre del nodo actual
        self.fNode = ""
        #Valor de funciones repetidas
        self.sName = 1
        #Lista de variables encontradas
        self.varsL = []
        #Lista de estructuras encontradas
        self.structsL = []
        self.n2Table(None)
        super().__init__()
    #Se encarga de verificar si las variables fueron declaradas
    def enterVarDeclaration(self, ctx: DecafParser.VarDeclarationContext):
        #Temp=agrega variable a estrucutra
        arr = False
        if ctx.NUM() != None:
            arr = True
        parentCtx = ctx.parentCtx
        child = parentCtx.getChild(0).getText()
        vType = ctx.getChild(0).getText()
        var = ctx.getChild(1).getText()
        #Si vienen de una estructura agrega la variable a la misma 
        if child == "struct":
            strc = parentCtx.getChild(1).getText()
            temp = self.v2Struct(strc, vType, var, 0, arr)
            if temp:
                self.nodes[ctx] = 'void'
            else:
                self.nodes[ctx] = 'error'
                print(ctx.start.line,errorTable[12])
                errors.append([ctx.start.line,errorTable[12]])
        #sino la agrega como variable normal
        else:
            temp = self.v2Table(vType, var,0,arr)
            if temp:
                self.nodes[ctx] = 'void'
            else:
                self.nodes[ctx] = 'error'
                print(ctx.start.line,errorTable[12])
                errors.append([ctx.start.line,errorTable[12]])
    #Verifica los bloques de codigo que contienen if...
    def enterBlock(self, ctx: DecafParser.BlockContext):
        #Temp=agrega variable a tabla 
        parentCtx = ctx.parentCtx
        child = parentCtx.getChild(0).getText()
        if child not in ['int', 'char', 'boolean', 'struct', 'void']:
            self.setName(self.name + str(self.sName + 1))
        #se agrega a la tabla
        temp = self.n2Table(self.fNode)
        if temp:
            self.nodes[ctx] = 'void'
    #al encontrar
    def enterLocation(self, ctx: DecafParser.LocationContext):
        if ctx.location():
            var = ctx.getChild(0).getText()
            if self.structs == []:
                #verifica si la variable esta en la tabla
                sType = self.sVarTable(var, self.aName)
                #verifica si es parte de una estructura
                aStruct = self.sStruct(sType.vType)
                #agrega a estructuras
                self.structs.append(aStruct)
            else:
                #agrega la variable a estructura
                sType = self.structs[-1].sBod[var]
                aStruct = self.sStruct(sType.vType)
                self.structs.append(aStruct)
    #se encarga de los parametros
    def enterParameter(self, ctx: DecafParser.ParameterContext):
        #Temp=agrega variable a variables
        arr = False
        #si tiene mas de dos valores es array
        if len(ctx.children) > 2: 
            arr=True
        #si el primer valor es void omite
        pType = ctx.getChild(0).getText()
        if pType != 'void':
            name = ctx.getChild(1).getText()
            temp = self.v2Table(pType, name,1, arr)
            #si llega es void
            if temp:
                self.nodes[ctx] = 'void'
            else:
                self.nodes[ctx] = 'error'
                print(ctx.start.line,errorTable[9])
                errors.append([ctx.start.line,errorTable[9]])
    #se crean los metodos
    def enterMethodDeclaration(self, ctx: DecafParser.MethodDeclarationContext):
        #Temp=agrega variable a tabla
        mType = ctx.getChild(0).getText()
        mName = ctx.getChild(1).getText()
        #Se guarda el nombre del metodo
        self.name = mName
        self.setName(mName)
        temp = self.n2Table(self.fNode, mType)
        if temp:
            self.nodes[ctx] = 'void'
        else:
            self.nodes[ctx] = 'error'
            print(ctx.start.line,errorTable[6])
            errors.append([ctx.start.line,errorTable[6]])
    #se crean las estructuras
    def enterStructDeclaration(self, ctx: DecafParser.StructDeclarationContext):
        strc = ctx.getChild(1).getText()
        self.s2Table(strc)
    #realiza verificaciones metodos
    def exitMethodCall(self, ctx: DecafParser.MethodCallContext):
        #sames= compara si los parametros son iguales
        # tTemp= lista con los tipos del metodo
        #Busca el metodo creado
        meth = self.findMeth(ctx.getChild(0).getText())
        if meth != None:
            tTemp = []
            #Obtiene los tipos que contiene el metodo
            for i in range(0, len(ctx.children)):
                if i > 1 and i < len(ctx.children)-1:
                    if ctx.getChild(i).getText() != ",":
                        tTemp.append(self.nodes[ctx.getChild(i)])
            #Compara si los metodos son iguales
            sames = self.comps(meth, tTemp)
            if sames:
                self.nodes[ctx] = meth.rType
            else:
                self.nodes[ctx] = 'error'
                print(ctx.start.line,errorTable[1])
                errors.append([ctx.start.line,errorTable[1]])
        else:
            self.nodes[ctx] = 'error'
            print(ctx.start.line,errorTable[3])
            errors.append([ctx.start.line,errorTable[3]])
    #Verifica si existe el metodo main
    def exitMethodDeclaration(self, ctx: DecafParser.MethodDeclarationContext):
        if ctx.getChild(1).getText() == 'main':
            self.main = True
        self.sName = 1
        self.name = "global"
        self.setName("global")
    #verifica que se tenga un return valido
    def exitStatement(self, ctx: DecafParser.StatementContext):
        #Si hay return continua
        if ctx.getChild(0).getText() == "return":
            #Verifica el tipo del metodo
            mType = self.rMethType(self.aName).rType
            exp = ctx.getChild(1)
            #si esta vacio lo guarda como void
            if ctx.getChild(1).getText() == "":
                if mType == 'void':
                    self.nodes[ctx] = 'void'
                #si esta vacio pero el siguiente tiene tipo es error
                elif mType in ['int', 'char', 'boolean', 'struct']:
                    self.nodes[ctx] = 'error'
                    print(ctx.start.line,errorTable[7])
                    errors.append([ctx.start.line,errorTable[7]])
                else:
                    self.nodes[ctx] = 'error'    
                    print(ctx.start.line,errorTable[5])
                    errors.append([ctx.start.line,errorTable[5]])
            else:
                #si tiene tipo verifica que exista para luego comparar tipos
                if mType in ['int', 'char', 'boolean', 'struct', 'void']:
                    exprType = self.nodes[exp.getChild(0)]
                    if exprType == mType:
                        self.nodes[ctx] = 'void'
                    else:
                        self.nodes[ctx] = 'error'
                        print(ctx.start.line,errorTable[0])
                        errors.append([ctx.start.line,errorTable[0]])
                else:
                    self.nodes[ctx] = 'error'  
                    print(ctx.start.line,errorTable[5])
                    errors.append([ctx.start.line,errorTable[5]])
    def exitBlock(self, ctx: DecafParser.BlockContext):
        currentBlockObj = self.findMeth(self.aName)
        self.setName(currentBlockObj.sup)
    def exitRegMethS(self, ctx: DecafParser.RegMethSContext):
        self.nodes[ctx] = self.nodes[ctx.methodCall()]
    def exitProgram(self, ctx: DecafParser.ProgramContext):
        if not self.main:
            self.nodes[ctx] = 'error'
            print(ctx.start.line,errorTable[4])
            errors.append([ctx.start.line,errorTable[4]])
    #verifica los tipos de operadores disponibles
    def exitRegOps(self, ctx: DecafParser.RegOpsContext):
        #Verifica los tipos y operandos
        op1 = ctx.getChild(0)
        op2 = ctx.getChild(2)
        op = ctx.getChild(1).getText()
        #Si alguno de estos debe de ser igual a int
        if op in ['*','/','%','+','-']:
            if self.nodes[op1] == 'int' and self.nodes[op2] == 'int':
                self.nodes[ctx] = 'int'
            else:
                self.nodes[ctx] = 'error'    
                print(ctx.start.line,errorTable[0])
                errors.append([ctx.start.line,errorTable[0]])
        #SI es alguno de estos debe de ser ent y retonoa bool
        elif op in ['<','>','<=','>=']:
            if self.nodes[op1] == 'int' and self.nodes[op2] == 'int':
                self.nodes[ctx] = 'boolean'
            else:
                self.nodes[ctx] = 'error'
                print(ctx.start.line,errorTable[0])
                errors.append([ctx.start.line,errorTable[0]])
        #Si es alguno de estos puede ser cualquier tipo pero iguales
        elif op in ['==','!='] :
            if self.nodes[op1]  in ['int', 'char', 'boolean'] and self.nodes[op2] in ['int', 'char', 'boolean']:
                if self.nodes[op1] == self.nodes[op2]:
                    self.nodes[ctx] = 'boolean'
                else:
                    self.nodes[ctx] = 'error'
                    print(ctx.start.line,errorTable[0])  
                    errors.append([ctx.start.line,errorTable[0]])
            else:
                self.nodes[ctx] = 'error'
                print(ctx.start.line,errorTable[0])
                errors.append([ctx.start.line,errorTable[0]])
        #Si es alguno de estos debe de ser bool
        elif op in ["&&","||"]:
            if self.nodes[op1] == 'boolean' and self.nodes[op2] == 'boolean':
                self.nodes[ctx] = 'boolean'
            else:
                self.nodes[ctx] = 'error'
                print(ctx.start.line,errorTable[0])
                errors.append([ctx.start.line,errorTable[0]])
    #para saber si es ditinto debe de ser bool
    def exitRegDistE(self, ctx: DecafParser.RegDistEContext):
        op1 = ctx.getChild(1)
        if self.nodes[op1] == 'boolean':
            self.nodes[ctx] = 'boolean'
        else:
            self.nodes[ctx] = 'error' 
            print(ctx.start.line,errorTable[0])
            errors.append([ctx.start.line,errorTable[0]])
    #para poder restar debe de ser int
    def exitReg_E(self, ctx: DecafParser.Reg_EContext):
        op1 = ctx.getChild(1)
        if self.nodes[op1] == 'int':
            self.nodes[ctx] = 'int'
        else:
            self.nodes[ctx] = 'error'
            print(ctx.start.line,errorTable[0])
            errors.append([ctx.start.line,errorTable[0]])
    def exitRegClosE(self, ctx: DecafParser.RegClosEContext):
        self.nodes[ctx] = self.nodes[ctx.expression()]    
    def exitInt_literal(self, ctx: DecafParser.Int_literalContext):
        self.nodes[ctx] = 'int'
    def exitChar_literal(self, ctx: DecafParser.Char_literalContext):
        self.nodes[ctx] = 'char'
    def exitBool_literal(self, ctx: DecafParser.Bool_literalContext):
        self.nodes[ctx] = 'boolean'
    def exitRegLocE(self, ctx: DecafParser.RegLocEContext):
        self.nodes[ctx] = self.nodes[ctx.getChild(0)]
    def exitVarDeclaration(self, ctx: DecafParser.VarDeclarationContext):
        vType = ctx.getChild(0).getText()
        self.nodes[ctx] = vType
    def exitLiteral(self, ctx: DecafParser.LiteralContext):
        self.nodes[ctx] = self.nodes[ctx.getChild(0)]
    def exitRegLitE(self, ctx: DecafParser.RegLitEContext):
        self.nodes[ctx] = self.nodes[ctx.getChild(0)]
    def exitRegMethE(self, ctx: DecafParser.RegMethEContext):
        self.nodes[ctx] = self.nodes[ctx.getChild(0)]
    #compara que la asignacion sea del mismo tipo
    def exitRegAssigS(self, ctx: DecafParser.RegAssigSContext):
        op1 = ctx.getChild(0)
        op2 = ctx.getChild(2)
        if self.nodes[op1] == self.nodes[op2] :
            self.nodes[ctx] = self.nodes[op1]
        else:
            self.nodes[ctx] = 'error'
            print(ctx.start.line,errorTable[0])
            errors.append([ctx.start.line,errorTable[0]])
    #verifica que sea bool
    def exitRegIfS(self, ctx: DecafParser.RegIfSContext):
        expression = ctx.getChild(2)
        if self.nodes[expression] == 'boolean':
            self.nodes[ctx] = 'boolean'
        else:
            self.nodes[ctx] = 'error'
            print(ctx.start.line,errorTable[0])   
            errors.append([ctx.start.line,errorTable[0]])
    #verifica que sea bool
    def exiRegElseS(self, ctx: DecafParser.RegElseSContext):
        expression = ctx.getChild(2)
        if self.nodes[expression] == 'boolean':
            self.nodes[ctx] = 'boolean'
        else:
            self.nodes[ctx] = 'error'  
            print(ctx.start.line,errorTable[0])
            errors.append([ctx.start.line,errorTable[0]])
    #asigna el nombre del nodo actiual
    def setName(self, amb):
        self.fNode = self.aName
        self.aName = amb
    #Agrega los nodos a la tabla
    def n2Table(self, fNode, mType=None):
        ok = False
        temp=[]
        for i in  self.varsL:
            temp.append(i[0])
        if self.aName not in temp:
            self.varsL.append([self.aName,Table(sup=fNode, rType=mType, tbl={})])
            ok = True
        else:
            ok = False
        return ok
    #Agrega la variable a la tabla
    def v2Table(self, vType, var, vPar, arr):
        ok = False
        for i in  self.varsL:
            if i[0]==self.aName:
                tempT=i[1]
        tempT2=tempT.tbl
        if var not in tempT2:
            tempT2[var] = VarInfo(var, vType, vPar,arr)
            ok = True
        else:
            ok = False
        for i in  self.varsL:
            if i[0]==self.aName:
                tempT.tbl=tempT2
                i[1]=tempT
        return ok
    #Busca que la variable este en la tabla
    def sVarTable(self, var, scopeName):
        for i in  self.varsL:
            if i[0]==scopeName:
                tempT=i[1]
        tempT2=tempT.tbl
        var2 = None
        if var in tempT2:
            var2 = tempT2[var]
        else:
            for i in  self.varsL:
                if i[0]==scopeName:
                    newScope=i[1]
            newScope=newScope.sup
            if newScope != None:
                var2 = self.sVarTable(var, newScope)
        return var2
    #busca el metodo dentro de la variable
    def findMeth(self, methodId):
        for i in  self.varsL:
            if i[0]==methodId:
                obj=i[1]
        return obj
    #Compara el tipo de los metodos
    def comps(self, meth, tTemp):
        tbl = meth.tbl
        tTemp2 = []
        for var, varItem in tbl.items():
            if varItem.vPar == 1:
                tTemp2.append(varItem.vType)
        if tTemp == tTemp2:
            return True 
        else:
            return False
    #Agrega la estructura a la tabla
    def s2Table(self, strc):
        strc = "struct"+strc
        temp=[]
        for i in  self.structsL:
            temp.append(i[0])
        if strc not in temp:
            self.structsL.append([strc,StructInfo(strc=strc, sBod={})])
    #Agrega las variables a las estructuras
    def v2Struct(self, strc, vType, var, vPar,arr):
        ok = False
        strc = "struct"+strc
        for i in  self.structsL:
            if i[0]==strc:
                tempS=i[1]
        tempS2=tempS.sBod
        if var not in tempS2:
            tempS2[var] = VarInfo(var, vType, vPar,arr)
            ok = True
        else:
            ok = False
        for i in  self.structsL:
            if i[0]==strc:
                tempS.sBod=tempS2
                i[1]=tempS
        return ok
    #Busca dentro de las estructuras
    def sStruct(self, strc):
        sVal = None
        for i in  self.structsL:
            if i[0]==strc:
                sVal=i[1]
        return sVal
    #Verifica las propiedades de las estructuras
    def exitLocation(self, ctx: DecafParser.LocationContext):
        var = None
        if ctx.location() != None:
            if self.structs != []:
                table = self.structs.pop()
                if table != None:
                    var = table.sBod[ctx.getChild(0).getText()]
                    if var != None:
                        self.nodes[ctx] = self.nodes[ctx.location()]
                    else:
                        self.nodes[ctx] = 'error'
                        print(ctx.start.line,errorTable[10])
                        errors.append([ctx.start.line,errorTable[10]])
                else:
                    self.nodes[ctx] = 'error'
                    print(ctx.start.line,errorTable[10])
                    errors.append([ctx.start.line,errorTable[10]])
            else:
                var = self.sVarTable(ctx.getChild(0).getText(), self.aName)
                if var != None:
                    self.nodes[ctx] = self.nodes[ctx.location()]
                else:
                    self.nodes[ctx] = 'error'
                    print(ctx.start.line,errorTable[2])
                    errors.append([ctx.start.line,errorTable[2]])
        elif type(ctx.parentCtx) == DecafParser.LocationContext and ctx.location() == None:
            if self.structs != []:
                table = self.structs.pop()
                if table != None:
                    var = table.sBod[ctx.getChild(0).getText()]
                    if var != None:                      
                        self.nodes[ctx] = var.vType        
                    else:
                        self.nodes[ctx] = 'error'   
                        print(ctx.start.line,errorTable[10])   
                        errors.append([ctx.start.line,errorTable[10]])                           
                else:
                    self.nodes[ctx] = 'error'
                    print(ctx.start.line,errorTable[10])
                    errors.append([ctx.start.line,errorTable[10]])
        else:
            var = self.sVarTable(ctx.getChild(0).getText(), self.aName)
            if var != None:
                self.nodes[ctx] = var.vType
            else:
                self.nodes[ctx] = 'error'  
                print(ctx.start.line,errorTable[12])
                errors.append([ctx.start.line,errorTable[12]])
        if ctx.expression():
            if self.nodes[ctx.expression()] != 'int':
                self.nodes[ctx] = 'error'
                print(ctx.start.line,errorTable[0])
                errors.append([ctx.start.line,errorTable[0]])
            if type(ctx.expression()) == DecafParser.Reg_EContext:
                self.nodes[ctx] = 'error'
                print(ctx.start.line,errorTable[0])
                errors.append([ctx.start.line,errorTable[0]])
            if var != None:
                if not var.arr:
                    self.nodes[ctx] = 'error'
                    print(ctx.start.line,errorTable[0])
                    errors.append([ctx.start.line,errorTable[0]])
        else:
            if var != None:
                if var.arr:
                    self.nodes[ctx] = 'error'
                    print(ctx.start.line,errorTable[11])
                    errors.append([ctx.start.line,errorTable[11]])
    #Busca el typo del metodo
    def rMethType(self, scope):
        for i in  self.varsL:
            if i[0]==scope:
                obj=i[1]
        if obj.sup != "global":
            obj = self.rMethType(obj.sup)
        return obj

def main(argv):
    input_stream = FileStream(argv)
    lexer = DecafLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = DecafParser(stream)
    tree = parser.program()  
    printer = DecafPrinter()
    walker = ParseTreeWalker()
    walker.walk(printer, tree)
    file = open("tabla.txt","w")
    for i in printer.varsL:
        vars=[]
        for key in i[1].tbl:
            vars.append([i[1].tbl[key].var,i[1].tbl[key].vType,i[1].tbl[key].vPar,i[1].tbl[key].arr])
        file.write(str([i[0],i[1].rType,vars])+'\n')
    for i in printer.structsL:
        vars=[]
        for key in i[1].sBod:
            vars.append([i[1].sBod[key].var,i[1].sBod[key].vType,i[1].sBod[key].vPar,i[1].sBod[key].arr])
        file.write(str([i[0],vars])+'\n')
    file.close()
    file = open("error.txt","w")
    for i in errors:
        file.write(str(i)+'\n')
    file.close()
    return []