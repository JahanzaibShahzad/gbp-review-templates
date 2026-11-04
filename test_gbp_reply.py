"""Quick sanity tests for gbp_reply.py. Run: python test_gbp_reply.py"""

import unittest

from gbp_reply import draft_reply
from templates import SITUATIONS, TEMPLATES, classify, render


class TestClassify(unittest.TestCase):
    def test_five_star_with_text(self):
        self.assertEqual(classify(5, "great"), "five_star_text")

    def test_five_star_no_text(self):
        self.assertEqual(classify(5, ""), "five_star_no_text")
        self.assertEqual(classify(5, "   "), "five_star_no_text")

    def test_four_star(self):
        self.assertEqual(classify(4, "ok"), "four_star")

    def test_three_star(self):
        self.assertEqual(classify(3, "meh"), "three_star")

    def test_one_two_star(self):
        self.assertEqual(classify(2, "bad"), "one_two_star")
        self.assertEqual(classify(1, "terrible"), "one_two_star")

    def test_low_rating_no_text(self):
        self.assertEqual(classify(2, ""), "no_text_low")

    def test_bad_rating_raises(self):
        with self.assertRaises(ValueError):
            classify(6, "x")


class TestDraftReply(unittest.TestCase):
    def test_reply_contains_business(self):
        reply, situation = draft_reply(5, "great", "AA Garments", seed=0)
        self.assertIn("AA Garments", reply)
        self.assertEqual(situation, "five_star_text")

    def test_seed_is_reproducible(self):
        a, _ = draft_reply(5, "great", "X", seed=7)
        b, _ = draft_reply(5, "great", "X", seed=7)
        self.assertEqual(a, b)

    def test_negative_reply_has_no_template_leftovers(self):
        reply, situation = draft_reply(1, "awful", "X", seed=0)
        self.assertNotIn("{business}", reply)
        self.assertEqual(situation, "one_two_star")


class TestStyle(unittest.TestCase):
    def test_no_em_dash_anywhere(self):
        import pathlib
        for path in pathlib.Path(".").glob("*.py"):
            content = path.read_text(encoding="utf-8")
            self.assertNotIn("\u2014", content, path)

    def test_all_situations_have_templates(self):
        for key in SITUATIONS:
            self.assertIn(key, TEMPLATES)
            self.assertGreater(len(TEMPLATES[key]), 0)


if __name__ == "__main__":
    unittest.main()
