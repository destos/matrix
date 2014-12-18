from .exceptions import BadDimensions, InconsistentRows, InvalidMatrix


class Matrix(object):
    """
    eg.
    Matrix([0,0],[0,1])
    """
    values = []
    # m rows
    # n columns
    mn = (0, 0)

    def __init__(self, *args, **kwargs):
        good_length = None
        if len(args) > 0:
            for arg in args:
                if not isinstance(arg, list):
                    raise TypeError('Row wasn\'t a list')
                arg_length = len(arg)
                if good_length and arg_length != good_length:
                    raise InconsistentRows('weird length')
                else:
                    good_length = arg_length
            self.mn = (len(args), good_length)
            self.values = list(args)
        else:
            self.mn = kwargs.pop('size', (0, 0))
            if not isinstance(self.mn, tuple) or len(self.mn) != 2 \
                    or not isinstance(self.mn[0], int) or not isinstance(self.mn[1], int):
                raise TypeError('size must be tuple of two integers')
            type = kwargs.pop('type', 'zero')
            if type == 'identity':
                self.values = [[1 if i == j else 0 for i in range(self.mn[1])] for j in range(self.mn[0])]
            elif type == 'zero':
                self.values = [[0 for i in range(self.mn[1])] for j in range(self.mn[0])]

    @property
    def size(self):
        return self.mn

    @property
    def valid(self):
        return True

    def check_valid_operation(self, matrix, op='multi'):
        if op == 'multi':
            pass
        elif op == 'add/sub':
            pass
        elif op == 'invert':
            pass
        return True

    def valid_matrix(self, matrix):
        if not isinstance(matrix, self.__class__) and matrix.valid:
            raise InvalidMatrix("{} passed into {} ".format(matrix, self))
        return True

    def __mul__(self, matrix):
        """Post multiply by another matrix"""
        self.valid_matrix(matrix)
        # self.check_valid_operation(matrix, op='multi')

        # first rows
        m = self.mn[0]
        # first columns
        n = self.mn[1]
        if n != matrix.mn[0]:
            raise BadDimensions('inner dimensions must match')
        # second matrix columns
        p = matrix.mn[1]
        new_mtx = Matrix(size=(m, p), type='zero')

        for xm in range(0, m):
            for xp in range(0, p):
                for xn in range(0, n):
                    new_mtx[xm][xp] += self[xm][xn] * matrix[xn][xp]

        # return matrix
        return new_mtx

    def __add__(self, matrix):
        self.valid_matrix(matrix)
        if self.mn[0] != matrix.mn[0] or self.mn[1] != matrix.mn[1]:
            raise BadDimensions('dimensions must match')

        new_mtx = Matrix(size=self.mn)
        (m, n) = self.mn

        for xm in range(0, m):
            for xn in range(0, n):
                new_mtx[xm][xn] = self[xm][xn] + matrix[xm][xn]

        return new_mtx

    def __neg__(self):
        self.valid_matrix(self)

        new_mtx = Matrix(size=self.mn)
        (m, n) = self.mn

        for xm in range(0, m):
            for xn in range(0, n):
                new_mtx[xm][xn] = -self[xm][xn]

        return new_mtx

    def __sub__(self, matrix):
        return self + (-matrix)

    def __getitem__(self, index):
        """
        Look up a particular row and column in the matrix
        matrix[1][3]
        """
        return self.values[index]
