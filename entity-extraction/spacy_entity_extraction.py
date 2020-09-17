import spacy
from prompt_toolkit import prompt

nlp = spacy.load("en_core_web_md")

include_entities = ["DATE", "ORG", "PERSON"]


def extract_entities(message):
    # Create a dict to hold the entities
    ents = dict.fromkeys(include_entities)

    doc = nlp(message)
    for ent in doc.ents:
        if ent.label_ in include_entities:
            ents[ent.label_] = ent.text
    return ents


while 1:
    input = prompt("Message: ")
    print(f"Entities: {extract_entities(input)}")


# print(extract_entities('Ishwar has been working as a machine learning engineer at Fusemachines since 2018'))
# print(extract_entities('people who graduated from Pulchowk Campus in 2076'))
