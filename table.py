class VarInfo():
    def __init__(self, var, vType, vPar, num, size, arr, offset, amb):
        #nombre de variable
        self.var = var 
        #Tipo de la variable
        self.vType = vType
        #Indica el valor que tiene
        self.value = None
        #Indica el numero asignado
        self.num = num
        #Indica el tamaño
        self.size = size
        self.offset = offset
        #Comprueba si es parametro
        self.vPar = vPar
        #Comprueba si es array True si, False no
        self.arr = arr
        #Indica en que ambito esta
        self.amb = amb
class StructInfo():
    def __init__(self, strc, sBod):
        #nombre de la estructura
        self.strc = strc
        #variables dentro de la estrutura
        self.sBod = sBod
        #Tamaño de la estrucuta
        self.size = 0
class SymbolTableItem():
    def __init__(self, sup, tbl, rType):
        #Contiene el nombre del padre
        self.sup = sup
        #contiene tipo de retono
        self.rType = rType
        #variables del nodo
        self.tbl = tbl
class Cuadruples():
    def __init__(self, op, arg1, arg2, res):
        #Contiene el operador
        self.op = op
        #Contienen el argumento 1
        self.arg1 = arg1
        #Contienen el argumento 2
        self.arg2 = arg2
        #Contienen el resultado
        self.res = res
class Lprops():
    def __init__(self, Name, first, els, go):
        #Contiene el nombre de la funcion
        self.Name = Name
        #COntiene el true
        self.first = first
        #Contiene el false
        self.els = els
        #Contiene que hace despues
        self.go = go