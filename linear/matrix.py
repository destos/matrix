from .exceptions import BadDimensions, InconsistentRows, InvalidMatrix


class Matrix(object):
    """
    eg.
    A Matrix object can be initalized two different ways.
    Call it with multiple arguments containing your matrix rows expressed as lists:
        Matrix([0,0],[0,1])
    Call it with a two length tuple size kwarg:
        Matrix(size(1,4))
    When initalizing with kwargs, you can also pass a type.
        identity: creates an identity matrix.
        zero: (default) an empty matrix
    """
    values = []
    # m rows
    # n columns
    mn = (0, 0)

    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            length = len(args[0])
            self.mn = (len(args), length)
            self.values = list(args)
            self.validate_values()
        else:
            size = kwargs.pop('size', (1, 1))
            self.validate_size(mn=size)
            self.mn = size
            type = kwargs.pop('type', 'zero')
            if type == 'identity':
                self.values = [[1 if i == j else 0 for i in range(self.mn[1])] for j in range(self.mn[0])]
            elif type == 'zero':
                self.values = [[0 for i in range(self.mn[1])] for j in range(self.mn[0])]

    @property
    def size(self):
        return self.mn

    def validate_size(self, **kwargs):
        mn = kwargs.get('mn', self.mn)
        if not isinstance(mn, tuple) or len(mn) != 2 \
                or not isinstance(mn[0], int) or not isinstance(mn[1], int):
            raise BadDimensions('{} mn size must be tuple of two integers'.format(self))
        for d in mn:
            if d == 0:
                raise BadDimensions('{} mn has a zero dimension'.format(self))
        return True

    def validate_values(self, **kwargs):
        values = kwargs.get('values', self.values)
        good_length = None
        for row in values:
            if not isinstance(row, list):
                raise TypeError('matrix row wasn\'t a list')
            row_length = len(row)
            if good_length and row_length != good_length:
                raise InconsistentRows('matrix row lengths inconsistent')
            else:
                good_length = row_length
        return True

    @property
    def valid(self):
        return self.validate_size() and self.validate_values()

    def check_valid_operation(self, matrix, op='multi'):
        if op == 'multi':
            pass
        elif op == 'add/sub':
            pass
        elif op == 'invert':
            pass
        return True

    def valid_matrix(self, matrix):
        if not isinstance(matrix, self.__class__) or not matrix.valid:
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
        self.valid_matrix(matrix)
        return self + (-matrix)

    def __eq__(self, matrix):
        self.valid_matrix(matrix)
        return self.values == matrix.values

    def __getitem__(self, index):
        """
        Look up a particular row and column in the matrix
        matrix[1][3]
        """
        return self.values[index]

    def transpose(self):
        (m, n) = self.mn
        new_mtx = Matrix(size=(n, m))
        for xm in range(0, m):
            for xn in range(0, n):
                new_mtx[xn][xm] = self[xm][xn]
        return new_mtx
