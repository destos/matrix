from .exceptions import InconsistentRows


class Matrix(object):
    """Matrix([0,0],[0,1])"""
    values = []
    mn = (0, 0)

    def __init__(self, *args, **kwargs):
        good_length = None
        if len(args) > 1:
            for arg in args:
                if not isinstance(arg, list):
                    raise TypeError('Row wasn\'t a list')
                arg_length = len(arg)
                if good_length and arg_length != good_length:
                    raise InconsistentRows('weird length')
                else:
                    good_length = arg_length
            self.mn = (good_length, len(args))
            self.values = [arg for arg in args]
        else:
            self.mn = kwargs.pop('size')
            if not isinstance(self.mn, tuple) or len(self.mn) != 2 \
                    or not isinstance(self.mn[0], int) or not isinstance(self.mn[1], int):
                raise TypeError('size must be tuple of two integers')
            type = kwargs.pop('type', None)
            if type == 'identity':
                self.values = [[1 if i == j else 0 for i in range(self.mn[0])] for j in range(self.mn[1])]
            elif type == 'zero':
                self.values = [[0 for i in range(self.mn[0])] for j in range(self.mn[1])]

    @property
    def size(self):
        return self.mn

    def times(self, matrix):
        "Post multiply by another matrix"
        pass
