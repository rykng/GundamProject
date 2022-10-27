import unittest

from gundam import GundamNameGenerator


class TestGundam(unittest.TestCase):

    def test_pilot(self):
        result: str = GundamNameGenerator.get_random_pilot_name()
        self.assertTrue(len(result) == 1, msg="should get 1 name.")
