class CommentException(Exception):        
    def __str__(self):
        return "Comentário aberto e não fechado"