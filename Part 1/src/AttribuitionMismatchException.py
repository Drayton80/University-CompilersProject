class AttribuitionMismatchException(Exception):           
    def __str__(self):
        return "Tipo atribuído ao identificador não condiz com seu tipo declarado"