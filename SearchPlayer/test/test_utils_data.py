import unittest
import lister.utils.data as du
import random
import string


class TestStringMethods(unittest.TestCase):

    def generate_random_string(self, string_size=10):
        return ''.join(random.choice(string.ascii_uppercase + string.digits)
                       for _ in range(string_size))

    def test_get_single_random(self):
        test_data = [self.generate_random_string() for i in xrange(0, 10)]
        random_song = du.get_single_random(test_data)[0]
        self.assertTrue(random_song in test_data,
                        'Chosen song is in the provided list')

    def test_get_shuffled_list(self):
        test_data = [self.generate_random_string() for i in xrange(0, 10)]
        shuffled_list = du.get_shuffled_list(test_data)
        self.assertTrue(len(test_data) == len(shuffled_list),
                        'The same amount of entries is returned')
        for song in test_data:
            self.assertTrue(song in shuffled_list,
                            'Song from shuffled list is in the provided list')
        different = False
        for index in xrange(len(test_data)):
            if (shuffled_list[index] != test_data[index]):
                different = True
        self.assertTrue(different)

    def test_get_search_filter(self):
        test_data = [self.generate_random_string() for i in xrange(0, 10)]
        cases = [{
            'label': 'Single string does not return array with only one element',
            'input': test_data[0],
            'expected': [test_data[0]]
        },
        {
            'label': 'Two strings do not return two separate strings',
            'input': ' '.join((test_data[0], test_data[1])),
            'expected': [test_data[0], test_data[1]]
        }]

        for case in cases:
            result = du.get_search_filter(case['input'])
            self.assertEqual(result, case['expected'], case['label'])


if __name__ == '__main__':
    unittest.main()
