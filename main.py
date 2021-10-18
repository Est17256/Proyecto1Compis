import sys
from antlr4 import *
from antlr4.tree.Trees import TerminalNode
from antlr4.error.Errors import *
from DecafLexer import DecafLexer
from DecafParser import DecafParser
from DecafListener import DecafListener
from table import *
#Posibles errores que pueden ocurrir
# errorTable=[
#     "Error de tipo incorrecto",
#     "Fallo al llamar al metodo",
#     "Indefinido",
#     "Metodo inexistente",
#     "Metodo no declarado",
#     "Metodo no valido",
#     "Metodo ya existente",
#     "No hay valor de retorno",
#     "Operado no aceptado",
#     "Parametro ya existente",
#     "Propiedad no pertenece a estruct",
#     "Se declaro como array",
#     "Variable no declarada",
#     "Variable ya existente",
#     "Variables con diferente tipo"
# ]
class DecafPrinter(DecafListener):
    def __init__(self) -> None:
        #Contiene los pesos de las variables
        self.typeSizes = {'int':4, 'char':1, 'boolean':1}
        #contiene la info de los nodos
        self.nodes = {}
        #Ya encontro el main?
        self.main = False
        #Esctructura actual
        self.aStruct = None
        #lista de estructuras encontradas
        self.structs = []
        self.localOffset = 0
        self.globalOffset = 0
        self.structOffset = 0
        #nombre de metodo actual
        self.name = ""
        #en que ambito se ecuentra
        self.aName = "global"
        #nombre del nodo actual
        self.fNode = "None"
        #Valor de funciones repetidas
        self.cName = 1
        #Diccionario que contiene los ambitos
        self.ambDict = {}
        #Diccionario que contiene las estrucutras
        self.strDic = {}
        #Cuadruplas generadas
        self.lcuads = []
        #Contiene los argumentros de los nodos
        self.nodeArg = {}
        #Contiene el numero de variable por la que vamos
        self.cVar = 1
        #Contiene el numero de bloque por el que vamos
        self.cBloc = 1
        #Contiene el numero de condicion  por la que vamos
        self.loops = 1
        #Contiene el numero de vento por el vamos
        self.relCounter = 1
        #Verifica si ya pasamos por el bloque
        self.visit = False
        # Contiene posicion de estructura
        self.currentStructMovement = 0
        #COntiene informacion del array
        self.arrayInfo = []
        self.n2Table(None)
        super().__init__()
    # Imprime las cuadruplas anteriormente realizadas
    def PrintCuad(self, cuad):
        cuads = ""
        if cuad.op == '<' :
            cuads = '  if ' + cuad.arg1.Name + cuad.op + cuad.arg2.Name + ' GOTO ' + cuad.res.first
        elif cuad.op== '<=':
            cuads = '  if ' + cuad.arg1.Name + cuad.op + cuad.arg2.Name + ' GOTO ' + cuad.res.first
        elif cuad.op == '>':
            cuads = '  if ' + cuad.arg1.Name + cuad.op + cuad.arg2.Name + ' GOTO ' + cuad.res.first
        elif cuad.op == '>=':
            cuads = '  if ' + cuad.arg1.Name + cuad.op + cuad.arg2.Name + ' GOTO ' + cuad.res.first
        elif cuad.op == '==':
            cuads = '  if ' + cuad.arg1.Name + cuad.op + cuad.arg2.Name + ' GOTO ' + cuad.res.first
        elif cuad.op == '!=':
            cuads = '  if ' + cuad.arg1.Name + cuad.op + cuad.arg2.Name + ' GOTO ' + cuad.res.first
        elif cuad.op == "LABEL":
            if cuad.arg1 != None:
                cuads = cuad.arg1.Name + ":"
        elif cuad.op == "lTrue":
            cuads = cuad.arg1.first + ":"
        elif cuad.op == "lFalse":
            cuads = cuad.arg1.els + ":"
        elif cuad.op == "labeln":
            cuads = cuad.arg1.go + ":"
        elif cuad.op == "GOTON":
            cuads = "  GOTO " + cuad.arg1.go
        elif cuad.op == "GOTOF":
            cuads = "  GOTO " + cuad.arg1.els
        elif cuad.res == None:
            cuads = "  " + cuad.op + " " + cuad.arg1.Name
        elif cuad.arg2 != None:
            cuads = "  " + cuad.res.Name + "=" + cuad.arg1.Name  + cuad.op + cuad.arg2.Name 
        elif cuad.arg2 == None:
            cuads = "  " + cuad.res.Name + "=" + cuad.op + cuad.arg1.Name 
        return cuads 
    #Se encarga de verificar si las variables fueron declaradas
    def enterVarDeclaration(self, ctx: DecafParser.VarDeclarationContext):
        #Temp=agrega variable a estrucutra
        value = None
        arr = False
        if ctx.NUM() != None:
            value = ctx.getChild(3).getText()
            arr = True
        parentCtx = ctx.parentCtx
        child = parentCtx.getChild(0).getText()
        vType = ctx.getChild(0).getText()
        var = ctx.getChild(1).getText()
        #Si vienen de una estructura agrega la variable a la misma 
        if child == "struct":
            strc = parentCtx.getChild(1).getText()
            temp = self.v2Struct(strc, vType, var, "blockVar", value, arr, self.aName)
            if temp:
                self.nodes[ctx] = 'void'
        #sino la agrega como variable normal
        else:
            temp = self.v2Table(vType, var, "blockVar", value, arr, self.aName)
            if temp:
                self.nodes[ctx] = 'void'
    #Verifica los bloques de codigo que contienen if...
    #Se encarga de dirijir a las los bloques dependiendo si las condiciones se cumplen o no 
    def enterBlock(self, ctx: DecafParser.BlockContext):
        #Temp=agrega variable a tabla 
        parentCtx = ctx.parentCtx
        child = parentCtx.getChild(0).getText()
        if child not in ['int', 'char', 'boolean', 'struct', 'void']:
            self.cName += 1
            self.setName(self.name + str(self.cName))
        temp = self.n2Table(self.fNode)
        if temp:
            self.nodes[ctx] = 'void'
        #Si el tipo del padre es un if
        if type(parentCtx) == DecafParser.RegIfSContext:
            tempArg = self.nodeArg[parentCtx.getChild(2)]
            if self.visit == False:
                self.lcuads.append(Cuadruples("lTrue", tempArg, None, None))
                self.visit = True 
            else:
                tempArg2 = self.nodeArg[parentCtx.getChild(4)]
                self.lcuads.append(Cuadruples('GOTON', tempArg2, None, None))
                self.lcuads.append(Cuadruples("lFalse", tempArg, None, None))
        if type(parentCtx) == DecafParser.RegElseSContext:
            tempArg = self.nodeArg[parentCtx.getChild(2)]
            self.lcuads.append(Cuadruples('lTrue', tempArg, None, None))
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
            temp = self.v2Table(pType, name, "PARAM", None, arr, self.aName)
            #si llega es void
            if temp:
                self.nodes[ctx] = 'void'
    #se crean los metodos
    #Se encarga de poder crear el metodo en codigo intermedio
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
            newLabel = "LABEL_"+mName
            newAddr = Lprops(newLabel, None, None, None)
            self.lcuads.append(Cuadruples("LABEL", newAddr, None, None))
    #se crean las estructuras
    def enterStructDeclaration(self, ctx: DecafParser.StructDeclarationContext):
        strc = ctx.getChild(1).getText()
        self.s2Table(strc)
    #realiza verificaciones metodos
    #aqui llamo a todos los metodos y los hijos y busco las direcciones y despues ya guardo lo que tengo dentro de los hijos
    def exitMethodCall(self, ctx: DecafParser.MethodCallContext):
        #sames= compara si los parametros son iguales
        # tTemp= lista con los tipos del metodo
        args = ctx.getChild(2).getText()
        meth = self.findMeth(ctx.getChild(0).getText())
        if meth != None:
            tTemp = []
            for i in range(0, len(ctx.children)):
                if i > 1 and i < len(ctx.children)-1:
                    if (ctx.getChild(i).getText() != ","):
                        tTemp.append(self.nodes[ctx.getChild(i)])
            #Compara si los metodos son iguales
            sames = self.comps(meth, args, tTemp)
            if sames:
                self.nodes[ctx] = meth.rType
                for i in range(0, len(ctx.children)):
                    if i > 1 and i < len(ctx.children)-1:
                        if (ctx.getChild(i).getText() != ","):
                            try:
                                self.lcuads.append(Cuadruples('PARAM', self.nodeArg[ctx.getChild(i)], None, None))
                            except:
                                pass
                methodAddr = Lprops("LABEL_"+ctx.getChild(0).getText()+","+str(len(tTemp)), None, None, None)
                self.lcuads.append(Cuadruples('CALL', methodAddr, None, None))
    #Verifica si existe el metodo main
    def exitMethodDeclaration(self, ctx: DecafParser.MethodDeclarationContext):
        if ctx.getChild(1).getText() == 'main':
            self.main = True
        self.cName = 1
        self.cVar = 1
        self.localOffset = 0
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
                if (mType == 'void'):
                    self.nodes[ctx] = 'void'
            else:
                #si tiene tipo verifica que exista para luego comparar tipos
                if mType in ['int', 'char', 'boolean', 'struct']:
                    exprType = self.nodes[exp.getChild(0)]
                    if (exprType == mType):
                        self.nodes[ctx] = 'void'
    def exitBlock(self, ctx: DecafParser.BlockContext):
        currentBlockObj = self.findMeth(self.aName)
        self.setName(currentBlockObj.sup)
    def exitRegMethS(self, ctx: DecafParser.RegMethSContext):
        try:
            self.nodes[ctx] = self.nodes[ctx.methodCall()]
        except:
            pass
    def exitProgram(self, ctx: DecafParser.ProgramContext):
        if (not self.main):
            self.nodes[ctx] = 'error'
    def exitStructDeclaration(self, ctx: DecafParser.StructDeclarationContext):
        self.structOffset = 0
    def calculateSize(self, vType, num):
        num = int(num)
        if vType in self.typeSizes:
            return self.typeSizes[vType]*num
        elif (vType in self.strDic):
            return self.strDic[vType].size*num
    #verifica si  hay un ||
    def enterRegAr1(self, ctx: DecafParser.RegAr1Context):
        op1 = ctx.getChild(0)
        op2 = ctx.getChild(2)
        op1False = "LABEL_"+"rel"+str(self.relCounter)+"_FALSE"
        self.nodeArg[op1] = Lprops(None, self.nodeArg[ctx].first, op1False, None)
        self.nodeArg[op2] = self.nodeArg[ctx]
    #verifica si  hay un &&    
    def enterRegAr2(self, ctx: DecafParser.RegAr2Context):
        op1 = ctx.getChild(0)
        op2 = ctx.getChild(2)
        op1True = "LABEL_"+"rel"+str(self.relCounter)+"_:TRUE"
        self.nodeArg[op1] = Lprops(None, op1True, self.nodeArg[ctx].els, None)
        self.nodeArg[op2] = self.nodeArg[ctx]
    #para saber si es ditinto debe de ser bool
    def enterRegDistE(self, ctx: DecafParser.RegDistEContext):
        op = ctx.getChild(1)
        self.nodeArg[op] = self.nodeArg[ctx]
    #Se encarga de las operaciones y agregar sus valores a las variables
    def exitRegAr5(self, ctx: DecafParser.RegAr5Context):
        op1 = ctx.getChild(0)
        op2 = ctx.getChild(2)
        operator = ctx.getChild(1).getText()
        if(self.nodes[op1] == 'int' and self.nodes[op2] == 'int'):
            self.nodes[ctx] = 'int'
            nVar ="T" + str(self.cVar)
            self.cVar += 1
            self.nodeArg[ctx] = Lprops(nVar, None, None, None)
            self.lcuads.append(Cuadruples(operator, self.nodeArg[op1], self.nodeArg[op2], self.nodeArg[ctx]))
    def exitRegAr4(self, ctx: DecafParser.RegAr4Context):
        op1 = ctx.getChild(0)
        op2 = ctx.getChild(2)
        operator = ctx.getChild(1).getText()
        if(self.nodes[op1] == 'int' and self.nodes[op2] == 'int'):
            self.nodes[ctx] = 'int'
            nVar ="T" + str(self.cVar)
            self.cVar += 1
            self.nodeArg[ctx] = Lprops(nVar, None, None, None)
            self.lcuads.append(Cuadruples(operator, self.nodeArg[op1], self.nodeArg[op2], self.nodeArg[ctx]))
    def exitRegAr3(self, ctx: DecafParser.RegAr3Context):
        op1 = ctx.getChild(0)
        op2 = ctx.getChild(2)
        symbol = ctx.getChild(1).getText()
        if (symbol == '<' or symbol == '<=' or symbol == '>' or symbol == '>='):
            if(self.nodes[op1] == 'int' and self.nodes[op2] == 'int'):
                self.nodes[ctx] = 'boolean'
                self.lcuads.append(Cuadruples(symbol, self.nodeArg[op1], self.nodeArg[op2], self.nodeArg[ctx]))
                self.lcuads.append(Cuadruples('GOTOF', self.nodeArg[ctx], None, None))
                self.relCounter += 1
        elif (symbol == "==" or symbol == "!="):
            allowed = ('int', 'char', 'boolean')
            type1 = self.nodes[op1] 
            type2 = self.nodes[op2]
            if (type1 in allowed and type2 in allowed):
                if(self.nodes[op1] == self.nodes[op2]):
                    self.nodes[ctx] = 'boolean'
                    self.lcuads.append(Cuadruples(symbol, self.nodeArg[op1], self.nodeArg[op2], self.nodeArg[ctx]))
                    self.lcuads.append(Cuadruples('GOTOF', self.nodeArg[ctx], None, None))
                    self.relCounter += 1
    def exitRegAr2(self, ctx: DecafParser.RegAr2Context):
        op1 = ctx.getChild(0)
        op2 = ctx.getChild(2)
        if(self.nodes[op1] == 'boolean' and self.nodes[op2] == 'boolean'):
            self.nodes[ctx] = 'boolean'
    def exitRegAr1(self, ctx: DecafParser.RegAr1Context):
        op1 = ctx.getChild(0)
        op2 = ctx.getChild(2)
        if(self.nodes[op1] == 'boolean' and self.nodes[op2] == 'boolean'):
            self.nodes[ctx] = 'boolean'
    def exitRegDistE(self, ctx: DecafParser.RegDistEContext):
        op1 = ctx.getChild(1)
        if(self.nodes[op1] == 'boolean'):
            self.nodes[ctx] = 'boolean'
    #para poder restar debe de ser int
    def exitReg_E(self, ctx: DecafParser.Reg_EContext):
        op1 = ctx.getChild(1)
        if(self.nodes[op1] == 'int'):
            self.nodes[ctx] = 'int'
            nVar ="T" + str(self.cVar)
            self.cVar += 1
            self.nodeArg[ctx] = Lprops(nVar, None, None, None)
            self.lcuads.append(Cuadruples('minus', self.nodeArg[op1], None, self.nodeArg(ctx)))
    def exitRegClosE(self, ctx: DecafParser.RegClosEContext):
        self.nodes[ctx] = self.nodes[ctx.expression()]
        self.nodeArg[ctx] = self.nodeArg[ctx.expression()]
    def exitInt_literal(self, ctx: DecafParser.Int_literalContext):
        self.nodes[ctx] = 'int'
        self.nodeArg[ctx] = Lprops(ctx.getText(), None, None, None)
    def exitChar_literal(self, ctx: DecafParser.Char_literalContext):
        self.nodes[ctx] = 'char'
        self.nodeArg[ctx] = Lprops(ctx.getText(), None, None, None)
    def exitBool_literal(self, ctx: DecafParser.Bool_literalContext):
        self.nodes[ctx] = 'boolean'
        self.nodeArg[ctx] = Lprops(ctx.getText(), None, None, None)
    def exitRegLocE(self, ctx: DecafParser.RegLocEContext):
        self.nodes[ctx] = self.nodes[ctx.getChild(0)]
        self.nodeArg[ctx] = self.nodeArg[ctx.getChild(0)]
    def exitVarDeclaration(self, ctx: DecafParser.VarDeclarationContext):
        vType = ctx.getChild(0).getText()
        self.nodes[ctx] = vType   
    def exitLiteral(self, ctx: DecafParser.LiteralContext):
        self.nodes[ctx] = self.nodes[ctx.getChild(0)]
        self.nodeArg[ctx] = self.nodeArg[ctx.getChild(0)]    
    def exitRegLitE(self, ctx: DecafParser.RegLitEContext):
        self.nodes[ctx] = self.nodes[ctx.getChild(0)]
        self.nodeArg[ctx] = self.nodeArg[ctx.getChild(0)]  
    def exitRegMethE(self, ctx: DecafParser.RegMethEContext):
        try:
            self.nodes[ctx] = self.nodes[ctx.getChild(0)]  
        except:
            pass 
    # Crea las cuadruplas y sus valores para el if
    def enterRegIfS(self, ctx: DecafParser.RegIfSContext):
        trues = "LABEL_"+"BLOCK"+str(self.cBloc)+"_TRUE"
        conds = "LABEL_"+"LOOPEND"+str(self.cBloc)+"_NEXT"
        tempArg2 = Lprops(None, None, None, conds)
        if (len(ctx.children) > 5):
            falses = "LABEL_"+"BLOCK"+str(self.cBloc)+"_FALSE"
            tempArg = Lprops(None, trues, falses, None)
        else:
            falses = conds
            tempArg = Lprops(None, trues, falses, None)
        self.nodeArg[ctx.getChild(2)] = tempArg
        self.nodeArg[ctx.getChild(4)] = tempArg2
    # Crea las cuadruplas y sus valores para el if
    def enterRegElseS(self, ctx: DecafParser.RegElseSContext):
        Sconds = "LABEL_"+"LOOP"+str(self.loops)+"_START"
        trues = "LABEL_"+"BLOCK"+str(self.cBloc)+"_TRUE"
        falses = "LABEL_"+"LOOPEND"+str(self.cBloc)+"_NEXT"
        self.nodeArg[ctx.getChild(2)] = Lprops(None, trues, falses, None)
        self.nodeArg[ctx.getChild(4)] = Lprops(None, None, None, Sconds)
        self.lcuads.append(Cuadruples('labeln', self.nodeArg[ctx.getChild(4)], None, None))
    #compara que la asignacion sea del mismo tipo    
    def exitRegAssigS(self, ctx: DecafParser.RegAssigSContext):
        op1 = ctx.getChild(0)
        op2 = ctx.getChild(2)
        try:
            if self.nodes[op1] == self.nodes[op2]:
                self.nodes[ctx] = self.nodes[op1]
                self.lcuads.append(Cuadruples('', self.nodeArg[op2], None, self.nodeArg[op1]))      
        except:
            pass
    def exitRegIfS(self, ctx: DecafParser.RegIfSContext):
        expression = ctx.getChild(2)
        statement = ctx.getChild(4)
        if(self.nodes[expression] == 'boolean'):
            self.nodes[ctx] = 'boolean'
            tempArg2 = self.nodeArg[statement] 
            self.lcuads.append(Cuadruples("labeln", tempArg2, None, None))
            self.cBloc += 1
            self.visit = False 
    def exitRegElseS(self, ctx: DecafParser.RegElseSContext):
        expression = ctx.getChild(2)
        if(self.nodes[expression] == 'boolean'):
            self.nodes[ctx] = 'boolean'
            self.lcuads.append(Cuadruples("GOTON", self.nodeArg[ctx.getChild(4)], None, None))
            self.lcuads.append(Cuadruples("lFalse", self.nodeArg[expression], None, None))
            self.cBloc += 1
    #asigna el nombre del nodo actiual
    def setName(self, amb):
        self.fNode = self.aName
        self.aName = amb
    #Agrega los nodos a la tabla
    def n2Table(self, fNode, mType=None):
        ok = False
        if self.aName not in self.ambDict:
            self.ambDict[self.aName] = SymbolTableItem(sup=fNode, rType=mType, tbl={})
            ok = True
        else:
            ok = False
        return ok
    #Agrega la variable a la tabla
    def v2Table(self, vType, var, vPar, num, arr, amb):
        if num == None: 
            num = 1
        ok = False
        currentVarSize = self.calculateSize(vType, num)
        currentOffset = 0
        if (self.aName == 'global'):
            currentOffset = self.globalOffset
        else:
            currentOffset = self.localOffset
        tempT2 = self.ambDict.get(self.aName).tbl
        if var not in tempT2:
            tempT2[var] = VarInfo(var, vType, vPar, num, currentVarSize, arr, currentOffset, amb)
            if self.aName == 'global':
                self.globalOffset += currentVarSize
            else:
                self.localOffset += currentVarSize
            ok = True
        else:
            ok = False
        self.ambDict.get(self.aName).tbl = tempT2
        return ok
    #Busca que la variable este en la tabla
    def sVarTable(self, var, scopeName):
        tempT2 = self.ambDict.get(scopeName).tbl
        var2 = None
        if var in tempT2:
            var2 = tempT2[var]
        else:
            newScope = self.ambDict.get(scopeName).sup
            if newScope != None:
                var2 = self.sVarTable(var, newScope)
        return var2
    #busca el metodo dentro de la variable
    def findMeth(self, methodId):
        obj = self.ambDict.get(methodId)
        return obj
    #Compara el tipo de los metodos
    def comps(self, meth, args, tTemp):
        tbl = meth.tbl
        tTemp2 = []
        for var, varItem in tbl.items():
            if varItem.vPar == "PARAM":
                tTemp2.append(varItem.vType)
        if (tTemp == tTemp2):
            return True 
        else:
            return False
    #Agrega la estructura a la tabla
    def s2Table(self, strc):
        strc = "struct"+strc
        if strc not in self.strDic:
            self.strDic[strc] = StructInfo(strc=strc, sBod={})
    #Agrega las variables a las estructuras
    def v2Struct(self, strc, vType, var, vPar, num, arr, amb):
        if (num == None): num = 1
        ok = False
        currentVarSize = self.calculateSize(vType, num)
        currentOffset = self.structOffset
        strc = "struct"+strc
        tempS2 = self.strDic.get(strc).sBod
        tempStructSize = self.strDic.get(strc).size
        if var not in tempS2:
            tempS2[var] = VarInfo(var, vType, vPar, num, currentVarSize, arr, currentOffset, amb)
            self.structOffset += currentVarSize
            tempStructSize += currentVarSize
            ok = True
        else:
            ok = False
        self.strDic.get(strc).sBod = tempS2
        self.strDic.get(strc).size = tempStructSize
        return ok
    #Busca dentro de las estructuras
    def sStruct(self, strc):
        sVal = None
        if strc in self.strDic:
            sVal = self.strDic[strc]
        return sVal
    #Verifica las propiedades de las estructuras
    def exitLocation(self, ctx: DecafParser.LocationContext):
        var = None
        child = False
        mld = False
        if (ctx.location() != None):
            if self.structs != []:
                table = self.structs.pop()
                if (table != None):
                    var = table.sBod[ctx.getChild(0).getText()]
                    if (var != None):
                        self.nodes[ctx] = self.nodes[ctx.location()]
                        self.currentStructMovement += var.size
            else:
                var = self.sVarTable(ctx.getChild(0).getText(), self.aName)
                if (var != None):
                    self.nodes[ctx] = self.nodes[ctx.location()]
        elif (type(ctx.parentCtx) == DecafParser.LocationContext and ctx.location() == None):
            if self.structs != []:
                table = self.structs.pop()
                if (table != None):
                    var = table.sBod[ctx.getChild(0).getText()]
                    if (var != None):                      
                        self.nodes[ctx] = var.vType    
                        self.currentStructMovement += var.offset
                        child = True 
                        mld = True
        else:
            var = self.sVarTable(ctx.getChild(0).getText(), self.aName)
            if (var != None):
                self.nodes[ctx] = var.vType
        if ctx.expression():
            if var != None:
                if not var.arr:
                    return
                else:
                    if child: 
                        self.arrayInfo = [var.vType, ctx.expression()]
        if var != None:
            if ctx.expression() and mld == False:
                nVar ="T" + str(self.cVar)
                self.cVar += 1
                temp = Lprops(nVar, None, None, None)
                ops = self.nodeArg[ctx.expression()]
                zType = Lprops(str(self.typeSizes[var.vType]), None, None, None)
                self.lcuads.append(Cuadruples('*', ops, zType, temp))
                nVar2 ="T" + str(self.cVar)
                self.cVar += 1
                nVar2Addr = Lprops(nVar2, None, None, None)
                offsetAddr = Lprops(str(var.offset), None, None, None)
                self.lcuads.append(Cuadruples('+', temp, offsetAddr, nVar2Addr))
                self.nodeArg[ctx]= Lprops(self.getCodeContext(var)+"["+str(nVar2)+"]", None, None, None)
            else:
                self.nodeArg[ctx]= Lprops(self.getCodeContext(var)+"["+str(var.offset)+"]", None, None, None)
    #Busca el typo del metodo
    def rMethType(self, amb):
        obj = self.ambDict.get(amb)
        if (obj.sup != "global"):
            obj = self.rMethType(obj.sup)
        return obj
    # Verifica si es global o no
    def getCodeContext(self, var):
        if (var.amb == 'global'):
            codeContext = "G"
        else:
            codeContext = "FP"
        return codeContext
#---------------------------------------------------------------------------------------------------
def main(argv):
    input_stream = FileStream(argv)
    lexer = DecafLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = DecafParser(stream)
    tree = parser.program()  
    printer = DecafPrinter()
    walker = ParseTreeWalker()
    walker.walk(printer, tree)
    lcuads2 = []
    for cuad in printer.lcuads:
        lcuads2.append(printer.PrintCuad(cuad)+"\n")
    file = open("inter.txt","w")
    for i in lcuads2:
        print(i)
        file.write(i)
    return lcuads2