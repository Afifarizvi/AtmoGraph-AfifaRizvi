import spacy

nlp = spacy.load("en_core_web_sm")

DISRUPTION_KEYWORDS = [
    "strike", "shutdown", "delay", "disrupt", "closure", "halt",
    "shortage", "blockade", "flood", "earthquake", "fire", "protest"
]

NEGATION_WORDS = ["no", "not", "without", "never", "none"]


def extract_entities(text):
    """Extract structured entities from a news/disruption text, with basic negation handling."""
    doc = nlp(text)

    locations = []
    organizations = []

    for ent in doc.ents:
        if ent.label_ == "GPE":
            locations.append(ent.text)
        elif ent.label_ == "ORG":
            organizations.append(ent.text)

    text_lower = text.lower()
    words = text_lower.split()

    detected_keywords = []
    for kw in DISRUPTION_KEYWORDS:
        for i, word in enumerate(words):
            if kw in word:
                # Check a small window before the keyword for negation words
                window = words[max(0, i - 3):i]
                if not any(neg in window for neg in NEGATION_WORDS):
                    detected_keywords.append(kw)
                break

    return {
        "locations": list(set(locations)),
        "organizations": list(set(organizations)),
        "disruption_keywords": list(set(detected_keywords)),
        "has_disruption": len(detected_keywords) > 0,
    }


if __name__ == "__main__":
    sample_texts = [
        """A sudden port strike has broken out in Rotterdam, Netherlands,
        disrupting operations. Stuttgart Auto Factory in Germany is expected
        to face significant delays.""",

        """Taiwan Semiconductor Co continues normal operations with no
        reported disruptions this quarter.""",
    ]

    for i, text in enumerate(sample_texts, 1):
        print(f"\n=== Sample {i} ===")
        result = extract_entities(text)
        print(result)