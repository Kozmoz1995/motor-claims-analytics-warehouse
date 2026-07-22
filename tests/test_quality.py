import unittest

from motor_dwh.quality import validate_crash


def crash():
    return {
        "collision_id": "1",
        "crash_date": "2025-01-01T00:00:00.000",
        "latitude": "40.7",
        "longitude": "-73.9",
        "number_of_persons_injured": "2",
        "number_of_persons_killed": "0",
        "number_of_pedestrians_injured": "1",
        "number_of_cyclist_injured": "0",
        "number_of_motorist_injured": "1",
    }


class QualityTests(unittest.TestCase):
    def test_valid_record(self):
        self.assertTrue(validate_crash(crash()).valid)

    def test_missing_key(self):
        record = crash()
        record["collision_id"] = ""
        self.assertIn("missing_collision_id", validate_crash(record).reasons)

    def test_negative_measure(self):
        record = crash()
        record["number_of_persons_killed"] = "-1"
        self.assertIn("negative_number_of_persons_killed", validate_crash(record).reasons)

    def test_component_reconciliation(self):
        record = crash()
        record["number_of_cyclist_injured"] = "3"
        self.assertIn("injury_components_exceed_total", validate_crash(record).reasons)


if __name__ == "__main__":
    unittest.main()
