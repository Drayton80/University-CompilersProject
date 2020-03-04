class UsingNotDeclaredException(Exception):        
    def __init__(self, identifier_token):
        self._identifier_token = identifier_token
    
    def __str__(self):
        return "O identificador " + str(self._identifier_token) + " está sendo usado antes de ser declarado"