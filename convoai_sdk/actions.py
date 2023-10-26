from entity_extractor.entity_extractor import EntityExtractor

class Action:
    def __init__(self):
        self.entity_extractor = EntityExtractor()
        self.slots = {}
    
    def get_entities(self, user_question, entity_label):
        entity = self.entity_extractor.get_entities(user_question, entity_label)
        if entity!= []:
            return entity

    def SlotSet(self, slot_name, value):
        self.slots[slot_name] = value

    def get_slot(self, slot_name):
        return self.slots.get(slot_name)