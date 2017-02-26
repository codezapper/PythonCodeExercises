import unittest
from lister.data_utils import get_single_random, get_shuffled_list
import random
import string


class TestStringMethods(unittest.TestCase):

    def generate_random_string(self, string_size=10):
        return ''.join(random.choice(string.ascii_uppercase + string.digits)
                       for _ in range(string_size))

    def test_get_single_random(self):
        test_data = [self.generate_random_string() for i in xrange(0, 10)]
        random_song = get_single_random(test_data)[0]
        self.assertTrue(random_song in test_data,
                        'Chosen song is in the provided list')

    def test_get_shuffled_list(self):
        test_data = [self.generate_random_string() for i in xrange(0, 10)]
        shuffled_list = get_shuffled_list(test_data)
        self.assertTrue(len(test_data) == len(shuffled_list),
                        'The same amount of entries is returned')
        for song in test_data:
            self.assertTrue(song in shuffled_list,
                            'Song from shuffled list is in the provided list')

if __name__ == '__main__':
    unittest.main()
