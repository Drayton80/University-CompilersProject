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
        for identifier in self._stack:
            print(identifier._token, sep='')

    def block_entrance(self):
        self._stack.insert(0, IdentifierInformation('$', None))

    def identifier_declaration(self, identifier_token: str, identifier_type: str):       
        for identifier in self._stack.copy():
            if identifier._token == '$':
                self._stack.insert(0, IdentifierInformation(identifier_token, identifier_type))
                break
            elif identifier_token == identifier._token:
                raise IdentifierDeclarationException(identifier_token)
    
    def identifier_type_redefinition(self, search_tokens: list, new_identifier_type: str):
        if not isinstance(search_tokens, list):
            search_tokens = [search_tokens]
        
        stack_index = 0
        
        for identifier in self._stack:
            if search_token == identifier['token']:
                self._stack[stack_index]._type = new_identifier_type
            
            stack_index += 1

    def identifier_usage(self, token: str):
        for identifier in self._stack:
            if token == identifier._token:
                return identifier
        raise UsingNotDeclaredException(token)

    def block_exit(self):
        for identifier in self._stack.copy():
            if identifier._token == '$':
                self._stack.pop(0)
                break
            else:
                self._stack.pop(0)