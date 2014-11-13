#python -m unittest -v matrix.tests.MatrixTest

from unittest import TestCase

from linear.matrix import Matrix
from linear.exceptions import InconsistentRows

class MatrixTest(TestCase):
    # def setUp(self):
    #     self.mtx_obj = Matrix()

    def test_constructing_with_good_args(self):
        Matrix([1,4], [4,8])

    def test_constructing_with_bad_args(self):
        with self.assertRaises(InconsistentRows):
            Matrix([3,4,6], [3,5])

    def test_size_from_args(self):
        mtx = Matrix([1,4], [4,8], [4,9])
        self.assertEqual(mtx.size, (2,3))

    def test_size_from_kwargs(self):
        mtx = Matrix(size=(4,5))
        self.assertEqual(mtx.size, (4,5))

    def test_size_not_tuple(self):
        with self.assertRaises(TypeError):
            Matrix(size=False)
        with self.assertRaises(TypeError):
            Matrix(size=(1,2,3))
        with self.assertRaises(TypeError):
            Matrix(size='tssssdf')
        with self.assertRaises(TypeError):
            Matrix(size=('dl','d'))
        with self.assertRaises(TypeError):
            Matrix(size=('dl',1))

    def test_identity_matrix_init(self):
        mtx = Matrix(size=(3,3), type='identity')
        self.assertEqual(mtx.values, [[1,0,0], [0,1,0], [0,0,1]])

    def test_zero_matrix_init(self):
        mtx = Matrix(size=(3,3), type='zero')
        self.assertEqual(mtx.values, [[0,0,0], [0,0,0], [0,0,0]])

    # def test_times_incorrect_matrix(self):
    #     pass
