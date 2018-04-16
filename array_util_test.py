import unittest

import numpy as np

import array_util


class TestFindSubarray(unittest.TestCase):

    def test_not_existing(self):
        self.assertIsNone(
            array_util.find_subarray_np(
                np.array([1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5]),
                np.array([1, 2, 3, 5])
            ),
        )

    def test_existing_beginning(self):
        self.assertEqual(
            array_util.find_subarray_np(
                np.array([1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5]),
                np.array([1, 2])
            ),
            0,
        )

    def test_existing_end(self):
        self.assertEqual(
            array_util.find_subarray_np(
                np.array([1, 2, 2, 4, 5, 0, 1, 2, 3, 4, 5]),
                np.array([2, 3, 4, 5])
            ),
            7,
        )

    def test_not_existing_same_end(self):
        self.assertIsNone(
            array_util.find_subarray_np(
                np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
                np.array([9, 10, 11])
            )
        )

    def test_arrays_same(self):
        self.assertEqual(
            array_util.find_subarray_np(
                np.array([1]),
                np.array([1])
            ),
            0
        )

    def test_empty_subarray(self):
        self.assertEqual(
            array_util.find_subarray_np(
                np.array([0, 1, 2, 3, 4, 5]),
                np.array([])
            ),
            0
        )

    def test_empty_array(self):
        self.assertIsNone(
            array_util.find_subarray_np(
                np.array([]),
                np.array([1, 2, 3, 4])
            )
        )

    def test_both_empty(self):
        self.assertEqual(
            array_util.find_subarray_np(
                np.array([]),
                np.array([])
            ),
            0,
        )

    def test_subarray_is_bigger(self):
        self.assertIsNone(
            array_util.find_subarray_np(
                np.array([1, 2, 3]),
                np.array([1, 2, 3, 4, 5])
            )
        )


if __name__ == '__main__':
    unittest.main()
