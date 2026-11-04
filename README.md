# GBP Review Reply Templates

Ready-made Google Business Profile review reply templates by situation, plus a tiny Python helper that drafts a reply from a star rating and the review text.

Built by a Local SEO specialist who answers client reviews every day and wanted a copy-paste starting point that always sounds human.

## Why this exists

Reviews move the needle in local SEO. Fast, personal replies to reviews signal activity on your Google Business Profile, and they are one of the simplest things a local business can do consistently. This project gives you:

- Templates for every common situation: 5-star, 4-star, 3-star, 1-2 star, reviews with no text, and suspicious/fake reviews.
- A small CLI that picks a suitable template and fills in your business name.

## Usage

No installation needed. Python 3.8 or newer is all you need (standard library only).

```bash
# See every template grouped by situation
python gbp_reply.py --list

# Draft a reply for a 5-star review
python gbp_reply.py --rating 5 --text "Great fitting, fair prices." --business "AA Garments"

# Draft a reply for a 2-star review (no business name needed)
python gbp_reply.py --rating 2 --text "Waited 30 minutes for my order."

# Use a seed for a reproducible pick (otherwise random)
python gbp_reply.py --rating 5 --text "Lovely shop." --seed 1
```

You can also import it:

```python
from gbp_reply import draft_reply

reply, situation = draft_reply(
    rating=3,
    review_text="Average experience.",
    business="AA Garments",
)
print(situation)  # "3-star review"
print(reply)      # ready-to-paste text
```

## Template philosophy (honest notes)

- Every template is one to three sentences, written like a real owner, not a bot. Edit the wording to match your voice before you paste it.
- For negative reviews, the templates invite the reviewer to contact you directly. That keeps the back-and-forth private and shows future readers you care.
- The "fake review" template asks the reviewer to get in touch instead of accusing them publicly. If the review is genuinely fake, still flag it inside your Google Business Profile, no template can do that for you.
- Randomness is on purpose: replying to every 5-star review with the same sentence looks automated. Use `--seed` if you want the same pick twice.
- These are starting points. A genuine personal detail about the visit beats any template.

## Files

- `gbp_reply.py` - CLI and the `draft_reply()` helper.
- `templates.py` - the template library, grouped by situation.
- `test_gbp_reply.py` - quick sanity tests.

## License

MIT. See `LICENSE`.
