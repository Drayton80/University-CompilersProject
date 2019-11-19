import re
import os
import sys

sys.path.append(os.path.abspath(os.path.join('..')))

from src.LexicalAnalyzer import LexicalAnalyzer


class SyntacticAnalyzer:
    def __init__(self, code_path: str):
        self._lexical_table = LexicalAnalyzer(code_path).create_table()
        self._current_value = None
    
    def _next_value(self):
        self._current_value = self._lexical_table.pop()
        return self._current_value

    def _variables_declaration(self):
        if self._current_value['token'] == 'var':
            self._list_variable_declaration()

    def _list_variable_declaration(self):
        pass

    def _procedures_declaration(self):
        pass

    def _compound_statement(self):
        pass

    def program(self):
        if self._next_value()['token'] == 'program':
            if self._next_value()['class'] == 'Identificador':
                if self._next_value()['token'] == ';':
                    self._next_value()
                    self._variables_declaration()
                    self._procedures_declaration()
                    self._compound_statement()

                    if self._next_value()['token'] != '.':
                        print('ERRO')
                    