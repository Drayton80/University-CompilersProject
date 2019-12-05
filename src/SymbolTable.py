import os
import sys

sys.path.append(os.path.abspath(os.path.join('..')))

from src.IdentifierDeclarationException import IdentifierDeclarationException
from src.UsingNotDeclaredException import UsingNotDeclaredException

class IdentifierInformation:
    def __init__(self, value_token, new_identifier_type):
        self._value = value_token
        self._type = new_identifier_type

class SymbolTable:
    def __init__(self):
        self._stack = []

    def print_stack(self):
        for identifier in self._stack:
            print(identifier._token, ' - ' , identifier._type, sep='')
        print('\n')

    def block_entrance(self):
        self._stack.insert(0, IdentifierInformation('$', None))

    def identifier_declaration_token(self, new_identifiers_tokens: list):       
        if not isinstance(new_identifiers_tokens, list):
            new_identifiers_tokens = [new_identifiers_tokens]
        
        for stack_identifier in self._stack.copy():
            if stack_identifier._token == '$':
                for identifier_token in new_identifiers_tokens:
                    self._stack.insert(0, IdentifierInformation(identifier_token, None))
                break
            elif stack_identifier._token in new_identifiers_tokens:
                raise IdentifierDeclarationException(stack_identifier._token)
    
    def identifier_declaration_type(self, search_tokens: list, new_identifier_type: str, ignore_end_block_symbol=False):
        if not isinstance(search_tokens, list):
            search_tokens = [search_tokens]
        
        stack_index = 0
        
        for stack_identifier in self._stack:
            if stack_identifier._token in search_tokens:
                self._stack[stack_index]._type = new_identifier_type
            elif not ignore_end_block_symbol and stack_identifier._token == '$':
                break
            
            stack_index += 1

    def identifier_usage(self, token: str):
        for stack_identifier in self._stack:
            if token == stack_identifier._token:
                return stack_identifier
        raise UsingNotDeclaredException(token)

    def block_exit(self):
        #self.print_stack()
        for identifier in self._stack.copy():
            if identifier._token == '$':
                self._stack.pop(0)
                break
            else:
                self._stack.pop(0)