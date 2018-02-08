import os
import json
import unittest

from app import app


TEST_DB = 'test.db'


class BasicTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_new_word(self):
        # When not logged in, redirects to login
        response = self.app.get('/hangman/new_word')
        self.assertEqual(response.status_code, 302)
        self.login('gabriele', 'g')
        response = self.app.get('/hangman/new_word', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_character(self):
        # When not logged in, redirects to login
        response = self.app.get('/hangman/character')
        self.assertEqual(response.status_code, 302)
        self.login('gabriele', 'g')
        response = self.app.get('/hangman/character', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)


    def logout(self):
        return self.app.get('/logout', follow_redirects=True)


if __name__ == "__main__":
    unittest.main()
