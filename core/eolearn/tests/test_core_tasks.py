import unittest
import logging
import datetime
import numpy as np

from copy import copy, deepcopy

from eolearn.core import EOPatch, CopyTask, DeepCopyTask


logging.basicConfig(level=logging.DEBUG)


class TestCoreTasks(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.patch = EOPatch()

        cls.patch.data['bands'] = np.arange(2*3*3*2).reshape(2, 3, 3, 2)
        cls.patch.mask_timeless['mask'] = np.arange(3*3*2).reshape(3, 3, 2)
        cls.patch.scalar['values'] = np.arange(10*5).reshape(10, 5)
        cls.patch.timestamp = [datetime.datetime(2017, 1, 1, 10, 4, 7),
                               datetime.datetime(2017, 1, 4, 10, 14, 5),
                               datetime.datetime(2017, 1, 11, 10, 3, 51),
                               datetime.datetime(2017, 1, 14, 10, 13, 46),
                               datetime.datetime(2017, 1, 24, 10, 14, 7),
                               datetime.datetime(2017, 2, 10, 10, 1, 32),
                               datetime.datetime(2017, 2, 20, 10, 6, 35),
                               datetime.datetime(2017, 3, 2, 10, 0, 20),
                               datetime.datetime(2017, 3, 12, 10, 7, 6),
                               datetime.datetime(2017, 3, 15, 10, 12, 14)]
        cls.patch.bbox = '324.54,546.45,955.4,63.43'
        cls.patch.meta_info['something'] = np.random.rand(10, 1)

    def test_copy(self):
        patch_copy = copy(self.patch)

        self.assertTrue(self.patch == patch_copy, 'Copied patch is different')

        patch_copy.data['new'] = np.arange(1).reshape(1, 1, 1, 1)
        self.assertFalse('new' in self.patch.data, 'Dictionary of features was not copied')

        patch_copy.data['bands'][0, 0, 0, 0] += 1
        self.assertTrue(np.array_equal(self.patch.data['bands'], patch_copy.data['bands']),
                        'Data should not be copied')

    def test_deepcopy(self):
        patch_deepcopy = deepcopy(self.patch)

        self.assertTrue(self.patch == patch_deepcopy, 'Deep copied patch is different')

        patch_deepcopy.data['new'] = np.arange(1).reshape(1, 1, 1, 1)
        self.assertFalse('new' in self.patch.data, 'Dictionary of features was not copied')

        patch_deepcopy.data['bands'][0, 0, 0, 0] += 1
        self.assertFalse(np.array_equal(self.patch.data['bands'], patch_deepcopy.data['bands']),
                         'Data should be copied')


if __name__ == '__main__':
    unittest.main()
