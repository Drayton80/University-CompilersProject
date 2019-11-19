import re
import os
import sys

sys.path.append(os.path.abspath(os.path.join('..')))

from src.CommentException import CommentException
from src.WrongSymbolException import WrongSymbolException

class LexicalAnalyzer:
    def __init__(self, code_path: str):
        self._code_path = code_path
        self._keywords = ["program", "var", "integer", "real", "boolean", "procedure", "begin", "end", "if", "then", "else", "while", "do", "not"]
        self._additives = ["or"]
        self._multiplicatives = ["and"]
    
    def state_initial(self, code, line_index, character_index, token):
        if code[character_index] == "\n":
            return token, "", character_index + 1, line_index + 1
        elif re.search(r'[a-zA-Z]', code[character_index]):
            return self.state_identifier(code, line_index, character_index + 1, token + code[character_index])
        elif re.search(r'[0-9]', code[character_index]):
            return self.state_integer(code, line_index, character_index + 1, token + code[character_index])
        elif re.search(r'[:;.,()]', code[character_index]):
            return self.state_delimeter(code, line_index, character_index + 1, token + code[character_index])
        elif re.search(r'[<>=]', code[character_index]):
            return self.state_relational(code, line_index, character_index + 1, token + code[character_index])
        elif re.search(r'[+\-]', code[character_index]):
            return self.state_additive(code, line_index, character_index + 1, token + code[character_index])
        elif re.search(r'[*\/]', code[character_index]):
            return self.state_multiplicative(code, line_index, character_index + 1, token + code[character_index])
        elif code and code[character_index] == '{':
            return self.state_comment(code, line_index, character_index + 1, token)
        elif code and code[character_index] == '}':
            raise CommentException()
        elif re.search(r'\s', code[character_index]):
            return token, "", character_index + 1, line_index
        else:
            raise WrongSymbolException()

    def state_identifier(self, code, line_index, character_index, token):
        if code[character_index] == "\n":
            return token, "Identificador", character_index + 1, line_index + 1
        elif re.search(r'[a-zA-Z0-9_]', code[character_index]):
            return self.state_identifier(code, line_index, character_index + 1, token + code[character_index])
        else:
            return token, "Identificador", character_index, line_index

    def state_integer(self, code, line_index, character_index, token):
        if code[character_index] == "\n":
            return token, "Número inteiro", character_index + 1, line_index + 1
        elif re.search(r'[0-9]', code[character_index]):
            return self.state_integer(code, line_index, character_index + 1, token + code[character_index])
        elif code[character_index] == '.':
            return self.state_real(code, line_index, character_index + 1, token + code[character_index])
        else:
            return token, "Número inteiro", character_index, line_index

    def state_real(self, code, line_index, character_index, token):
        if code[character_index] == "\n":
            return token, "Número real", character_index + 1, line_index + 1
        elif re.search(r'[0-9]', code[character_index]):
            return self.state_real(code, line_index, character_index + 1, token + code[character_index])
        else:
            return token, "Número real", character_index, line_index
    
    def state_delimeter(self, code, line_index, character_index, token):
        if code[character_index] == "\n":
            return token, "Delimitador", character_index + 1, line_index + 1
        elif code[character_index] == '=':
            return self.state_attribution(code, line_index, character_index + 1, token + code[character_index])
        else:
            return token, "Delimitador", character_index, line_index

    def state_attribution(self, code, line_index, character_index, token):
        if code[character_index] == "\n":
            return token, "Atribuição", character_index + 1, line_index + 1
        else:
            return token, "Atribuição", character_index, line_index

    def state_relational(self, code, line_index, character_index, token):
        if code[character_index] == "\n":
            return token, "Relacional", character_index + 1, line_index + 1
        elif code[character_index - 1] == '>' and code[character_index] == '=' :
            return token + code[character_index], "Relacional", character_index + 1, line_index
        elif code[character_index - 1] == '<' and code[character_index] in ['>', '='] :
            return token + code[character_index], "Relacional", character_index + 1, line_index
        else:
            return token, "Relacional", character_index, line_index

    def state_additive(self, code, line_index, character_index, token):
        if code[character_index] == "\n":
            return token, "Aditivo", character_index + 1, line_index + 1
        else:
            return token, "Aditivo", character_index, line_index

    def state_multiplicative(self, code, line_index, character_index, token):
        if code[character_index] == "\n":
            return token, "Multiplicativo", character_index + 1, line_index + 1
        else:
            return token, "Multiplicativo", character_index, line_index

    def state_comment(self, code, line_index, character_index, token):
        if character_index >= len(code):
            raise CommentException()
        elif code[character_index] == '\n':
            return self.state_comment(code, line_index + 1, character_index + 1, token)
        elif code[character_index] == '}':
            return token, "", character_index + 1, line_index
        else:
            # Comentários são ignorados, então eles não precisam ter seu token salvo:
            return self.state_comment(code, line_index, character_index + 1, token)

    def create_table(self) -> list:
        with open(self._code_path, 'r') as file:
            code = file.read()    
        
        table = []
        line_index = 1
        character_index = 0
        
        while character_index < len(code) and line_index <= len(code.split('\n')):
            try:
                token, classificacao, character_index, line_index = self.state_initial(code, line_index, character_index, "")
            except CommentException as exception:
                print(exception)
                return []
            except WrongSymbolException as exception:
                print(exception)
                return []
            
            if classificacao == "Identificador":
                if token in self._keywords:
                    table.append({'token': token, 'class': "Palavra reservada", 'line': line_index})
                elif token in self._additives:
                    table.append({'token': token, 'class': "Aditivo", 'line': line_index})
                elif token in self._multiplicatives:
                    table.append({'token': token, 'class': "Multiplicativo", 'line': line_index})
                else:
                    table.append({'token': token, 'class': classificacao, 'line': line_index})
            elif classificacao != "":
                table.append({'token': token, 'class': classificacao, 'line': line_index})

        line_index += 1

        return table
        
        
table = LexicalAnalyzer('../data/input.txt').create_table()

for element in table:
    print(element)