import unittest
from validator import validate_json

class TestValidator(unittest.TestCase):
    def test_validate_json(self):
        with open('tests/data/valid_json.json', 'r') as f:
            json_data = json.load(f)
        self.assertTrue(validate_json(json_data))

if __name__ == '__main__':
    unittest.main()