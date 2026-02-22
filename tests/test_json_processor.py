import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from extractor import validate_json

VALID_RECORD = {
    "id": "123",
    "timestamp": "2026-02-20T12:00:00Z",
    "payload": {"name": "John Doe", "email": "john@example.com"},
}


class TestValidateJson(unittest.TestCase):
    def test_valid_record(self):
        valid, error = validate_json(VALID_RECORD)
        self.assertTrue(valid)
        self.assertIsNone(error)

    def test_valid_timestamp_with_offset(self):
        data = {**VALID_RECORD, "timestamp": "2026-02-20T12:00:00+05:30"}
        valid, error = validate_json(data)
        self.assertTrue(valid)

    def test_missing_id(self):
        data = {"timestamp": "2026-02-20T12:00:00Z", "payload": {}}
        valid, error = validate_json(data)
        self.assertFalse(valid)
        self.assertIn("Missing field: id", error)

    def test_missing_timestamp(self):
        data = {"id": "123", "payload": {}}
        valid, error = validate_json(data)
        self.assertFalse(valid)
        self.assertIn("Missing field: timestamp", error)

    def test_missing_payload(self):
        data = {"id": "123", "timestamp": "2026-02-20T12:00:00Z"}
        valid, error = validate_json(data)
        self.assertFalse(valid)
        self.assertIn("Missing field: payload", error)

    def test_id_must_be_string(self):
        data = {**VALID_RECORD, "id": 123}
        valid, error = validate_json(data)
        self.assertFalse(valid)
        self.assertIn("id must be string", error)

    def test_timestamp_invalid_format(self):
        data = {**VALID_RECORD, "timestamp": "not-a-date"}
        valid, error = validate_json(data)
        self.assertFalse(valid)
        self.assertIn("ISO-8601", error)

    def test_timestamp_not_string(self):
        data = {**VALID_RECORD, "timestamp": 12345}
        valid, error = validate_json(data)
        self.assertFalse(valid)
        self.assertIn("timestamp", error)

    def test_payload_must_be_object(self):
        data = {**VALID_RECORD, "payload": "not an object"}
        valid, error = validate_json(data)
        self.assertFalse(valid)
        self.assertIn("payload must be object", error)

    def test_root_must_be_dict(self):
        valid, error = validate_json([])
        self.assertFalse(valid)
        self.assertIn("root must be an object", error)

    def test_root_none(self):
        valid, error = validate_json(None)
        self.assertFalse(valid)
        self.assertIn("object", error)


if __name__ == "__main__":
    unittest.main()
