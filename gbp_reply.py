#!/usr/bin/env python3
"""Draft a Google Business Profile review reply from rating + review text.

Examples:
    python gbp_reply.py --rating 5 --text "Great service, loved the fitting."
    python gbp_reply.py --rating 5 --text "Great service." --business "AA Garments" --owner Jahanzaib
    python gbp_reply.py --rating 2 --text "Waited 30 minutes."
    python gbp_reply.py --rating 5 --text "Lovely shop." --reviewer "Sarah"
    python gbp_reply.py --list
    python gbp_reply.py --batch reviews.csv --output replies.csv

Batch input CSV columns: rating, text, reviewer (reviewer optional,
text may be empty). Output CSV columns: rating, reviewer, text,
situation, reply. Rows with an invalid rating are skipped with a
warning on stderr, the rest are still processed.
"""

import argparse
import csv
import random
import sys

from templates import SITUATIONS, TEMPLATES, classify, render


def draft_reply(rating, review_text="", business="", owner="", seed=None,
                reviewer=""):
    """Return a ready-to-paste reply string for a review."""
    situation = classify(rating, review_text)
    rng = random.Random(seed)
    template = rng.choice(TEMPLATES[situation])
    return (render(template, business=business, owner=owner, reviewer=reviewer),
            situation)


def batch_reviews(input_path, output_path, business="", owner="", seed=None):
    """Draft replies for every review in a CSV file.

    Returns (written, skipped): how many replies were written to the
    output CSV and how many input rows were skipped as invalid.
    """
    written = 0
    skipped = 0
    with open(input_path, newline="", encoding="utf-8") as infile, \
            open(output_path, "w", newline="", encoding="utf-8") as outfile:
        reader = csv.DictReader(infile)
        writer = csv.DictWriter(
            outfile,
            fieldnames=["rating", "reviewer", "text", "situation", "reply"],
        )
        writer.writeheader()
        for lineno, row in enumerate(reader, start=2):
            try:
                rating = int((row.get("rating") or "").strip())
            except ValueError:
                print("warning: line %d: bad rating %r, skipped"
                      % (lineno, row.get("rating")), file=sys.stderr)
                skipped += 1
                continue
            try:
                reply, situation = draft_reply(
                    rating,
                    review_text=row.get("text") or "",
                    business=business,
                    owner=owner,
                    seed=seed,
                    reviewer=row.get("reviewer") or "",
                )
            except ValueError as exc:
                print("warning: line %d: %s, skipped" % (lineno, exc),
                      file=sys.stderr)
                skipped += 1
                continue
            writer.writerow({
                "rating": rating,
                "reviewer": row.get("reviewer") or "",
                "text": row.get("text") or "",
                "situation": SITUATIONS[situation],
                "reply": reply,
            })
            written += 1
    return written, skipped


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Draft a Google Business Profile review reply."
    )
    parser.add_argument("--rating", type=int, choices=[1, 2, 3, 4, 5],
                        help="Star rating of the review (1-5).")
    parser.add_argument("--text", default="",
                        help="The review text (leave empty if there is none).")
    parser.add_argument("--business", default="",
                        help="Your business name (used in some templates).")
    parser.add_argument("--owner", default="",
                        help="Your name (used in some templates).")
    parser.add_argument("--reviewer", default="",
                        help="The reviewer's name (used in some templates).")
    parser.add_argument("--batch", default=None, metavar="INPUT.csv",
                        help="Draft replies for every review in a CSV file "
                        "(columns: rating, text, reviewer).")
    parser.add_argument("--output", default=None, metavar="OUTPUT.csv",
                        help="Where to write batch replies (default: "
                        "replies.csv next to the input file).")
    parser.add_argument("--list", action="store_true",
                        help="Print every template grouped by situation and exit.")
    parser.add_argument("--seed", type=int, default=None,
                        help="Random seed for reproducible template choice.")
    args = parser.parse_args(argv)

    if args.list:
        for key, label in SITUATIONS.items():
            print("== %s ==" % label)
            for template in TEMPLATES[key]:
                print("  - " + render(template, business="<business>", owner="<owner>",
                                     reviewer="<reviewer>"))
            print()
        return 0

    if args.batch:
        output = args.output or "replies.csv"
        written, skipped = batch_reviews(
            args.batch, output, business=args.business, owner=args.owner,
            seed=args.seed,
        )
        print("Wrote %d %s to %s" % (
            written, "reply" if written == 1 else "replies", output))
        if skipped:
            print("Skipped %d invalid %s (see warnings above)"
                  % (skipped, "row" if skipped == 1 else "rows"))
        return 0

    if args.rating is None:
        parser.error("--rating is required unless --list or --batch is used")

    reply, situation = draft_reply(
        args.rating, args.text, args.business, args.owner, seed=args.seed,
        reviewer=args.reviewer,
    )
    print("Situation: " + SITUATIONS[situation])
    print()
    print(reply)
    return 0


if __name__ == "__main__":
    sys.exit(main())
