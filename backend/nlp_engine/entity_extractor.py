import spacy

nlp = spacy.load("en_core_web_sm")

# Keywords that indicate a supply chain disruption
DISRUPTION_KEYWORDS = [
    "strike", "shutdown", "delay", "disrupt", "closure", "halt",
    "shortage", "blockade", "flood", "earthquake", "fire", "protest"
]


def extract_entities(text):
    """Extract structured entities from a news/disruption text."""
    doc = nlp(text)

    locations = []
    organizations = []

    for ent in doc.ents:
        if ent.label_ == "GPE":
            locations.append(ent.text)
        elif ent.label_ == "ORG":
            organizations.append(ent.text)

    # Simple keyword-based disruption detection
    text_lower = text.lower()
    detected_keywords = [kw for kw in DISRUPTION_KEYWORDS if kw in text_lower]

    return {
        "locations": list(set(locations)),
        "organizations": list(set(organizations)),
        "disruption_keywords": detected_keywords,
        "has_disruption": len(detected_keywords) > 0,
    }


if __name__ == "__main__":
    sample_texts = [
        """A sudden port strike has broken out in Rotterdam, Netherlands,
        disrupting operations. Stuttgart Auto Factory in Germany is expected
        to face significant delays.""",

        """Shenzhen Electronics Factory announced a temporary shutdown due to
        a fire at its main production facility in China.""",

        """Congo Cobalt Mines reported a shortage of skilled labor, causing
        delays in raw material shipments to Shenzhen Electronics Factory.""",

        """Taiwan Semiconductor Co continues normal operations with no
        reported disruptions this quarter.""",
    ]

    for i, text in enumerate(sample_texts, 1):
        print(f"\n=== Sample {i} ===")
        result = extract_entities(text)
        print(result)