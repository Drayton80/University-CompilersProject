import os
import sys

sys.path.append(os.path.abspath(os.path.join('..')))

from src.IdentifierDeclarationException import IdentifierDeclarationException
from src.UsingNotDeclaredException import UsingNotDeclaredException


class IdentifierInformation:
    def __init__(self, identifier_token, identifier_type):
        self._token = identifier_token
        self._type = identifier_type


class SymbolTable:
    def __init__(self):
        self._stack = []

    def print_stack(self):
        print('\n NOVO ESTADO')
        for identifier in self._stack:
            print(identifier._token, sep='')

    def block_entrance(self):
        self._stack.insert(0, IdentifierInformation('$', None))
        self.print_stack()

    def identifier_declaration(self, identifier_declared: IdentifierInformation):
        aux_stack = self._stack.copy()
        
        for identifier in aux_stack:
            if identifier._token == '$':
                self._stack.insert(0, identifier_declared)
                self.print_stack()
                break
            elif identifier_declared._token == identifier._token:
                print(identifier_declared._token, identifier._token)
                raise IdentifierDeclarationException(identifier_declared._token)

    def identifier_usage(self, token: str):
        for identifier in self._stack:
            if token == identifier._token:
                return identifier
        raise UsingNotDeclaredException(token)

    def block_exit(self):
        print('limpou')
        for identifier in self._stack:
            if identifier._token == '$':
                self._stack.pop(0)
                self.print_stack()
                break
            else:
                self._stack.pop(0)