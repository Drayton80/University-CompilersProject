import re
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

    def block_entrance(self):
        self._stack.insert(0, IdentifierInformation('$', None))

    def identifier_declaration(self, identifier_declared: IdentifierInformation):
        for identifier in self._stack:
            if identifier._token == '$':
                self._stack.insert(0, identifier)
            elif identifier_declared._token == identifier._token:
                raise IdentifierDeclarationException(identifier_declared._token)

    def identifier_usage(self, identifier_used: IdentifierInformation):
        for identifier in self._stack:
            if identifier_used._token == identifier._token:
                return identifier
        
        raise UsingNotDeclaredException(identifier_used._token)

    def block_exit(self):
        for identifier in self._stack:
            if identifier._token == '$':
                self._stack.pop(0)
                break
            else:
                self._stack.pop(0)
            