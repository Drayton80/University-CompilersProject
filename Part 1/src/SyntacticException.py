class SyntacticException(Exception):    
    def __init__(self, message, line):
        self._message = message
        self._line = line

    def __str__(self):
        return "Ocorreu o ERRO " + self._message + " na Linha " + str(self._line)