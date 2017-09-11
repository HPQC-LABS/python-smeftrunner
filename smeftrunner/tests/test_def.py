import unittest
import numpy as np
import numpy.testing as npt
from smeftrunner import definitions
import test_beta

C = test_beta.C.copy()
for i in C:
    if i in definitions.WC_keys_2f + definitions.WC_keys_4f:
        # make Wilson coefficients involving fermions complex!
        C[i] = C[i] + 1j*C[i]

class TestSymm(unittest.TestCase):
    def test_keys(self):
        # check no parameter or WC was forgotten in the C_symm_keys lists
        self.assertEqual(
          set(definitions.C_keys),
          set([c for cs in definitions.C_symm_keys.values() for c in cs])
        )

    def test_symmetrize_symmetric(self):
        a = np.array([[1, 2, 3], [2, 4, 5], [3, 5, 6]])
        npt.assert_array_equal(definitions.symmetrize_2(a), a)
        b = np.array([[1, 2, 3], [0, 4, 5], [0, 0, 6]])
        npt.assert_array_equal(definitions.symmetrize_2(b), a)

    def test_symmetrize_hermitian(self):
        a = np.array([[1, 2j, 3j], [-2j, 4, 5j], [-3j, -5j, 6]])
        npt.assert_array_equal(definitions.symmetrize_2(a), a)
        b = np.array([[1, 2j, 3j], [0, 4, 5j], [0, 0, 6]])
        npt.assert_array_equal(definitions.symmetrize_2(b), a)

    def test_symmetrize_C(self):
        C_symm = definitions.symmetrize(C)
        # check all keys are present
        self.assertSetEqual(set(C.keys()), set(C_symm.keys()))
        for i, v in C_symm.items():
            # check trivial cases are the same
            if i in definitions.C_symm_keys[0] + definitions.C_symm_keys[1] + definitions.C_symm_keys[3]:
                if definitions.C_keys_shape[i] == 1:
                    self.assertEqual(v, C[i])
                else:
                    npt.assert_array_equal(v, C[i])
            # check symmetric
            elif i in definitions.C_symm_keys[9]:
                npt.assert_array_equal(v, v.T)
            # check hermitian
            elif i in definitions.C_symm_keys[2]:
                npt.assert_array_equal(v, v.T.conj())
            # check 2 identical FFbar
            elif i in definitions.C_symm_keys[4]:
                npt.assert_array_equal(v, v.transpose((2, 3, 0, 1)))
                npt.assert_array_equal(v, v.transpose((1, 0, 3, 2)).conj())
            # check 2 independent FFbar
            elif i in definitions.C_symm_keys[5]:
                npt.assert_array_equal(v, v.transpose((1, 0, 3, 2)).conj())
            # check special case ee
            elif i in definitions.C_symm_keys[6]:
                # npt.assert_array_equal(v, v.transpose((2, 3, 0, 1)))
                print(tuple(np.array(np.nonzero(v-v.transpose((2, 3, 0, 1)))).T))
                # npt.assert_array_equal(v, v.transpose((0, 3, 2, 1)))
                print(tuple(np.array(np.nonzero(v-v.transpose((0, 3, 2, 1)))).T))
                # npt.assert_array_equal(v, v.transpose((2, 1, 0, 3)))
                print(tuple(np.array(np.nonzero(v-v.transpose((2, 1, 0, 3)))).T))
            # check special case qque
            elif i in definitions.C_symm_keys[7]:
                npt.assert_array_equal(v, v.transpose((1, 0, 2, 3)))
            # check special case qqql
            elif i in definitions.C_symm_keys[8]:
                # see eq. (10) of arXiv:1405.0486
                # npt.assert_array_equal(v + v.transpose((1, 0, 2, 3)), v.transpose((2, 0, 1, 3)) + v.transpose((2, 1, 0, 3)))
                print(tuple(np.array(np.nonzero(v + v.transpose((1, 0, 2, 3))- (v.transpose((2, 0, 1, 3)) + v.transpose((2, 1, 0, 3))))).T))
