import spacy
from spacy.tokens import Span
from spacy.matcher import Matcher
import yaml

class EntityExtractorError(Exception):
    """EntityExtractor exception class"""
    pass

class EntityExtractor:
    def __init__(self, pattern_file="entities.yaml"):
        try:
            # Initialize NLP components
            self.nlp = spacy.load("/Users/abdulbasitayinla/Downloads/en_core_web_sm-3.1.0/en_core_web_sm/en_core_web_sm-3.1.0")
            self.matcher = Matcher(self.nlp.vocab)
        except Exception as e:
            raise EntityExtractorError(f"Error loading SpaCy model: {e}")
        
        # Load patterns from the file
        self.load_patterns(pattern_file)
    
    def load_patterns(self, filename):
        try:
            with open(filename, 'r') as f:
                patterns = yaml.safe_load(f)
        except FileNotFoundError:
            raise EntityExtractorError(f"File {filename} not found.")
        except Exception as e:
            raise EntityExtractorError(f"Error loading patterns: {e}")

        for label, words in patterns.items():
            for word in words:
                pattern = [{"LOWER": word}]
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
            all_entities = self.extract_entities(text)
            return [ent.text for ent in all_entities if ent.label_ == entity_label]
        
        except Exception as e:
            raise ValueError(f"Error retrieving entities of type {entity_label}: {e}")