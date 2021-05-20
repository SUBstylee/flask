from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!
    def setUp(self):
        '''todo before every test'''
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_index(self):
        '''check that info and html are displaying'''
        with self.client:
            res = self.client.get('/')
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))
            self.assertIn(b'<p>HIGH SCORE:', res.data)
            self.assertIn(b'SCORE:', res.data)
            self.assertIn(b'TIME REMAINING:', res.data)

    def test_valid_word(self):
        """Test if word is valid by modifying the board in the session"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"]]
        response = self.client.get('/check-word?word=cat')
        self.assertEqual(response.json['result'], 'ok')

    def test_found_word(self):
        """is it in word.txt?"""

        self.client.get('/')
        response = self.client.get('/check-word?word=likely')
        self.assertEqual(response.json['result'], 'not-on-board')

    def test_not_word(self):
        """is it on the board?"""

        self.client.get('/')
        res = self.client.get('/check-word?word=dsjkfsadklfjdskal')
        self.assertEqual(res.json['result'], 'not-word')
