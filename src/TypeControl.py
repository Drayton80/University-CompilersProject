from src.TypeMismatchException import TypeMismatchException

class TypeControl:
    def __init__(self):
        self._stackTypeControl = []

    def value_usage(self, value_class):
        self._stackTypeControl.insert(0, value_class)

    def arithmetic_expression(self):
        topo = self._stackTypeControl.pop()
        subtopo = self._stackTypeControl.pop()

        if topo == 'Número inteiro' and subtopo == 'Número inteiro':
            self._stackTypeControl.insert(0, 'Número inteiro')
        elif topo == 'Número Real' and subtopo == 'Número Real':
            self._stackTypeControl.insert(0, 'Número Real')
        elif topo == 'Número inteiro' and subtopo == 'Número Real':
            self._stackTypeControl.insert(0, 'Número Real')
        elif topo == 'Número Real' and subtopo == 'Número inteiro':
            self._stackTypeControl.insert(0, 'Número Real')
        else:
            raise TypeMismatchException(type1 = topo, type2 = subtopo, operator = 'Expressão Aritimética')
    