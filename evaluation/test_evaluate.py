"""Checks evaluator semantics only; these tests say nothing about a model."""
import unittest
from evaluate import evaluate, load_rows


class EvaluatorTests(unittest.TestCase):
    def setUp(self):
        self.cases = load_rows("smoke-cases.jsonl")
        self.outputs = load_rows("handwritten-outputs.jsonl")

    def test_separates_leakage_from_overmasking(self):
        result = evaluate(self.cases, self.outputs)
        self.assertEqual(result["overall"]["exact_match_rate"], 1 / 3)
        self.assertEqual(result["overall"]["literal_leak_rate"], 1 / 2)
        self.assertEqual(result["overall"]["missing_kept_literal_rate"], 1 / 3)
        self.assertEqual(result["cases"][0]["literal_leaks"], 1)
        self.assertEqual(result["cases"][1]["missing_kept_literals"], 1)

    def test_no_remove_checks_is_unmeasured(self):
        result = evaluate(self.cases, self.outputs)
        self.assertIsNone(result["slices"]["negative"]["literal_leak_rate"])

    def test_missing_prediction_is_rejected(self):
        del self.outputs["smoke-01"]
        with self.assertRaises(ValueError):
            evaluate(self.cases, self.outputs)

    def test_empty_evaluation_is_not_zero(self):
        self.assertIsNone(evaluate({}, {})["overall"]["exact_match_rate"])

    def test_non_string_output_is_rejected(self):
        self.outputs["smoke-01"]["output"] = None
        with self.assertRaises(ValueError):
            evaluate(self.cases, self.outputs)


if __name__ == "__main__":
    unittest.main()
