import os
import unittest
import json
from bs4 import BeautifulSoup

from app import app


class HomepageTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()

        self.assertEqual(app.debug, False)

    def test_it_loads(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_calculator_loads(self):
        response = self.app.get('/')
        soup = BeautifulSoup(response.data, features='html.parser')
        self.assertTrue(soup.find(id='calculator'))


class ApiTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()

    def test_handles_max_term(self):
        response = self.app.get('/calculate_fee')
        self.assertEqual(response.status_code, 200)

    def test_returns_default_amounts(self):
        response = self.app.get('/calculate_fee')

        data = json.loads(response.data)
        self.assertEqual(data['amount'], 10000)
        self.assertEqual(data['term'], 12)

    def test_handles_max_amount(self):
        response = self.app.get('/calculate_fee', data={
            'amount': 4000000000,
            'term': 12,
        })
        data = json.loads(response.data)
        self.assertEqual(data['amount'], 20000)

    def test_handles_min_amount(self):
        response = self.app.get('/calculate_fee', data={
            'amount': 4,
            'term': 12,
        })
        data = json.loads(response.data)
        self.assertEqual(data['amount'], 1000)

    def test_handles_wrong_term(self):
        response = self.app.get('/calculate_fee', data={
            'amount': 1000,
            'term': 222,
        })
        data = json.loads(response.data)
        self.assertEqual(data['term'], 12)


class CalculatorTests(unittest.TestCase):
    def setUp(self):
        self.test_data = {
            12: [
                {'amount': 1000, 'fee': 50},
                {'amount': 2000, 'fee': 90},
                {'amount': 3000, 'fee': 90},
                {'amount': 4000, 'fee': 115},
                {'amount': 5000, 'fee': 100},
                {'amount': 6000, 'fee': 120},
                {'amount': 7000, 'fee': 140},
                {'amount': 8000, 'fee': 160},
                {'amount': 9000, 'fee': 180},
                {'amount': 15000, 'fee': 300},
                {'amount': 20000, 'fee': 400},
            ],
            24: [
                {'amount': 1000, 'fee': 70},
                {'amount': 2000, 'fee': 100},
                {'amount': 3000, 'fee': 120},
                {'amount': 4000, 'fee': 160},
                {'amount': 5000, 'fee': 200},
                {'amount': 6000, 'fee': 240},
                {'amount': 7000, 'fee': 280},
                {'amount': 8000, 'fee': 320},
                {'amount': 9000, 'fee': 360},
                {'amount': 15000, 'fee': 600},
                {'amount': 20000, 'fee': 800},
            ]
        }

    def test_results_match(self):
        from utils import calculator

        for term in self.test_data:
            for data in self.test_data[term]:
                amount = data['amount']
                expected = data['fee']
                result = calculator(term, amount)

                self.assertEqual(
                    result,
                    expected,
                    'failed at: amount:{} term:{}'.format(amount, term)
                )


if __name__ == "__main__":
    unittest.main()
