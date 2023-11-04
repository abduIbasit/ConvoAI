import os
import json
from typing import Text, List, Dict, Tuple, Any
from .entity_extractor import EntityExtractor
# from entity_extractor import EntityExtractor

entity_extractor = EntityExtractor()
slots = {}

script_directory = os.path.dirname(os.path.realpath(__file__))
conversation_directory = os.path.join(os.path.dirname(script_directory), "conversation", "conversation.json")

def load_conversation():
        try:
            with open(conversation_directory, "r") as file:
                lines = file.readlines()
                if lines:
                    last_entry = json.loads(lines[-1])
                    message = last_entry['text']
                    return message
                else:
                    return f'Could not retrieve last message'
        except FileNotFoundError as e:
            return (f'{e}')

def SlotSet(slot_name: Text, value: Any):
    '''
    SlotSet method sets slot value or update current value of slot specified

    Parameters:
    slot_name (Text): The name of the slot to be updated.
    value (Any): The value to be set for the slot.

    Returns:
    (None) -> Sets the value of the slot
    '''
    try:
        if not slot_name or not isinstance(slot_name, str):
            raise ValueError("Slot name must be a non-empty string.")
        
        # You might want more validation for the value based on your requirements
        slots[slot_name] = value
    except Exception as e:
        raise ValueError(f"Error setting slot value: {e}")

def get_entities(entity_label: Text):
    try:
        if not entity_label or not isinstance(entity_label, str):
            raise ValueError("Entity label must be a non-empty string.")
        
        # print(instance.current_question)
        # instance.main()
        # if load_conversation == None:
            # raise ValueError("User input could not be retrieved")
        
        user_question = load_conversation()
        print(user_question)
        entity = entity_extractor.get_entities(text=user_question, entity_label=entity_label)
        
        if entity:
            return entity
        else:
            return None
    except Exception as e:
        raise ValueError(f"Error retrieving entities of type {entity_label}: {e}")

def get_slot(slot_name: Text):
    try:
        if not slot_name in slots:
            raise ValueError(f"Slot '{slot_name}' does not exist.")
        return slots.get(slot_name)
    except Exception as e:
        raise ValueError(f"Error retrieving slot value: {e}")


# import json

# def load_conversation():
#         try:
#             with open("../conversation/conversation.json", "r") as file:
#                 lines = file.readlines()
#                 if lines:
#                     last_entry = json.loads(lines[-1])
#                     message = last_entry['text']
#                     print(message)
#                 else:
#                     print('Not found')
#         except FileNotFoundError as e:
#             print(f'{e}')

# load_conversation()


# # def get_entities(entity_label: Text):
# #     try:
# #         if not entity_label or not isinstance(entity_label, str):
# #             raise ValueError("Entity label must be a non-empty string.")
        
# #         # print(instance.current_question)
# #         # instance.main()
# #         # if load_conversation == None:
# #         #     raise ValueError("User input could not be retrieved")
        
# #         user_question = load_conversation()
# #         # print(user_question)
# #         entity = entity_extractor.get_entities(text=user_question, entity_label=entity_label)
        
# #         if entity:
# #             print(entity)
# #         else:
# #             return None
# #     except Exception as e:
# #         raise ValueError(f"Error retrieving entities of type {entity_label}: {e}")


# # get_entities("food")