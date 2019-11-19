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
            self._next_value()
            self._list_variable_declaration1()
        else:
            return None

    def _list_variable_declaration1(self):
        self._list_identifiers1()

        if self._next_value()['token'] == ':':
            self._next_value()
            self._type()
            
            if self._next_value()['token'] == ';':   
                self._next_value()
                self._list_variable_declaration2()
            else:
                print("ERRO na Linha:", self._current_value['line'])
        else:
            print("ERRO na Linha:", self._current_value['line'])

    def _list_variable_declaration2(self):
        if self._current_value['class'] == 'Identificador':
            self._list_identifiers1()
            
            if self._next_value()['token'] == ':':
                self._next_value()
                self._type()
                
                if self._next_value()['token'] == ';':
                    self._next_value()
                    self._list_variable_declaration2()
                else:
                    print("ERRO na Linha:", self._current_value['line'])
            else:
                print("ERRO na Linha:", self._current_value['line'])
        else:
            return None

    def _list_identifiers1(self):
        if self._current_value['class'] == 'Identificador':
            self._next_value()
            self._list_identifiers2()
        else:
            print("ERRO na Linha:", self._current_value['line'])

    def _list_identifiers2(self):
        if self._current_value['token'] == ',':
            if self._current_value['class'] == 'Identificador':
                self._next_value()
                self._list_identifiers2()
            else:
                print("ERRO na Linha:", self._current_value['line'])
        else:
            return None

    def _type(self):
        if self._current_value['class'] == 'Número inteiro':
            return None
        elif self._current_value['class'] == 'Número real':
            return None
        elif self._current_value['class'] == 'Booleano':
            return None
        else:
            print("ERRO na Linha:", self._current_value['line'])

    def _list_procedures_declaration1(self):
        self._procedure_declaration()

        if self._next_value()['token'] == ';':
            self._list_procedures_declaration2()
        else:
            print("ERRO na Linha:", self._current_value['line'])

    def _list_procedures_declaration2(self):
        if self._next_value()['token'] == 'procedure':
            self._procedure_declaration()

            if self._next_value()['token'] == ';':
                self._list_procedures_declaration2()
            else:
                print("ERRO na Linha:", self._current_value['line'])
        else:
            return None
        
    
    def _procedure_declaration(self):
        if self._current_value['token'] == 'procedure':
            if self._next_value()['class'] == "Identificador":
                self._next_value()
                self._aurgment()
                
                if self._next_value()['token'] == ';':
                    self._next_value()
                    self._variables_declaration()
                    
                    self._next_value()
                    self._list_procedures_declaration1()
                    
                    self._next_value()
                    self._compound_statement()
                else:
                    print("ERRO na Linha:", self._current_value['line'])
            else:
                print("ERRO na Linha:", self._current_value['line'])

    def _aurgment(self):
        pass

    def _compound_statement(self):
        pass

    def program(self):
        if self._next_value()['token'] == 'program':
            if self._next_value()['class'] == 'Identificador':
                if self._next_value()['token'] == ';':
                    self._next_value()
                    self._variables_declaration()
                    
                    self._next_value()
                    self._list_procedures_declaration1()
                    
                    self._next_value()
                    self._compound_statement()

                    if self._next_value()['token'] != '.':
                        print("ERRO na Linha:", self._current_value['line'])
                    