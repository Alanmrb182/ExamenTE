import unittest
from unittest.mock import patch
import hashlib
import json
import pandas as pd
from main import process_countries_data  
class TestCountryProcessing(unittest.TestCase):

    @patch('main.requests.get')
    def test_process_countries_data(self, mock_get):
       
        mock_response = [
            {
                "name": {"common": "Test Country"},
                "languages": {"test": "Test Language"}
            }
        ]
        mock_get.return_value.text = json.dumps(mock_response)
        
        result = process_countries_data()
        
        self.assertIn("total_time", result)
        self.assertIn("average_time", result)
        self.assertIn("min_time", result)
        self.assertIn("max_time", result)
        self.assertIn("data", result)
        
        
        self.assertEqual(result["data"][0]["Country"], "Test Country")
        self.assertEqual(result["data"][0]["Language"], "Test Language")
        
        expected_hash = hashlib.sha1("Test Language".encode()).hexdigest()
        self.assertEqual(result["data"][0]["Encrypted Language"], expected_hash)

    def test_sha1_encryption(self):
        sample_language = "English"
        expected_hash = hashlib.sha1(sample_language.encode()).hexdigest()
        self.assertEqual(expected_hash, "f7c3bc1d808e04732adf679965ccc34ca7ae3441")

    def test_time_calculation(self):
        result = process_countries_data()
        self.assertGreater(result["total_time"], 0)
        self.assertGreater(result["average_time"], 0)
        self.assertGreater(result["max_time"], 0)
        self.assertGreaterEqual(result["min_time"], 0)

if __name__ == '__main__':
    unittest.main()
