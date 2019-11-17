import re
import os
import sys

sys.path.append(os.path.abspath(os.path.join('..')))

from src.CommentException import CommentException

class LexicalAnalyzer:
    def __init__(self, code_path: str):
        self._code_path = code_path
        self._keywords = ["program", "var", "integer", "real", "boolean", "procedure", "begin", "end", "if", "then", "else", "while", "do", "not"]
        self._additives = ["and"]
        self._multiplicatives = ["or"]
    
    def state_initial(self, line, character_index, token, code=None):
        if character_index >= len(line):
            return token, "", character_index
        elif re.search(r'[a-zA-Z]', line[character_index]):
            return self.state_identifier(line, character_index + 1, token + line[character_index])
        elif re.search(r'[0-9]', line[character_index]):
            return self.state_integer(line, character_index + 1, token + line[character_index])
        elif re.search(r'[:;.,()]', line[character_index]):
            return self.state_delimeter(line, character_index + 1, token + line[character_index])
        elif re.search(r'[<>=]', line[character_index]):
            return self.state_relational(line, character_index + 1, token + line[character_index])
        elif re.search(r'[+\-]', line[character_index]):
            return self.state_additive(line, character_index + 1, token + line[character_index])
        elif re.search(r'[*\/]', line[character_index]):
            return self.state_multiplicative(line, character_index + 1, token + line[character_index])
        elif code and line[character_index] == '{':
            return self.state_comment(code, character_index + 1, token)
        elif re.search(r'\s', line[character_index]):
            return token, "", character_index + 1
        else:
            return token, "", character_index + 1

    def state_identifier(self, line, character_index, token):
        if character_index >= len(line):
            return token, "Identificador", character_index
        elif re.search(r'[a-zA-Z0-9_]', line[character_index]):
            return self.state_identifier(line, character_index + 1, token + line[character_index])
        else:
            return token, "Identificador", character_index

    def state_integer(self, line, character_index, token):
        if character_index >= len(line):
            return token, "Número inteiro", character_index
        elif re.search(r'[0-9]', line[character_index]):
            return self.state_integer(line, character_index + 1, token + line[character_index])
        elif line[character_index] == '.':
            return self.state_real(line, character_index + 1, token + line[character_index])
        else:
            return token, "Número inteiro", character_index

    def state_real(self, line, character_index, token):
        if character_index >= len(line):
            return token, "Número real", character_index
        elif re.search(r'[0-9]', line[character_index]):
            return self.state_real(line, character_index + 1, token + line[character_index])
        else:
            return token, "Número real", character_index
    
    def state_delimeter(self, line, character_index, token):
        if character_index >= len(line):
            return token, "Delimitador", character_index
        elif line[character_index] == '=':
            return self.state_attribution(line, character_index + 1, token + line[character_index])
        else:
            return token, "Delimitador", character_index

    def state_attribution(self, line, character_index, token):
        return token, "Atribuição", character_index

    def state_relational(self, line, character_index, token):
        if character_index >= len(line):
            return token, "Relacional", character_index
        elif line[character_index - 1] == '>' and line[character_index] == '=' :
            return token + line[character_index], "Relacional", character_index + 1
        elif line[character_index - 1] == '<' and line[character_index] in ['>', '='] :
            return token + line[character_index], "Relacional", character_index + 1
        else:
            return token, "Relacional", character_index

    def state_additive(self, line, character_index, token):
        return token, "Aditivo", character_index

    def state_multiplicative(self, line, character_index, token):
        return token, "Multiplicativo", character_index

    def state_comment(self, code, character_index, token):
        if character_index >= len(code):
            raise CommentException()
        elif code[character_index] == '}':
            return token, "", character_index + 1
        else:
            # Comentários são ignorados, então eles não precisam ter seu token salvo:
            return self.state_comment(code, character_index + 1, token)

    def create_table(self) -> list:
        with open(self._code_path, 'r') as file:
            code = file.read()
            
        line_index = 1
        table = []
        
        for line in code.split('\n'):
            character_index = 0
            
            while character_index < len(line):
                try:
                    token, classificacao, character_index = self.state_initial(line, character_index, "", code)
                except CommentException as exception:
                    print(exception)
                    return []
                
                if classificacao == "Identificador":
                    if token in self._keywords:
                        table.append([token, "Palavra reservada", line_index])
                    elif token in self._additives:
                        table.append([token, "Aditivo", line_index])
                    elif token in self._multiplicatives:
                        table.append([token, "Multiplicativo", line_index])
                    else:
                        table.append([token, classificacao, line_index])
                elif classificacao != "":
                    table.append([token, classificacao, line_index])

            line_index += 1
        
        for element in table:
                print(element)
                    

LexicalAnalyzer('../data/input.txt').create_table()