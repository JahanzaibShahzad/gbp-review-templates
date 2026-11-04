#!/usr/bin/env python3
"""Draft a Google Business Profile review reply from rating + review text.

Examples:
    python gbp_reply.py --rating 5 --text "Great service, loved the fitting."
    python gbp_reply.py --rating 5 --text "Great service." --business "AA Garments" --owner Jahanzaib
    python gbp_reply.py --rating 2 --text "Waited 30 minutes."
    python gbp_reply.py --list
"""

import argparse
import random
import sys

from templates import SITUATIONS, TEMPLATES, classify, render


def draft_reply(rating, review_text="", business="", owner="", seed=None):
    """Return a ready-to-paste reply string for a review."""
    situation = classify(rating, review_text)
    rng = random.Random(seed)
    template = rng.choice(TEMPLATES[situation])
    return render(template, business=business, owner=owner), situation


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
    parser.add_argument("--list", action="store_true",
                        help="Print every template grouped by situation and exit.")
    parser.add_argument("--seed", type=int, default=None,
                        help="Random seed for reproducible template choice.")
    args = parser.parse_args(argv)

    if args.list:
        for key, label in SITUATIONS.items():
            print("== %s ==" % label)
            for template in TEMPLATES[key]:
                print("  - " + render(template, business="<business>", owner="<owner>"))
            print()
        return 0

    if args.rating is None:
        parser.error("--rating is required unless --list is used")

    reply, situation = draft_reply(
        args.rating, args.text, args.business, args.owner, seed=args.seed
    )
    print("Situation: " + SITUATIONS[situation])
    print()
    print(reply)
    return 0


if __name__ == "__main__":
    sys.exit(main())
