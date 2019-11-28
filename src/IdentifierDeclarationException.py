class IdentifierDeclarationException(Exception):        
    def __init__(self, identifier_token):
        self._identifier_token = identifier_token
    
    def __str__(self):
        return "Já existe um identificador com o nome " + str(self._identifier_token)