import spacy

# Load pre-trained English NER model
nlp = spacy.load("en_core_web_sm")

# Sample disruption news text (matches our use case scenario)
sample_text = """
A sudden port strike has broken out in Rotterdam, Netherlands, disrupting
operations at one of Europe's busiest shipping hubs. Stuttgart Auto Factory
in Germany, which relies on the port for exports, is expected to face
significant delays. Analysts at Reuters report that the strike could impact
shipments to North America for several weeks.
"""

doc = nlp(sample_text)

print("=== Entities Found ===")
for ent in doc.ents:
    print(f"{ent.text:40s} | {ent.label_:10s} | {spacy.explain(ent.label_)}")