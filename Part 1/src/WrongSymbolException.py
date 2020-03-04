class WrongSymbolException(Exception):        
    def __str__(self):
        return "Símbolo não pertencente a linguagem"