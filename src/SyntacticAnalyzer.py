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
        if self._lexical_table != []:
            self._current_value = self._lexical_table.pop()
        else:
            self._current_value = {'token': '', 'class': '', 'line': ''}

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
                self._argument()
                
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

    def _argument(self):
        if self._current_value['token'] == '(':
            self._next_value()
            self._list_parameters1()
        
            if self._next_value()['token'] != ')':
                print("ERRO na Linha:", self._current_value['line'])
        else:
            return None

    def _list_parameters1(self):
        self._next_value()
        self._list_identifiers1()
        
        if self._next_value()['token'] == ":":
            self._next_value()
            self._type()

            self._next_value()
            self._list_parameters2()
        else:
            print("ERRO na Linha:", self._current_value['line'])

    def _list_parameters2(self):
        if self._current_value['token'] == ";":
            self._next_value()
            self._list_identifiers1()

            if self._next_value()['token'] == ":":
                self._next_value()
                self._type()

                self._next_value()
                self._list_parameters2()
            else:
               print("ERRO na Linha:", self._current_value['line']) 
        else:
            return None

    def _compound_statement(self):
        if self._current_value['token'] == 'begin':
            # More legible representation for Optional Statements:
            if self._next_value()['token'] == 'end':
                return None
            else:
                self._list_statement1()

                if self._current_value['token'] != 'end':
                    print("ERRO na Linha:", self._current_value['line'])
            
        else:
            print("ERRO na Linha:", self._current_value['line'])      

    def _optional_statement(self):
        if self._current_value['token'] != 'end':
            self._next_value()
            self._list_statement1()
        else:
            return None

    def _list_statement1(self):
        self._statement()

        self._next_value()
        self._list_statement2()

    def _list_statement2(self):
        if self._current_value['token'] == ';':
            self._next_value()
            self._statement()
            
            if self._next_value()['token'] == 'end':
                return None
            else:
                self._list_statement2()
        else:
            print("ERRO na Linha:", self._current_value['line'])   

    def _statement(self):
        if self._current_value['class'] == 'Identificador':
            previous_value = self._current_value

            if self._next_value()['token'] == ':=':
                self._next_value()
                self._variable()
            else:
                self._lexical_table.insert(0, self._current_value)
                self._current_value = previous_value
                self._activation_procedure()
        
        elif self._current_value['token'] == 'begin':
            self._next_value()
            self._compound_statement()
        
        elif self._current_value['token'] == 'while':
            self._next_value()
            self._expression()

            if self._next_value()['token'] == 'do':
                self._next_value()
                self._statement()
            else:
                print("ERRO na Linha:", self._current_value['line']) 

        elif self._current_value['token'] == 'if':
            self._expression()

            if self._next_value()['token'] == 'then':
                self._statement()

                self._next_value()
                self._else()
            else:
                print("ERRO na Linha:", self._current_value['line']) 

        else:
            print("ERRO na Linha:", self._current_value['line']) 

    def _else(self):
        if self._current_value['token'] == 'else':
            self._next_value()
            self._statement()
        else:
            return None

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
                    