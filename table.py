class VarInfo():
    def __init__(self, var, vType, vPar, arr):
        #vPar 0:normla 1:param
        #nombre de variable
        self.var = var 
        #Tipo de la variable
        self.vType = vType
        #Comprueba si es parametro o no , 0 no, 1 si
        self.vPar = vPar
        #Comprueba si es array True si, False no
        self.arr = arr
class StructInfo():
    def __init__(self, strc, sBod):
        #nombre de la estructura
        self.strc = strc
        # variables dentro de la estrutura
        self.sBod = sBod
class Table():
    def __init__(self, sup, tbl, rType):
        #Contiene el nombre del padre
        self.sup = sup
        #contiene tipo de retono
        self.rType = rType
        #variables del nodo
        self.tbl = tbl