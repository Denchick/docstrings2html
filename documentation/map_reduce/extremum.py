from . import piece


class Extremum:
    def __init__(self, data, piece_obj):
        """ Удобная структура для хранения пары кусок <- его верхний элемент. 

        Args:
            data (str): верхний элемент piece_obj.
            piece_obj (piece.Piece): объект соответствующего маленького файла - куска.
        
        Raises:
            TypeError: если piece_obj не является объектом piece.Piece.
        """
        if not isinstance(piece_obj, piece.Piece) and piece_obj is not None:
            raise TypeError("piece_obj must be of instance of piece.Piece")
        self.data = data
        self.piece_obj = piece_obj
