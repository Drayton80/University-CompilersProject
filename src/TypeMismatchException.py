class TypeMismatchException(Exception):        
    def __init__(self, type1, type2, operator):
        self._type1 = type1
        self._type2 = type2
        self._operator = operator
    
    def __str__(self):
        return "O operador " + str(self._operator) + " está sendo usado com os tipos " + str(self._type1) + " e " + str(self._type2) + ", os quais são inválidos em conjunto nessa operação"