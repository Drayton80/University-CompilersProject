import re
import os
import sys

sys.path.append(os.path.abspath(os.path.join('..')))

class LexicalAnalyzer:
    def __init__(self, code_path: str):
        self._code_path = code_path
        self._keywords = ["program", "var", "integer", "real", "boolean", "procedure", "begin", "end", "if", "then", "else", "while", "do", "not"]
    
    def _find_all_indexes(input_string, search_string):
        l1 = []
        length = len(input_string)
        index = 0
        while index < length:
            i = input_string.find(search_string, index)
            if i == -1:
                return l1
            l1.append(i)
            index = i + 1
        return l1
    
    def _validate_comments(self, code: str) -> bool:
        open_braces = re.findall(r'\{', code)
        close_braces = re.findall(r'\}', code)

        if len(open_braces) != len(close_braces):
            return False
        else:
            return True

    def _validate_symbols(self, code: str) -> bool:
        if re.search(r'[^A-Za-z0-9:=\s_;.:=<>*/+\-,(){}]', code):
            return False
        else:
            return True

    def _delete_comments(self, code: str) -> str:
        stack = []

        index = 0
        
        for character in code:
            if character == '{':
                stack.append(index)
            elif character == '}':
                try:
                    inicio = stack.pop()
                    fim = index + 1
                    if '\n' in code[inicio:fim]:
                        code = code.replace(code[inicio:fim], "\n")
                    else:
                        code = code.replace(code[inicio:fim], "")
                except Exception:
                    pass
            index += 1
        
        return code
        

    
    def _get_identifiers(self, line: str):
        return re.findall(r'\b[a-zA-Z]+[0-9a-zA-Z_]*\b', line)

    def _get_keywords(self, identifiers: list):
        matched_keywords = []
        
        index = 0

        for identifier in identifiers:
            if identifier in self._keywords:
                matched_keywords.append(identifier)
                del(identifiers[index])

            index += 1

        return matched_keywords

    def _get_integers(self, line: str):
        return re.findall(r'\b[0-9]+\b', line)

    def _get_real(self, line: str):
        return re.findall(r'\b[0-9]+[.][0-9]*\b', line)

    def _get_delimeters(self, line: str):
        return re.findall(r'[\ba-zA-Z0-9_\s][;:,.()][\ba-zA-Z0-9_\s]', line)
        
        '''delimeters = []
        
        for index in range(len(line)):
            if line[index] in [';', '.', '(', ')']:
                delimeters.append(line[index])
            elif line[index] == ':':
                if index + 1 < len(line) and line[index+1] != '=':
                    delimeters.append(line[index])'''
        
    def create_table(self) -> list:
        with open(self._code_path, 'r') as file:
            code = file.read()

        if not self._validate_symbols(code) or not self._validate_comments(code):
            print("erro")
            return None
        
        self._delete_comments(code)
        
        line_index = 0

        for line in code.split('\n'):
            line = line.replace('\n', '')

            identifiers = self._get_identifiers(line)
            keywords = self._get_keywords(identifiers)
            integers = self._get_integers(line)
            delimeters = self._get_delimeters(line)

            print(delimeters)

            
            line_index += 1








LexicalAnalyzer('../data/input.txt').create_table()