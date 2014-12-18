# python -m unittest -v matrix.tests.MatrixTest
# python -m unittest tests.MatrixTest

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
        Matrix([1, 4], [4, 8])

    def test_constructing_with_bad_args(self):
        with self.assertRaises(InconsistentRows):
            Matrix([3, 4, 6], [3, 5])

    def test_size_from_args(self):
        mtx = Matrix([1, 4], [4, 8], [4, 9])
        self.assertEqual(mtx.size, (3, 2))

    def test_size_from_kwargs(self):
        mtx = Matrix(size=(4, 5))
        self.assertEqual(mtx.size, (4, 5))

    def test_size_not_tuple(self):
        with self.assertRaises(TypeError):
            Matrix(size=False)
        with self.assertRaises(TypeError):
            Matrix(size=(1, 2, 3))
        with self.assertRaises(TypeError):
            Matrix(size='tssssdf')
        with self.assertRaises(TypeError):
            Matrix(size=('dl', 'd'))
        with self.assertRaises(TypeError):
            Matrix(size=('dl', 1))

    def test_identity_matrix_init(self):
        mtx = Matrix(size=(3, 3), type='identity')
        self.assertEqual(mtx.values, [[1, 0, 0], [0, 1, 0], [0, 0, 1]])

    def test_zero_matrix_init(self):
        mtx = Matrix(size=(3, 3), type='zero')
        self.assertEqual(mtx.values, [[0, 0, 0], [0, 0, 0], [0, 0, 0]])

    def test_zero_matrix_init_2x2(self):
        mtx = Matrix(size=(3, 2), type='zero')
        self.assertEqual(mtx.values, [[0, 0], [0, 0], [0, 0]])

    def test_times_valid_matrix(self):
        self.mox.StubOutWithMock(Matrix, 'valid_matrix')
        # self.mox.StubOutWithMock(Matrix, 'check_valid_operation')
        mtx1 = Matrix([1, 4], [4, 8])
        mtx2 = Matrix([2, 1], [4, 6])

        mtx1.valid_matrix(mtx2).AndReturn(True)
        # mtx1.check_valid_operation(mtx2, op='multi').AndReturn(True)

        self.mox.ReplayAll()
        res_mtx = mtx1 * mtx2
        self.mox.VerifyAll()

        self.assertNotIn(res_mtx, (mtx1, mtx2))
        self.assertEqual(res_mtx.mn, (2, 2))
        self.assertEqual(res_mtx.values, [[18, 25], [40, 52]])

    def test_times_invalid_matrix_dimensions(self):
        self.mox.StubOutWithMock(Matrix, 'valid_matrix')
        mtx2 = Matrix([1, 4], [4, 8])
        mtx1 = Matrix([2, 1, 3], [4, 6, 5])

        mtx1.valid_matrix(mtx2).AndReturn(True)

        self.mox.ReplayAll()
        with self.assertRaises(BadDimensions):
            mtx1 * mtx2
        self.mox.VerifyAll()

    def test_add_valid_matrix(self):
        self.mox.StubOutWithMock(Matrix, 'valid_matrix')
        mtx1 = Matrix([6, 4], [2, 4])
        mtx2 = Matrix([2, 9], [1, 7])

        mtx1.valid_matrix(mtx2).AndReturn(True)

        self.mox.ReplayAll()
        res_mtx = mtx1 + mtx2
        self.mox.VerifyAll()

        self.assertNotIn(res_mtx, (mtx1, mtx2))
        self.assertEqual(res_mtx.mn, (2, 2))
        self.assertEqual(res_mtx.values, [[8, 13], [3, 11]])

    def test_add_valid_matrix_3x2(self):
        self.mox.StubOutWithMock(Matrix, 'valid_matrix')
        mtx1 = Matrix([6, 4], [2, 4], [1, 1])
        mtx2 = Matrix([2, 9], [1, 7], [1, 1])

        mtx1.valid_matrix(mtx2).AndReturn(True)

        self.mox.ReplayAll()
        res_mtx = mtx1 + mtx2
        self.mox.VerifyAll()

        self.assertNotIn(res_mtx, (mtx1, mtx2))
        self.assertEqual(res_mtx.mn, (3, 2))
        self.assertEqual(res_mtx.values, [[8, 13], [3, 11], [2, 2]])

    def test_add_bad_dimensions(self):
        self.mox.StubOutWithMock(Matrix, 'valid_matrix')
        mtx1 = Matrix([6, 4], [2, 4], [1, 1])
        mtx2 = Matrix([2, 9, 3], [1, 7, 5], [1, 1, 5])

        mtx1.valid_matrix(mtx2).AndReturn(True)

        self.mox.ReplayAll()
        with self.assertRaises(BadDimensions):
            mtx1 + mtx2
        self.mox.VerifyAll()

    def test_negate_valid_matrix(self):
        self.mox.StubOutWithMock(Matrix, 'valid_matrix')
        mtx = Matrix([-6, 4], [0, 4])

        mtx.valid_matrix(mtx).AndReturn(True)

        self.mox.ReplayAll()
        res_mtx = -mtx
        self.mox.VerifyAll()

        self.assertNotEqual(res_mtx, mtx)
        self.assertEqual(res_mtx.mn, (2, 2))
        self.assertEqual(res_mtx.values, [[6, -4], [0, -4]])

    def test_negate_valid_matrix_3x2(self):
        self.mox.StubOutWithMock(Matrix, 'valid_matrix')
        mtx = Matrix([6, 4], [2, 4], [1, 1])

        mtx.valid_matrix(mtx).AndReturn(True)

        self.mox.ReplayAll()
        res_mtx = -mtx
        self.mox.VerifyAll()

        self.assertNotEqual(res_mtx, mtx)
        self.assertEqual(res_mtx.mn, (3, 2))
        self.assertEqual(res_mtx.values, [[-6, -4], [-2, -4], [-1, -1]])

    def test_subtract(self):
        self.mox.StubOutWithMock(Matrix, '__neg__')
        self.mox.StubOutWithMock(Matrix, '__add__')

        mtx1 = Matrix([6, 4], [2, 4], [1, 1])
        mtx2 = Matrix([2, 9], [1, 7], [1, 1])

        mtx2.__neg__().AndReturn('negated')
        mtx1.__add__('negated').AndReturn('returned')

        self.mox.ReplayAll()
        res = mtx1 - mtx2
        self.mox.VerifyAll()
        self.assertEqual(res, 'returned')
