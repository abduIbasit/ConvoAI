from .entity_extractor import EntityExtractor
from core import ConvoAI

instance = ConvoAI()
entity_extractor = EntityExtractor()

slots = {}

def SlotSet(slot_name, value):
    try:
        if not slot_name or not isinstance(slot_name, str):
            raise ValueError("Slot name must be a non-empty string.")
        
        # You might want more validation for the value based on your requirements
        slots[slot_name] = value
    except Exception as e:
        raise ValueError(f"Error setting slot value: {e}")

def get_entities(entity_label):
    try:
        if not entity_label or not isinstance(entity_label, str):
            raise ValueError("Entity label must be a non-empty string.")
        
        user_question = instance.current_question
        entity = entity_extractor.get_entities(user_question, entity_label)
        
        if entity:
            return entity
        else:
            return None
    except Exception as e:
        raise ValueError(f"Error retrieving entities of type {entity_label}: {e}")

def get_slot(slot_name):
    try:
        if not slot_name in slots:
            raise ValueError(f"Slot '{slot_name}' does not exist.")
        return slots.get(slot_name)
    except Exception as e:
        raise ValueError(f"Error retrieving slot value: {e}")