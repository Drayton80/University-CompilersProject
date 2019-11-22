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
    
    def _next_value(self, place=''):
        if self._lexical_table != []:
            self._old_value = self._current_value
            self._current_value = self._lexical_table.pop(0)
        else:
            self._current_value = {'token': '', 'class': '', 'line': ''}

        if place != '':
            print('\ncurrent:\n', self._current_value, '\n', place, '\n', sep = '')

        return self._current_value

    def _previous_value(self, place=''):
        if self._old_value:
            if self._current_value['token'] != '':
                self._lexical_table.insert(0, self._current_value)
                
            self._current_value = self._old_value

        if place != '':
            print('\nPrevius:\n', self._old_value, '\n', place, '\n', sep = '')
        
        return self._old_value


    def _variables_declaration(self):
        if self._current_value['token'] == 'var':
            self._next_value(place='variables_declaration (dentro do if do var)')
            self._list_variable_declaration1()
        else:
            self._previous_value(place='variables_declaration (dentro do else do var)')
            return None

    def _list_variable_declaration1(self):
        self._list_identifiers1()
        
        if self._next_value(place='list_variable_declaration1 (if do :)')['token'] == ':':
            self._next_value(place='list_variable_declaration1 (dento do if do :)')
            self._type()
            
            if self._next_value(place='list_variable_declaration1 (if do ;)')['token'] == ';':   
                self._next_value(place='list_variable_declaration1 (dento do if do ;)')
                self._list_variable_declaration2()
            else:
                raise SyntacticException('; faltando', self._current_value['line'])
        else:
            raise SyntacticException('separador : faltando', self._current_value['line'])

    def _list_variable_declaration2(self):
        if self._current_value['class'] == 'Identificador':
            self._list_identifiers1()
            
            if self._next_value(place='list_variable_declaration2 (if do :)')['token'] == ':':
                self._next_value(place='list_variable_declaration2 (dentro do if do :)')
                self._type()
                
                if self._next_value(place='list_variable_declaration2 (if do ;)')['token'] == ';':
                    self._next_value(place='list_variable_declaration2 (dentro do if do ;)')
                    self._list_variable_declaration2()
                else:
                    raise SyntacticException('; faltando', self._current_value['line'])
            else:
                raise SyntacticException('separador : faltando', self._current_value['line'])
        else:
            self._previous_value(place='list_variable_declaration2 (dentro do else do if do :)')
            return None

    def _list_identifiers1(self):
        if self._current_value['class'] == 'Identificador':
            self._next_value(place='list_identifiers1 (antes da chamada do list_identifiers2)')
            self._list_identifiers2()
        else:
            raise SyntacticException('identificador de variável faltando', self._current_value['line'])

    def _list_identifiers2(self):
        if self._current_value['token'] == ',':
            if self._next_value(place='list_identifiers2 (if do Identificador)')['class'] == 'Identificador':
                self._next_value(place='list_identifiers2 (antes da chamada do list_identifiers2)')
                self._list_identifiers2()
            else:
                raise SyntacticException('identificador de variável faltando', self._current_value['line'])
        else:
            self._previous_value(place='list_identifiers2 (dentro do else do if da ,)')
            return None

    def _type(self):
        if self._current_value['token'] in ['integer', 'real', 'boolean', 'char', 'string']:
            return None
        else:
            raise SyntacticException('tipo da variável não especificado', self._current_value['line'])

    def _list_procedures_declaration1(self):
        if self._current_value['token'] == 'procedure':
            self._procedure_declaration()

            if self._next_value(place='list_procedures_declaration1 (if do ;)')['token'] == ';':
                self._list_procedures_declaration2()
            else:
                raise SyntacticException('; faltando', self._current_value['line'])
        else:
            self._previous_value(place='list_procedures_declaration1 (dentro do else do if do procedure)')
            return None

    def _list_procedures_declaration2(self):
        if self._current_value['token'] == 'procedure':
            self._procedure_declaration()

            if self._next_value(place='list_procedures_declaration2 (if do ;)')['token'] == ';':
                self._list_procedures_declaration2()
            else:
                raise SyntacticException('; faltando', self._current_value['line'])
        else:
            self._previous_value(place='list_procedures_declaration2 (dentro do else do if do procedure)')
            return None
    
    def _procedure_declaration(self):
        if self._current_value['token'] == 'procedure':
            if self._next_value(place='procedure_declaration (if do Identificador)')['class'] == "Identificador":
                self._next_value(place='procedure_declaration (antes da chamada do argument)')
                self._argument()
                
                if self._next_value(place='procedure_declaration (if do ;)')['token'] == ';':
                    self._next_value(place='procedure_declaration (antes da chamada do variables_declaration)')
                    self._variables_declaration()
                    
                    self._next_value(place='procedure_declaration (antes da chamada do list_procedures_declaration1)')
                    self._list_procedures_declaration1()
                    
                    self._next_value(place='procedure_declaration (antes da chamada do compound_statement)')
                    self._compound_statement()
                else:
                    raise SyntacticException('; faltando', self._current_value['line'])
            else:
                raise SyntacticException('procedure faltando', self._current_value['line'])

    def _argument(self):
        if self._current_value['token'] == '(':
            self._next_value(place='argument (antes da chamada do list_parameters1)')
            self._list_parameters1()
        
            if self._next_value(place='argument (if do ) )')['token'] != ')':
                raise SyntacticException('faltando fechamento fechamento \')\'', self._current_value['line'])
        else:
            self._previous_value(place='argument (dentro do else do if do ( )')
            return None

    def _list_parameters1(self):
        self._list_identifiers1()
        
        if self._next_value(place='list_parameters1 (if do :)')['token'] == ":":
            self._next_value(place='list_parameters1 (antes da chamada do type)')
            self._type()

            self._next_value(place='list_parameters1 (antes da chamada do list_parameters2)')
            self._list_parameters2()
        else:
            raise SyntacticException('Faltando separador \':\'', self._current_value['line'])

    def _list_parameters2(self):
        if self._current_value['token'] == ";":
            self._next_value(place='list_parameters2 (antes da chamada do list_identifiers1)')
            self._list_identifiers1()

            if self._next_value(place='list_parameters2 (if do :)')['token'] == ":":
                self._next_value(place='list_parameters2 (antes da chamada do type)')
                self._type()

                self._next_value(place='list_parameters2 (antes da chamada do list_parameters2)')
                self._list_parameters2()
            else:
               raise SyntacticException('Faltando separador \':\'', self._current_value['line']) 
        else:
            self._previous_value(place='list_parameters2 (dentro do else do if do ;)')
            return None

    def _compound_statement(self):
        if self._current_value['token'] == 'begin':
            # More legible representation for Optional Statements:
            if self._next_value(place='compound_statement (if do end)')['token'] == 'end':
                return None
            else:
                self._list_statement1()
                
                if self._next_value(place='compound_statement (2º if do end)')['token'] != 'end':
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

        self._next_value(place='list_statement1 (antes da chamada do list_statement2)')
        self._list_statement2()

    def _list_statement2(self):
        if self._current_value['token'] == ';':
            if self._next_value(place='list_statement2 (if do end)')['token'] == 'end':
                self._previous_value(place='list_statement2 (dentro do if do end)')
                return None

            self._statement()
            
            self._next_value(place='list_statement2 (antes da chamada do list_statement2)')
            self._list_statement2()
        
        elif self._current_value['token'] == 'end':
            self._next_value(place='list_statement2 (dentro do if do end)')
            self._statement()

        else:
            raise SyntacticException('Faltando fechamento de comandos', self._current_value['line'])   

    def _statement(self):
        if self._current_value['class'] == 'Identificador':         
            if self._next_value(place='statement (if do :=)')['token'] == ':=':
                self._next_value(place='statement (dentro do if do Identificador antes da chamada do expression)')
                # self._variable() #Perguntar pro draytim
                self._expression()
            else:
                self._previous_value(place='statement (dentro do else do if do :=)')
                self._activation_procedure()
        
        elif self._current_value['token'] == 'begin':
            self._compound_statement()
        
        elif self._current_value['token'] == 'while':
            self._next_value(place='statement (dentro do if do while antes do expression)')
            self._expression()

            if self._next_value(place='statement (dentro do if do while if do do)')['token'] == 'do':
                self._next_value(place='statement (dentro do if do while do antes do statement)')
                self._statement()
            else:
                raise SyntacticException('Faltando \'do\' após \'while\'', self._current_value['line']) 

        elif self._current_value['token'] == 'if':
            self._next_value(place='statement (dentro do if do if)')
            self._expression()
            if self._next_value(place='statement (dentro do if do if no if do then)')['token'] == 'then':
                self._next_value(place='statement (dentro do if do then antes do statement)')
                self._statement()

                self._next_value(place='statement (dentro do if do then antes do else)')
                self._else()
            else:
                raise SyntacticException('Faltando \'then\' esperado', self._current_value['line']) 

        else:
            raise SyntacticException('Comando vazio', self._current_value['line']) 

    def _else(self):
        if self._current_value['token'] == 'else':
            self._next_value(place='else (dentro do if do else antes do statement)')
            self._statement()
        else:
            self._previous_value(place='else (dentro do else if do else)')
            return None

    def _variable(self):
        if self._current_value['class'] != "Identificador":
            raise SyntacticException('Identificador esperado', self._current_value['line'])

    def _activation_procedure(self):
        if self._current_value['class'] == "Identificador":
            if self._next_value(place='activation_procedure (if do ( )')['token'] == '(':
                self._list_expression1()
                
                if self._current_value['token'] != ")":
                    raise SyntacticException('Procedimento faltando fechamento \')\'', self._current_value['line'])
            else:
                self._previous_value(place='activation_procedure (dentro do else do if do ( )')
                return None
        else:
            #TODO - Ver com o draytim se isso n da melda
            #Erro de que entrou no activation procedure e não tinha um identificador
            raise SyntacticException('Procedimento Vazio', self._current_value['line'])

    def _list_expression1(self):
        self._expression()
        
        self._next_value(place='list_expression1 (antes da chamada do list_expression2)')
        self._list_expression2()

    def _list_expression2(self):
        if self._current_value['token'] == ',':
            self._next_value(place='list_expression2 (antes da chamada do expression)')
            self._expression()
            
            self._next_value(place='list_expression2 (antes da chamada do list_expression2)')
            self._list_expression2()
        else:
            return None

    def _expression(self):
        self._simple_expression1()
        
        if self._next_value(place='expression (if do Relacional)')['class'] == "Relacional":
            self._next_value(place='expression (antes da chamada do expression)')
            self._expression()
        else:
            self._previous_value(place='expression (dentro do else do if do Relacional)')
            return None

    def _simple_expression1(self):
        #sinal já no if
        if self._current_value['token'] in ['+', '-']:
            self._next_value(place='simple_expression1 (dentro do if do + e - antes da chamada do term1)')
            self._term1()
        else:
            self._term1()

        
        self._next_value(place='simple_expression1 (antes da chamada do simple_expression2)')
        self._simple_expression2()

    def _simple_expression2(self):
        #Op aditiva já no if
        if self._current_value['class'] == "Aditivo":
            self._next_value(place='simple_expression2 (antes da chamada do term1)')
            self._term1()

            self._next_value(place='simple_expression2 (antes da chamada do simple_expression2)')
            self._simple_expression2()
        else:
            #Vamos retornar a ultima posição, pois não há uma continuação
            self._previous_value(place='simple_expression2 (expressão finalizada)')
            return None

    def _term1(self):
        self._factor()
        self._next_value(place='term1 (antes da chamada do term2)')
        self._term2()

    def _term2(self):
        #op_multiplicativo
        if self._current_value['class'] == 'Multiplicativo':
            self._next_value(place='term2 (antes da chamada do factor)')
            self._factor()

            self._next_value(place='term2 (antes da chamada do term2)')
            self._term2()
        else:
            #TODO - Não sei se precisa
            #Vamos retornar a ultima posição, pois não há uma continuação
            return None

    def _factor(self):

        if self._current_value['class'] == "Número inteiro":
            return None
        
        elif self._current_value['class'] == "Número real":
            return None
        
        elif self._current_value['token'] in ['true', 'false']:
            return None

        elif self._current_value['class'] == "Identificador":
            if self._next_value(place='factor (dentro do if do Identificador if do ( )')['token'] == '(':
                self._next_value(place='factor (dentro do if do Identificador dentro if do ( antes list_expression1)')
                self._list_expression1()

                if self._next_value(place='factor (dentro do if do Identificador dentro if do ( if do ) )')['token'] != ')':
                    raise SyntacticException('Fator faltando fechamento \')\'', self._current_value['line'])
            else:
                self._previous_value(place='factor (dentro do if do Identificador dentro do else if do ( )')
                return None
        
        elif self._current_value['token'] == '(':
            self._next_value(place='factor (dentro do if do ( )')
            self._expression()

            if self._next_value(place='factor (dentro do if do ( if do ) )')['token'] != ')':
                raise SyntacticException('Fator faltando fechamento \')\'', self._current_value['line'])

        elif self._current_value['token'] == 'not':
            self._next_value(place='factor (dentro do if do not)')
            self._factor()

        else:
            raise SyntacticException('Fator vazio', self._current_value['line'])

    def program(self):
        # for value in self._lexical_table:
        #     print(value)
        try:
            if self._lexical_table:
                if self._next_value(place='program (if do program)')['token'] == 'program':
                    if self._next_value(place='program (if do Identificador)')['class'] == 'Identificador':
                        if self._next_value(place='program (if do ;)')['token'] == ';':
                            self._next_value(place='program (antes da chamada do variables_declaration)')
                            self._variables_declaration()
                            
                            self._next_value(place='program (antes da chamada do list_procedures_declaration1)')
                            self._list_procedures_declaration1()
                            
                            # print('\n', self._current_value)
                            # print(self._lexical_table[0])
                            self._next_value(place='program (antes da chamada do compound_statement)')
                            self._compound_statement()

                            if self._next_value(place='program (if do .)')['token'] != '.':
                                raise SyntacticException('. final faltando', self._current_value['line'])
                        else:
                            raise SyntacticException('; faltando', self._current_value['line'])
                    else:
                        raise SyntacticException('identificador esperado após program', self._current_value['line'])  
                else:
                    raise SyntacticException('faltando program no começo', self._current_value['line'])
        
        except SyntacticException as exception:
            print(exception)
                    

SyntacticAnalyzer('../data/input.txt').program()