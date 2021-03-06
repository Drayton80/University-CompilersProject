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
    
    def state_initial(self, code, line_index, character_index, token, dimensionality_already_checked=False):
        if code[character_index] == "\n":
            return token, "", character_index + 1, line_index + 1
        elif re.search(r'[a-zA-Z]', code[character_index]):
            return self.state_identifier(code, line_index, character_index + 1, token + code[character_index], dimensionality_already_checked=dimensionality_already_checked)
        elif re.search(r'[0-9]', code[character_index]):
            return self.state_integer(code, line_index, character_index + 1, token + code[character_index])
        elif re.search(r'[;.,()]', code[character_index]):
            return self.state_delimeter1(code, line_index, character_index + 1, token + code[character_index])
        elif re.search(r'[:]', code[character_index]):
            return self.state_delimeter2(code, line_index, character_index + 1, token + code[character_index])
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

    def state_identifier(self, code, line_index, character_index, token, dimensionality_already_checked=False):
        if re.search(r'[a-zA-Z0-9_]', code[character_index]):
            return self.state_identifier(code, line_index, character_index + 1, token + code[character_index], dimensionality_already_checked=dimensionality_already_checked)
        elif not dimensionality_already_checked and code[character_index] == '.':
            return self.state_bidimensional(code, line_index, character_index + 1, token + code[character_index])
        else:
            return token, "Identificador", character_index, line_index

    def state_bidimensional(self, code, line_index, character_index, token, first_character_checked=False):
        if re.search(r'[a-zA-Z0-9_]', code[character_index]):
            return self.state_bidimensional(code, line_index, character_index + 1, token + code[character_index], first_character_checked=True)
        elif not first_character_checked:
            return self.state_initial(code, line_index, character_index - len(token), '', dimensionality_already_checked=True)
        elif code[character_index] == '.':
            return self.state_tridimensional(code, line_index, character_index + 1, token + code[character_index])
        else:
            return self.state_initial(code, line_index, character_index - len(token), '', dimensionality_already_checked=True)
            #return token, "Identificador Bidimensional", character_index, line_index
    
    def state_tridimensional(self, code, line_index, character_index, token, first_character_checked=False):
        if re.search(r'[a-zA-Z0-9_]', code[character_index]):
            return self.state_tridimensional(code, line_index, character_index + 1, token + code[character_index], first_character_checked=True)
        elif not first_character_checked:
            return self.state_initial(code, line_index, character_index - len(token), '', dimensionality_already_checked=True)
        else:
            return token, "Identificador Tridimensional", character_index, line_index

    def state_integer(self, code, line_index, character_index, token):
        if re.search(r'[0-9]', code[character_index]):
            return self.state_integer(code, line_index, character_index + 1, token + code[character_index])
        elif code[character_index] == '.':
            return self.state_real(code, line_index, character_index + 1, token + code[character_index])
        else:
            return token, "Número inteiro", character_index, line_index

    def state_real(self, code, line_index, character_index, token):
        if re.search(r'[0-9]', code[character_index]):
            return self.state_real(code, line_index, character_index + 1, token + code[character_index])
        else:
            return token, "Número real", character_index, line_index

    def state_delimeter1(self, code, line_index, character_index, token):
        return token, "Delimitador", character_index, line_index
    
    def state_delimeter2(self, code, line_index, character_index, token):
        if code[character_index] == '=':
            return self.state_attribution(code, line_index, character_index + 1, token + code[character_index])
        else:
            return token, "Delimitador", character_index, line_index

    def state_attribution(self, code, line_index, character_index, token):
        return token, "Atribuição", character_index, line_index

    def state_relational(self, code, line_index, character_index, token):
        if code[character_index - 1] == '>' and code[character_index] == '=' :
            return token + code[character_index], "Relacional", character_index + 1, line_index
        elif code[character_index - 1] == '<' and code[character_index] in ['>', '='] :
            return token + code[character_index], "Relacional", character_index + 1, line_index
        else:
            return token, "Relacional", character_index, line_index

    def state_additive(self, code, line_index, character_index, token):
        return token, "Aditivo", character_index, line_index

    def state_multiplicative(self, code, line_index, character_index, token):
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
            code = file.read() + '\n'
        
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
            except IndexError:
                return table
            
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

        return table
        
        
# table = LexicalAnalyzer('../data/input.txt').create_table()

# for element in table:
#     print(element)