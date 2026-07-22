import unittest
from urllib.parse import parse_qs, urlparse

from motor_dwh.extract import build_url


class ExtractTests(unittest.TestCase):
    def test_builds_bounded_official_api_url(self):
        url = build_url("crashes", 500, 1000, "2025-01-01")
        parsed = urlparse(url)
        query = parse_qs(parsed.query)
        self.assertEqual("data.cityofnewyork.us", parsed.netloc)
        self.assertEqual(["500"], query["$limit"])
        self.assertEqual(["1000"], query["$offset"])
        self.assertIn("2025-01-01", query["$where"][0])

    def test_rejects_unbounded_page(self):
        with self.assertRaises(ValueError):
            build_url("crashes", 50001)


if __name__ == "__main__":
    unittest.main()
