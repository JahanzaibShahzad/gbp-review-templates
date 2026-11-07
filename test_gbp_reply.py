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

    def test_reviewer_name_used_when_given(self):
        reply, _ = draft_reply(5, "great", "X", reviewer="Sarah", seed=0)
        self.assertIn("Sarah", reply)

    def test_no_reviewer_leaves_no_gap(self):
        # Seed 0 picks the reviewer template; with no reviewer given the
        # name slot must vanish cleanly instead of leaving "Thank you, ,".
        reply, _ = draft_reply(5, "great", "X", seed=0)
        self.assertNotIn(", ,", reply)
        self.assertNotIn("Thank you, ,", reply)
        self.assertNotIn("{reviewer}", reply)
        self.assertTrue(reply.startswith("Thank you for the 5 stars"))


class TestBatch(unittest.TestCase):
    def test_batch_writes_replies_csv(self):
        import csv
        import tempfile
        import os
        from gbp_reply import batch_reviews
        with tempfile.TemporaryDirectory() as tmp:
            src = os.path.join(tmp, "in.csv")
            out = os.path.join(tmp, "out.csv")
            with open(src, "w", newline="", encoding="utf-8") as f:
                f.write("rating,text,reviewer\n")
                f.write('5,"Lovely shop.",Sarah\n')
                f.write("2,Waited too long,\n")
                f.write("9,Not a real rating,\n")
            written, skipped = batch_reviews(src, out, business="X", seed=0)
            self.assertEqual((written, skipped), (2, 1))
            with open(out, newline="", encoding="utf-8") as f:
                rows = list(csv.DictReader(f))
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]["reviewer"], "Sarah")
            self.assertEqual(rows[0]["situation"], "5-star review with written feedback")
            self.assertIn("Sarah", rows[0]["reply"])
            self.assertEqual(rows[1]["situation"], "1-2 star negative review")


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
