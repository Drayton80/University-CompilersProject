import os
import sys

sys.path.append(os.path.abspath(os.path.join('..')))

from src.IdentifierDeclarationException import IdentifierDeclarationException
from src.UsingNotDeclaredException import UsingNotDeclaredException

class IdentifierInformation:
    def __init__(self, value_token, new_identifier_type):
        self._token = value_token
        self._type = new_identifier_type

class SymbolTable:
    def __init__(self):
        self._stack = []

    #Método usado para printar a pilha
    def print_stack(self):
        for identifier in self._stack:
            print(identifier._token, ' - ' , identifier._type, sep='')
        print('\n')

    #Método usado para começar um novo escopo
    def block_entrance(self):
        self._stack.insert(0, IdentifierInformation('$', None))

    #Método usado para colocar uma lista com as novas variáveis, na pilha
    def identifier_declaration_token(self, new_identifiers_tokens: list):
        #Primeiro a gente faz a checagem se o argumento foi mandado corretamente como uma lista
        if not isinstance(new_identifiers_tokens, list):
            #Se não a gente transforma ele em lista
            new_identifiers_tokens = [new_identifiers_tokens]
        
        #Depois nós vamos percurrer todos os objetos da pilha
        for stack_identifier in self._stack.copy():
            #Se ao percorrer a pilha, encontrarmos um token dentre daqueles que iriamos colocar
            if stack_identifier._token in new_identifiers_tokens:
                #Ocorreu o erro de variável duplicada
                raise IdentifierDeclarationException(stack_identifier._token)
            #Caso a gente chegue até o final, significa que tá tudo certo e pode adicionar na stack 
            elif stack_identifier._token == '$':
                for identifier_token in new_identifiers_tokens:
                    self._stack.insert(0, IdentifierInformation(identifier_token, None))
                break
            
    # Função que dado a lista de novas variáveis colocadas na pilha, definimos o seu tipo
    # search_tokens: list - Lista de novas variáveis
    # new_identifier_type: str - Tipo das novas variáveis
    # ignore_end_block_symbol=False - Ainda não sei
    def identifier_declaration_type(self, search_tokens: list, new_identifier_type: str, ignore_end_block_symbol=False):
        #Primeiro a gente faz a checagem se o argumento foi mandado corretamente como uma lista
        if not isinstance(search_tokens, list):
            #Se não a gente transforma ele em lista
            search_tokens = [search_tokens]
        
        stack_index = 0
        
        #Aqui vamos percorrer a lista, procurando as variáveis e taggiando os seus tipos
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