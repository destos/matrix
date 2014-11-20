#python -m unittest -v matrix.tests.MatrixTest

from unittest import TestCase
import mox

from linear.matrix import Matrix
from linear.exceptions import InconsistentRows, BadDimensions

class MatrixTest(TestCase):
    def setUp(self):
        # self.mtx_obj = Matrix()
        self.mox = mox.Mox()

    def tearDown(self):
        self.mox.UnsetStubs()

    def test_constructing_with_good_args(self):
        Matrix([1,4], [4,8])

    def test_constructing_with_bad_args(self):
        with self.assertRaises(InconsistentRows):
            Matrix([3,4,6], [3,5])

    def test_size_from_args(self):
        mtx = Matrix([1,4], [4,8], [4,9])
        self.assertEqual(mtx.size, (3, 2))

    def test_size_from_kwargs(self):
        mtx = Matrix(size=(4, 5))
        self.assertEqual(mtx.size, (4, 5))

    def test_size_not_tuple(self):
        with self.assertRaises(TypeError):
            Matrix(size=False)
        with self.assertRaises(TypeError):
            Matrix(size=(1,2,3))
        with self.assertRaises(TypeError):
            Matrix(size='tssssdf')
        with self.assertRaises(TypeError):
            Matrix(size=('dl', 'd'))
        with self.assertRaises(TypeError):
            Matrix(size=('dl', 1))

    def test_identity_matrix_init(self):
        mtx = Matrix(size=(3,3), type='identity')
        self.assertEqual(mtx.values, [[1,0,0], [0,1,0], [0,0,1]])

    def test_zero_matrix_init(self):
        mtx = Matrix(size=(3,3), type='zero')
        self.assertEqual(mtx.values, [[0,0,0], [0,0,0], [0,0,0]])

    def test_zero_matrix_init(self):
        mtx = Matrix(size=(3,2), type='zero')
        self.assertEqual(mtx.values, [[0,0], [0,0], [0,0]])

    def test_times_valid_matrix(self):
        self.mox.StubOutWithMock(Matrix, 'valid_matrix')
        # self.mox.StubOutWithMock(Matrix, 'check_valid_operation')
        mtx1 = Matrix([1,4], [4,8])
        mtx2 = Matrix([2,1], [4,6])

        mtx1.valid_matrix(mtx2).AndReturn(True)
        # mtx1.check_valid_operation(mtx2, op='multi').AndReturn(True)

        self.mox.ReplayAll()
        res_mtx = mtx1.times(mtx2)
        self.mox.VerifyAll()

        self.assertNotIn(res_mtx, (mtx1, mtx2))
        self.assertEqual(res_mtx.mn, (2, 2))
        self.assertEqual(res_mtx.values, [[18, 25], [40, 52]])

    def test_invalid_matrix_dimensions(self):
        self.mox.StubOutWithMock(Matrix, 'valid_matrix')
        mtx2 = Matrix([1,4], [4,8])
        mtx1 = Matrix([2,1,3], [4,6,5])

        mtx1.valid_matrix(mtx2).AndReturn(True)

        self.mox.ReplayAll()
        self.assertRaises(BadDimensions, mtx1.times, mtx2)
        self.mox.VerifyAll()
