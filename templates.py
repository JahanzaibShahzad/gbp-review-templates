"""GBP review reply templates, organized by situation.

Each entry is a template string that accepts these placeholders:
  {business}  business name
  {owner}     owner/reviewer-facing name (optional)

Keep every template free of the em dash character, and keep them
short: one to three sentences, exactly how a real owner would write.
"""

TEMPLATES = {
    "five_star_text": [
        "Thank you so much for the 5 stars, {business} really appreciates your kind words. We look forward to seeing you again soon!",
        "This made our day. Thank you for choosing {business} and for taking the time to leave such a great review.",
        "We are so glad you had a great experience with us. Thank you for the 5-star review, and we hope to serve you again!",
    ],
    "five_star_no_text": [
        "Thank you for the 5-star rating! We appreciate your support and look forward to seeing you again.",
        "Thanks a lot for the 5 stars. It means a lot to the whole team at {business}.",
    ],
    "four_star": [
        "Thank you for the 4-star review and your feedback. We would love to know what would have made it a 5-star visit, so please tell us next time you are in.",
        "Thanks for the kind review! We are always looking to improve, so feel free to share any suggestions with us.",
    ],
    "three_star": [
        "Thank you for your honest feedback. We are sorry your visit was only average, and we would like to make your next one better. Please reach out to us directly so we can help.",
        "Thanks for the review. We hear you, and we are working on improving. We would love another chance to give you a 5-star experience.",
    ],
    "one_two_star": [
        "We are sorry to hear about your experience. This is not the standard we aim for at {business}. Please contact us directly so we can make this right.",
        "Thank you for bringing this to our attention. We take this seriously and would like to fix it. Please reach out to us so we can discuss what happened.",
        "We sincerely apologize for the poor experience. Please get in touch with us directly, we want the chance to make it up to you.",
    ],
    "no_text_low": [
        "Thank you for the rating. We would love to know how we can improve your experience next time, so please feel free to contact us.",
    ],
    "spam_or_fake": [
        "Thank you for your review. We could not find any record of this visit in our system, so please contact us directly so we can look into it.",
    ],
}

SITUATIONS = {
    "five_star_text": "5-star review with written feedback",
    "five_star_no_text": "5-star review with no written feedback",
    "four_star": "4-star review",
    "three_star": "3-star review",
    "one_two_star": "1-2 star negative review",
    "no_text_low": "Low-star review with no written text",
    "spam_or_fake": "Review that looks fake or unrelated",
}


def classify(rating, review_text):
    """Pick the situation key for a rating and review text."""
    text = (review_text or "").strip()
    if rating == 5:
        return "five_star_text" if text else "five_star_no_text"
    if rating == 4:
        return "four_star"
    if rating == 3:
        return "three_star"
    if rating in (1, 2):
        return "no_text_low" if not text else "one_two_star"
    raise ValueError("rating must be 1-5, got %r" % (rating,))


def get_templates(situation):
    """Return all templates for a situation key."""
    return TEMPLATES[situation]


def render(template, business="", owner=""):
    """Fill placeholders in a template."""
    return template.format(
        business=business or "our business",
        owner=owner or "the team",
    )
