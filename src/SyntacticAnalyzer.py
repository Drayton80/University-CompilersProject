import re
import os
import sys

sys.path.append(os.path.abspath(os.path.join('..')))

from src.LexicalAnalyzer import LexicalAnalyzer
from src.SyntacticException import SyntacticException
from src.TypeMismatchException import TypeMismatchException
from src.SymbolTable import SymbolTable, IdentifierInformation
from src.TypeControl import TypeControl

class SyntacticAnalyzer:
    def __init__(self, code_path: str):
        self._lexical_table = LexicalAnalyzer(code_path).create_table()
        for element in self._lexical_table:
            print(element)
        self._current_value = None
        self._old_value = None
        self._symbol_table = SymbolTable()
        self._type_control = TypeControl()
    
    def _print_current_and_neighbors(self):
        print('')
        print(self._old_value)
        print(self._current_value)
        print(self._lexical_table[0])
    
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
            self._old_value = None
        
            return self._current_value

    def _variables_declaration(self):
        if self._next_value()['token'] == 'var':
            self._list_variable_declaration1()
        else:
            self._previous_value()
            return None

    def _list_variable_declaration1(self):
        identifiers_tokens = self._list_identifiers1()
        
        if self._next_value()['token'] == ':':
            self._type(identifiers_tokens)
            
            if self._next_value()['token'] == ';':   
                self._list_variable_declaration2()
            else:
                raise SyntacticException('; faltando', self._current_value['line'])
        else:
            raise SyntacticException('separador : faltando', self._current_value['line'])

    def _list_variable_declaration2(self):
        if self._next_value()['class'] == 'Identificador':
            identifiers_tokens = self._list_identifiers1(identifier_already_checked=True)
            
            if self._next_value()['token'] == ':':
                self._type(identifiers_tokens)
                
                if self._next_value()['token'] == ';':
                    self._list_variable_declaration2()
                else:
                    raise SyntacticException('; faltando', self._current_value['line'])
            else:
                raise SyntacticException('separador : faltando', self._current_value['line'])
        else:
            self._previous_value()
            return None

    def _list_identifiers1(self, identifier_already_checked=False):
        if identifier_already_checked or self._next_value()['class'] == 'Identificador':
            self._symbol_table.identifier_declaration_token(self._current_value['token'])
            return self._list_identifiers2(list_identifiers=[self._current_value['token']])
        else:
            raise SyntacticException('identificador de variável faltando', self._current_value['line'])

    def _list_identifiers2(self, list_identifiers=[]):
        if self._next_value()['token'] == ',':
            if self._next_value()['class'] == 'Identificador':
                self._symbol_table.identifier_declaration_token(self._current_value['token'])
                return self._list_identifiers2(list_identifiers=list_identifiers + [self._current_value['token']])
            else:
                raise SyntacticException('identificador de variável faltando', self._current_value['line'])
        else:
            self._previous_value()
            return list_identifiers

    def _type(self, identifiers_tokens=None, ignore_end_block_symbol=False):
        if self._next_value()['token'] in ['integer', 'real', 'boolean', 'char', 'string']:
            self._symbol_table.identifier_declaration_type(identifiers_tokens, self._current_value['token'], ignore_end_block_symbol)
            return None
        else:
            raise SyntacticException('tipo da variável não especificado', self._current_value['line'])

    def _list_procedures_declaration1(self):
        if self._next_value()['token'] == 'procedure':
            self._procedure_declaration()

            if self._next_value()['token'] == ';':
                self._list_procedures_declaration2()
            else:
                raise SyntacticException('; faltando', self._current_value['line'])
        else:
            self._previous_value()
            return None

    def _list_procedures_declaration2(self):
        if self._next_value()['token'] == 'procedure':
            self._procedure_declaration()

            if self._next_value()['token'] == ';':
                self._list_procedures_declaration2()
            else:
                raise SyntacticException('; faltando', self._current_value['line'])
        else:
            self._previous_value()
            return None

    def _list_function_declaration1(self):
        if self._next_value()['token'] == 'function':
            self._function_declaration()

            if self._next_value()['token'] == ';':
                self._list_function_declaration2()
            else:
                raise SyntacticException('; faltando', self._current_value['line'])
        else:
            self._previous_value()
            return None

    def _list_function_declaration2(self):
        if self._next_value()['token'] == 'function':
            self._function_declaration()

            if self._next_value()['token'] == ';':
                self._list_function_declaration2()
            else:
                raise SyntacticException('; faltando', self._current_value['line'])
        else:
            self._previous_value()
            return None
    
    def _function_declaration(self):
        if self._next_value()['class'] == "Identificador":
            identifier_token = self._current_value['token']
            self._symbol_table.identifier_declaration_token(identifier_token)
            
            self._argument()

            if self._next_value()['token'] == ':':
                self._type(identifier_token, ignore_end_block_symbol=True)
            
                if self._next_value()['token'] == ';':
                    self._variables_declaration()
                    self._list_function_declaration1()
                    self._compound_statement()
                    self._symbol_table.block_exit()
                else:
                    raise SyntacticException('; faltando', self._current_value['line'])
            
            else:
                raise SyntacticException('faltando tipo de retorno', self._current_value['line'])

        else:
            self._previous_value()
            return None

    def _procedure_declaration(self):
        if self._next_value()['class'] == "Identificador":
            self._symbol_table.identifier_declaration_token(self._current_value['token'])
            self._symbol_table.identifier_declaration_type(self._current_value['token'], 'procedure')
            self._argument()
            
            if self._next_value()['token'] == ';':
                self._variables_declaration()
                self._list_procedures_declaration1()
                self._compound_statement()
                self._symbol_table.block_exit()
            else:
                raise SyntacticException('; faltando', self._current_value['line'])

        else:
            self._previous_value()
            return None

    def _argument(self):
        self._symbol_table.block_entrance()

        if self._next_value()['token'] == '(':
            self._list_parameters1()
        
            if self._next_value()['token'] != ')':
                raise SyntacticException('Argumento sem fechamento \')\'', self._current_value['line'])
        else:
            self._previous_value()
            return None

    def _list_parameters1(self):
        identifiers_tokens = self._list_identifiers1()
        
        if self._next_value()['token'] == ":":
            self._type(identifiers_tokens)
            self._list_parameters2()

        else:
            raise SyntacticException('Faltando separador \':\'', self._current_value['line'])

    def _list_parameters2(self):
        if self._next_value()['token'] == ";":
            identifiers_tokens = self._list_identifiers1()

            if self._next_value()['token'] == ":":
                self._type(identifiers_tokens)
                self._list_parameters2()

            else:
               raise SyntacticException('Faltando separador \':\'', self._current_value['line']) 
        else:
            self._previous_value()
            return None

    def _compound_statement(self, begin_already_checked=False):
        if begin_already_checked or self._next_value()['token'] == 'begin':
            # More legible representation for Optional Statements:
            if self._next_value()['token'] == 'end':
                return None
            else:
                self._previous_value()
                self._list_statement1()

                if self._next_value()['token'] == 'end':
                    return None
                else:
                    raise SyntacticException('Comando composto não fechado com end', self._current_value['line'])
            
        else:
            raise SyntacticException('Comando composto não iniciado com begin', self._current_value['line'])      

    def _optional_statement(self):
        if self._next_value()['token'] != 'end':
            self._list_statement1()
        else:
            return None

    def _list_statement1(self):
        self._statement()
        self._list_statement2()

    def _list_statement2(self):
        if self._next_value()['token'] == ';':
            if self._next_value()['token'] == 'end':
                self._previous_value()
                return None
            else:
                self._previous_value()
                self._statement()
                self._list_statement2()

        else:
            raise SyntacticException('Faltando fechamento de comandos', self._current_value['line'])   

    def _statement(self):
        self._next_value()
        
        if self._current_value['class'] == 'Identificador':
            identifierAux = self._symbol_table.identifier_usage(self._current_value['token'])         
            self._type_control.value_usage(identifierAux._token, identifierAux._type)
            if self._next_value()['token'] == ':=':

                self._expression()
                self._type_control.assignment_expression()
                    
            else:
                self._previous_value()
                self._activation_procedure(identifier_already_checked=True)
        
        elif self._current_value['token'] == 'begin':
            self._compound_statement(begin_already_checked=True)
        
        elif self._current_value['token'] == 'while':
            self._expression()

            if self._next_value()['token'] == 'do':
                self._statement()
            else:
                raise SyntacticException('Faltando \'do\' após \'while\'', self._current_value['line']) 

        elif self._current_value['token'] == 'if':
            self._expression()
            
            if self._next_value()['token'] == 'then':
                self._statement()
                self._else()
            else:
                raise SyntacticException('Faltando \'then\' esperado', self._current_value['line']) 

        else:
            raise SyntacticException('Comando vazio', self._current_value['line']) 

    def _else(self):
        if self._next_value()['token'] == 'else':
            self._statement()
        else:
            self._previous_value()
            return None

    def _variable(self):
        if self._next_value()['class'] != "Identificador":
            raise SyntacticException('Identificador esperado', self._current_value['line'])

    def _activation_procedure(self, identifier_already_checked=False):
        if identifier_already_checked or self._next_value()['class'] == "Identificador":
            self._symbol_table.identifier_usage(self._current_value['token'])     

            if self._next_value()['token'] == '(':
                self._list_expression1()
                
                if self._next_value()['token'] != ")":
                    raise SyntacticException('Procedimento faltando fechamento \')\'', self._current_value['line'])
            else:
                self._previous_value()
                return None
        else:
            raise SyntacticException('Procedimento Vazio', self._current_value['line'])

    def _list_expression1(self):
        self._expression()
        self._list_expression2()

    def _list_expression2(self):
        if self._next_value()['token'] == ',':
            self._expression()
            self._list_expression2()
        else:
            self._previous_value()
            return None

    def _expression(self):
        self._simple_expression1()

        if self._next_value()['class'] == "Relacional":
            # Relacional EA1
            print("Chegou aqui")
            print(self._current_value)
            self._type_control.relacional_expression()
            self._expression()

            print("Chegou aqui2")
            print(self._current_value)
            # Relacional EA2
            self._type_control.relacional_expression()
        else:
            self._previous_value()
            return None

    def _simple_expression1(self):
        #sinal já no if
        if self._next_value()['token'] in ['+', '-']:
            self._term1()
        else:
            self._previous_value()
            self._term1()

        self._simple_expression2()

    def _simple_expression2(self):
        #Op aditiva já no if
        if self._next_value()['class'] == "Aditivo":
            self._term1()
            self._type_control.arithmetic_expression()
            self._simple_expression2()

        else:
            #Vamos retornar a ultima posição, pois não há uma continuação
            self._previous_value()
            return None

    def _term1(self):
        self._factor()
        self._term2()

    def _term2(self):
        #op_multiplicativo
        if self._next_value()['class'] == 'Multiplicativo':
            self._factor()
            self._type_control.arithmetic_expression()
            self._term2()

        else:
            #TODO - Não sei se precisa
            #Vamos retornar a ultima posição, pois não há uma continuação
            self._previous_value()
            return None

    def _factor(self):
        self._next_value()
        if self._current_value['class'] == "Número inteiro":
            self._type_control.value_usage(self._current_value['token'], 'integer')
            return None

        elif self._current_value['class'] == "Número real":
            self._type_control.value_usage(self._current_value['token'], 'real')
            return None

        elif self._current_value['token'] in ['true', 'false']:
            self._type_control.value_usage(self._current_value['token'], 'boolean')
            return None

        elif self._current_value['class'] == "Identificador": 
            identifierAux = self._symbol_table.identifier_usage(self._current_value['token'])
            self._type_control.value_usage(identifierAux._token, identifierAux._type)

            if self._next_value()['token'] == '(':
                self._list_expression1()

                if self._next_value()['token'] != ')':
                    raise SyntacticException('Fator faltando fechamento \')\'', self._current_value['line'])
            else:
                self._previous_value()
                return None

        elif self._current_value['token'] == '(':
            self._expression()

            if self._next_value()['token'] != ')':
                raise SyntacticException('Fator faltando fechamento \')\'', self._current_value['line'])

        elif self._current_value['token'] == 'not':
            self._factor()

        else:
            raise SyntacticException('Fator vazio', self._current_value['line'])

    def program(self):
        # for value in self._lexical_table:
        #     print(value)
        try:
            if self._lexical_table:
                if self._next_value()['token'] == 'program':
                    if self._next_value()['class'] == 'Identificador':
                        self._symbol_table.block_entrance()

                        if self._next_value()['token'] == ';':
                            self._variables_declaration()
                            self._list_procedures_declaration1()
                            self._list_function_declaration1()
                            self._compound_statement()
                            self._symbol_table.block_exit()

                            if self._next_value()['token'] != '.':
                                raise SyntacticException('. final faltando', self._current_value['line'])
                        else:
                            raise SyntacticException('; faltando', self._current_value['line'])
                    else:
                        raise SyntacticException('identificador esperado após program', self._current_value['line'])  
                else:
                    raise SyntacticException('faltando program no começo', self._current_value['line'])
        
        except SyntacticException as exception:
            print(exception)
        except TypeMismatchException as ex:
            print(ex)
                    

SyntacticAnalyzer('../data/input2.txt').program()