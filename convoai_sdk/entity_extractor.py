import spacy
from spacy.tokens import Span
from spacy.matcher import Matcher
import yaml
import re

class EntityExtractorError(Exception):
    """EntityExtractor exception class"""
    pass

class EntityExtractor:
    def __init__(self, pattern_file="entities.yaml"):
        try:
            # Initialize NLP components
            self.nlp = spacy.load("en_core_web_sm")
            self.matcher = Matcher(self.nlp.vocab)
        except Exception as e:
            raise EntityExtractorError(f"Error loading SpaCy model: {e}")
        
        # Load patterns from the file
        self.load_patterns(pattern_file)
    
    def load_patterns(self, filename):
        try:
            with open(filename, 'r') as f:
                self.patterns = yaml.safe_load(f)
        except FileNotFoundError:
            raise EntityExtractorError(f"File {filename} not found.")
        except Exception as e:
            raise EntityExtractorError(f"Error loading patterns: {e}")

        for label, words in self.patterns.items():
            for word in words:
                if word != 'regex':
                    pattern = [{"LOWER": word.lower()}]
                    self.matcher.add(label, [pattern])

    def extract_entities(self, text):
        try:
            doc = self.nlp(text)
            matches = self.matcher(doc)
            
            new_ents = []
            for match_id, start, end in matches:
                string_id = self.nlp.vocab.strings[match_id]
                entity = Span(doc, start, end, label=string_id)
                new_ents.append(entity)
            
            entities = [ent for ent in doc.ents if not any([span.start <= ent.end and span.end >= ent.start for span in new_ents])]
            doc.ents = tuple(entities + new_ents)
            
            return doc.ents
        
        except Exception as e:
            raise ValueError(f"Error during entity extraction: {e}")


    def get_entities(self, text, entity_label):
        try:
            for label, words in self.patterns.items():
                if type(words) is dict:
                    for k, v in words.items():
                        if label == entity_label:
                            a = [re.findall(v, t) for t in text.split()]
                            b = (a[0] for a in a if a != [])
                            return (b)
                
            all_entities = self.extract_entities(text)
            # return [ent.text for ent in all_entities if ent.label_ == entity_label]
            entities = (ent.text for ent in all_entities if ent.label_ == entity_label)
            return entities
        
        except Exception as e:
            raise ValueError(f"Error retrieving entities of type {entity_label}: {e}")
        
answer = EntityExtractor().get_entities('my account number is New York City', 'GPE')

# def test():
#     if answer:
#         return(answer)
#     else:
#         list = [None]
#         li = (l for l in list)
#         return(li)

# def order():
#     use = next(test())
#     print(use)

# test()
# print(next(answer))
print(next(answer, None))