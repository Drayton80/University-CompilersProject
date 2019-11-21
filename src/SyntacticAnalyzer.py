import re
import os
import sys

sys.path.append(os.path.abspath(os.path.join('..')))

from src.LexicalAnalyzer import LexicalAnalyzer
from src.SyntacticException import SyntacticException


class SyntacticAnalyzer:
    def __init__(self, code_path: str):
        self._lexical_table = LexicalAnalyzer(code_path).create_table()
        self._current_value = None
        self._old_value = None
    
    def _next_value(self):
        if self._lexical_table != []:
            self._old_value = self._current_value
            self._current_value = self._lexical_table.pop(0)
        else:
            self._current_value = {'token': '', 'class': '', 'line': ''}

        return self._current_value

    def _previous_value(self):
        if self._old_value:
            if self._current_value['token'] != '':
                self._lexical_table.insert(0, self._current_value)
                
            self._current_value = self._old_value
        
        return self._old_value


    def _variables_declaration(self):
        if self._current_value['token'] == 'var':
            self._next_value()
            self._list_variable_declaration1()
        else:
            return None

    def _list_variable_declaration1(self):
        self._list_identifiers1()
        
        if self._current_value['token'] == ':':
            self._next_value()
            self._type()
            
            if self._next_value()['token'] == ';':   
                self._next_value()
                self._list_variable_declaration2()
            else:
                raise SyntacticException('; faltando', self._current_value['line'])
        else:
            raise SyntacticException('separador : faltando', self._current_value['line'])

    def _list_variable_declaration2(self):
        if self._current_value['class'] == 'Identificador':
            self._list_identifiers1()
            
            if self._current_value['token'] == ':':
                self._next_value()
                self._type()
                
                if self._next_value()['token'] == ';':
                    self._next_value()
                    self._list_variable_declaration2()
                else:
                    raise SyntacticException('; faltando', self._current_value['line'])
            else:
                raise SyntacticException('separador : faltando', self._current_value['line'])
        else:
            self._previous_value()
            return None

    def _list_identifiers1(self):
        if self._current_value['class'] == 'Identificador':
            self._next_value()
            self._list_identifiers2()
        else:
            raise SyntacticException('identificador de variável faltando', self._current_value['line'])

    def _list_identifiers2(self):
        if self._current_value['token'] == ',':
            self._next_value()
            if self._current_value['class'] == 'Identificador':
                self._next_value()
                self._list_identifiers2()
            else:
                raise SyntacticException('identificador de variável faltando', self._current_value['line'])
        else:
            return None

    def _type(self):
        if self._current_value['token'] in ['integer', 'real', 'boolean', 'char', 'string']:
            return None
        else:
            raise SyntacticException('tipo da variável não especificado', self._current_value['line'])

    def _list_procedures_declaration1(self):
        if self._current_value['token'] == 'procedure':
            self._procedure_declaration()

            if self._next_value()['token'] == ';':
                self._list_procedures_declaration2()
            else:
                raise SyntacticException('; faltando', self._current_value['line'])
        else:
            self._previous_value()
            return None

    def _list_procedures_declaration2(self):
        if self._current_value['token'] == 'procedure':
            self._procedure_declaration()

            if self._next_value()['token'] == ';':
                self._list_procedures_declaration2()
            else:
                raise SyntacticException('; faltando', self._current_value['line'])
        else:
            self._previous_value()
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
                    raise SyntacticException('; faltando', self._current_value['line'])
            else:
                raise SyntacticException('procedure faltando', self._current_value['line'])

    def _argument(self):
        if self._current_value['token'] == '(':
            self._next_value()
            self._list_parameters1()
        
            if self._current_value['token'] != ')':
                raise SyntacticException('Argumento sem fechamento \')\'', self._current_value['line'])
        else:
            return None

    def _list_parameters1(self):
        self._list_identifiers1()
        
        if self._current_value['token'] == ":":
            self._next_value()
            self._type()

            self._next_value()
            self._list_parameters2()
        else:
            raise SyntacticException('Faltando separador \':\'', self._current_value['line'])

    def _list_parameters2(self):
        if self._current_value['token'] == ";":
            self._next_value()
            self._list_identifiers1()

            if self._current_value['token'] == ":":
                self._next_value()
                self._type()

                self._next_value()
                self._list_parameters2()
            else:
               raise SyntacticException('Faltando separador \':\'', self._current_value['line']) 
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
                    raise SyntacticException('Comando composto não fechado com end', self._current_value['line'])
            
        else:
            raise SyntacticException('Comando composto não iniciado com begin', self._current_value['line'])      

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
            if self._current_value['token'] == 'end':
                return None
            self._statement()
            
            self._next_value()
            self._list_statement2()
        else:
            raise SyntacticException('Faltando separador \';\' entre comandos', self._current_value['line'])   

    def _statement(self):
        if self._current_value['class'] == 'Identificador':         
            if self._next_value()['token'] == ':=':
                self._next_value()
                # self._variable() #Perguntar pro draytim
                self._expression()
            else:
                self._previous_value()
                self._activation_procedure()
        
        elif self._current_value['token'] == 'begin':
            self._next_value()
            self._compound_statement()
        
        elif self._current_value['token'] == 'while':
            
            self._next_value()
            self._expression()

            print(self._lexical_table[0])
            if self._next_value()['token'] == 'do':
                self._next_value()
                self._statement()
            else:
                raise SyntacticException('Faltando \'do\' após \'while\'', self._current_value['line']) 

        elif self._current_value['token'] == 'if':
            self._expression()

            if self._next_value()['token'] == 'then':
                self._statement()

                self._next_value()
                self._else()
            else:
                raise SyntacticException('Faltando \'Then\' esperado', self._current_value['line']) 

        else:
            raise SyntacticException('Comando vazio', self._current_value['line']) 

    def _else(self):
        if self._current_value['token'] == 'else':
            self._next_value()
            self._statement()
        else:
            return None

    def _variable(self):
        if self._current_value['class'] != "Identificador":
            raise SyntacticException('Identificador esperado', self._current_value['line'])

    def _activation_procedure(self):
        if self._current_value['class'] == "Identificador":
            if self._next_value()['token'] == '(':
                self._list_expression1()
                
                if self._current_value['token'] != ")":
                    raise SyntacticException('Procedimento faltando fechamento \')\'', self._current_value['line'])
        else:
            #TODO - Ver com o draytim se isso n da melda
            #Erro de que entrou no activation procedure e não tinha um identificador
            raise SyntacticException('Procedimento Vazio', self._current_value['line'])

    def _list_expression1(self):
        self._expression()

        self._next_value()
        self._list_expression2()

    def _list_expression2(self):
        if self._current_value['token'] == ',':
            self._next_value()
            self._expression()

            self._next_value()
            self._list_expression2()
        else:
            return None

    def _expression(self):
        self._simple_expression1()

        if self._current_value['class'] == "Relacional":

            self._next_value()
            self._expression()
        else:
            return None

    def _simple_expression1(self):
        #sinal já no if
        if self._current_value['token'] in ['+', '-']:
            self._next_value()
            self._term1()
        else:
            self._term1()

        self._next_value()
        self._simple_expression2()

    def _simple_expression2(self):
        #Op aditiva já no if
        if self._current_value['class'] == "Aditivo":
            self._next_value()
            self._term1()

            self._next_value()
            self._simple_expression2()
        else:
            #Vamos retornar a ultima posição, pois não há uma continuação
            self._previous_value()
            return None

    def _term1(self):
        self._factor()

        self._next_value()
        self._term2()

    def _term2(self):
        #op_multiplicativo
        if self._current_value['class'] == 'Multiplicativo':
            self._next_value()
            self._factor()

            self._next_value()
            self._term2()
        else:
            #TODO - Não sei se precisa
            #Vamos retornar a ultima posição, pois não há uma continuação
            self._previous_value()
            return None

    def _factor(self):
        if self._current_value['class'] == "Número inteiro":
            return None
        
        elif self._current_value['class'] == "Número real":
            return None
        
        elif self._current_value['token'] in ['true', 'false']:
            return None

        elif self._current_value['class'] == "identificador":
            if self._next_value()['token'] == '(':
                self._next_value()
                self._list_expression1()

                if self._next_value()['token'] != ')':
                    raise SyntacticException('Fator faltando fechamento \')\'', self._current_value['line'])

            else:
                return None
        elif self._current_value['token'] == '(':
            self._next_value()
            self._expression()

            if self._next_value()['token'] != ')':
                raise SyntacticException('Fator faltando fechamento \')\'', self._current_value['line'])

        elif self._current_value['token'] == 'not':
            self._next_value()
            self._factor()

        else:
            raise SyntacticException('Fator vazio', self._current_value['line'])

    def program(self):
        for value in self._lexical_table:
            print(value)
        try:
            if self._lexical_table:
                if self._next_value()['token'] == 'program':
                    if self._next_value()['class'] == 'Identificador':
                        if self._next_value()['token'] == ';':
                            self._next_value()
                            self._variables_declaration()
                            
                            self._next_value()
                            self._list_procedures_declaration1()
                            
                            # print('\n', self._current_value)
                            # print(self._lexical_table[0])
                            self._next_value()
                            self._compound_statement()

                            if self._next_value()['token'] != '.':
                                raise SyntacticException('. final faltando', self._current_value['line'])
                        else:
                            raise SyntacticException('; faltando', self._current_value['line'])
                    else:
                        raise SyntacticException('identificador esperado após program', self._current_value['line'])  
                else:
                    print(self._current_value)
                    raise SyntacticException('faltando program no começo', self._current_value['line'])
        
        except SyntacticException as exception:
            print(exception)
                    

SyntacticAnalyzer('../data/input.txt').program()