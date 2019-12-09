from src.TypeMismatchException import TypeMismatchException
from src.LogicalExpressionException import LogicalExpressionException


class TypeControl:
    def __init__(self):
        self._stackTypeControl = []
        self._arithmetic_types = ['integer', 'real']
        self._relational_type1 = None
        self._logical_type1 = None

    def value_usage(self, token_value, class_value):
        print('value usage')
        self._stackTypeControl.insert(0, class_value)
        self.print_stack()

    def print_stack(self):
        for value_class in self._stackTypeControl:
            print(value_class)
        print('\n')


    def arithmetic_expression(self):
        print("Arithmetic")
        topo = self._stackTypeControl.pop(0)
        subtopo = self._stackTypeControl.pop(0)
        if topo == 'integer' and subtopo == 'integer':
            self._stackTypeControl.insert(0, 'integer')
        elif topo == 'real' and subtopo == 'real':
            self._stackTypeControl.insert(0, 'real')
        elif topo == 'integer' and subtopo == 'real':
            self._stackTypeControl.insert(0, 'real')
        elif topo == 'real' and subtopo == 'integer':
            self._stackTypeControl.insert(0, 'real')
        else:
            raise TypeMismatchException(type1 = topo, type2 = subtopo, 
                                        operator = 'Expressão Aritimética')
        self.print_stack()
    
    def assignment_expression(self):
        print("assignment")
        topo = self._stackTypeControl.pop(0)
        subtopo = self._stackTypeControl.pop(0)
        self.print_stack()
        if topo != subtopo:
            raise TypeMismatchException(type1 = topo, type2 = subtopo, 
                                        operator = 'Expressão Atribuição')

    def relacional_expression(self):
        print("relational")
        self.print_stack()
        topo = self._stackTypeControl.pop(0)
        subtopo = self._stackTypeControl.pop(0)
        if topo == 'integer' and subtopo == 'integer':
            self._stackTypeControl.insert(0, 'boolean')
        elif topo == 'real' and subtopo == 'real':
            self._stackTypeControl.insert(0, 'boolean')
        elif topo == 'integer' and subtopo == 'real':
            self._stackTypeControl.insert(0, 'boolean')
        elif topo == 'real' and subtopo == 'integer':
            self._stackTypeControl.insert(0, 'boolean')
        else:
            raise TypeMismatchException(type1 = topo, type2 = subtopo, 
                                        operator = 'Expressão Relacional')

    def logical_expression(self):
        print("logical")
        self.print_stack()
        #Quando usado pela primeira vez, fazemos relational pegar o valor da ultima expressão
        topo = self._stackTypeControl.pop(0)
        subtopo = self._stackTypeControl.pop(0)
        if topo == 'boolean' and subtopo == 'boolean':
            self._stackTypeControl.insert(0, 'boolean')
        else:
            raise LogicalExpressionException()

