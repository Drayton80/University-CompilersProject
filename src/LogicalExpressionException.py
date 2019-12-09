class LogicalExpressionException(Exception):
    def __str__(self):
        return "Operação lógica com AND ou OR só pode acontecer a partir de dois valores booleanos lógicos"