import os
import sys

sys.path.append(os.path.abspath(os.path.join('..')))

from src.TypeMismatchException import TypeMismatchException
from src.AttribuitionMismatchException import AttribuitionMismatchException


class TypeControlStack:
    def __init__(self):
        self._stack = []

    def _print_stack(self):
        for stack_identifier in self._stack:
            print(stack_identifier)
        print('\n')

    def push(self, new_type):
        self._stack.insert(0, new_type)
    
    def get_top(self):
        if len(self._stack) >= 1:
            return self._stack[0]

    def get_subtop(self):
        if len(self._stack) >= 2:
            return self._stack[1]

    def update(self, result_type: str):
        #self._print_stack()
        if self._stack != []:
            self._stack.pop(0)
        if self._stack != []:
            self._stack.pop(0)
            
        self._stack.insert(0, result_type)

    def check_arithmetical(self):
        if self.get_top() == 'integer' and self.get_subtop() == 'integer':
            self.update('integer')
        elif self.get_top() == 'integer' and self.get_subtop() == 'real':
            self.update('real')
        elif self.get_top() == 'real' and self.get_subtop() == 'integer':
            self.update('real')
        elif self.get_top() == 'real' and self.get_subtop() == 'real':
            self.update('real')
        else:
            raise TypeMismatchException(self.get_subtop(), self.get_top(), 'aritmético')

    def check_relational(self):
        if self.get_top() == 'integer' and self.get_subtop() == 'integer':
            self.update('boolean')
        elif self.get_top() == 'integer' and self.get_subtop() == 'real':
            self.update('boolean')
        elif self.get_top() == 'real' and self.get_subtop() == 'integer':
            self.update('boolean')
        elif self.get_top() == 'real' and self.get_subtop() == 'real':
            self.update('boolean')
        else:
            raise TypeMismatchException(self.get_subtop(), self.get_top(), 'relacional')

    def check_logical(self):
        if self.get_top() == 'boolean' and self.get_subtop() == 'boolean':
            self.update('boolean')
        else:
            raise TypeMismatchException(self.get_subtop(), self.get_top(), 'lógico')

    def check_atribuition(self, identifier_type):        
        if self.get_top() == identifier_type:
            self._stack.pop(0)
        elif self.get_top() == 'integer' and identifier_type == 'real':
            self._stack.pop(0)
        else:
            raise AttribuitionMismatchException()