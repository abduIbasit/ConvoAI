import os

#************************************** ************************************** ************************************** ************************************** 
script_directory = os.path.dirname(os.path.realpath(__file__))
conversation_directory = os.path.join(os.path.dirname(script_directory), "conversation", "conversation.json")
prompts_directory = os.path.join(os.path.dirname(script_directory), "conversation", "prompts.txt")
#************************************** ************************************** ************************************** ************************************** 

import yaml
from typing import Text, List, Dict, Tuple, Any, Generator
from .entity_extractor import EntityExtractor
# from entity_extractor import EntityExtractor


def load_prompts():
        try:
            with open(prompts_directory, "r") as file:
                lines = file.readlines()
                if lines:
                    last_entry = (lines[-1])
                    return last_entry
                else:
                    return f'Could not retrieve last message'
        except FileNotFoundError as e:
            return (f'{e}')


# Check if slots.yaml is directly in the working directory
slots_config_file = os.path.join(os.getcwd(), "slots.yaml")
slots_configurations = {}


if os.path.exists(slots_config_file):
    try:
        with open(slots_config_file, "r") as config_file:
            slot_config = yaml.safe_load(config_file)
            slots_configurations.update(slot_config)
    except Exception as e:
        print(f"Error loading {slots_config_file}. Details: {e}")
    
# Check if slots.yaml is in the slots subdirectory
slots_subdir = os.path.join(os.getcwd(), "slots")
if os.path.exists(slots_subdir):
    # Load all YAML files in the slots subdirectory
    slot_files = [f for f in os.listdir(slots_subdir) if f.endswith('.yaml') or f.endswith('.yml')]
    for slot_file in slot_files:
        slot_file_path = os.path.join(slots_subdir, slot_file)
        try:
            with open(slot_file_path, "r") as config_file:
                slot_config = yaml.safe_load(config_file)
                slots_configurations.update(slot_config)
        except Exception as e:
            print(f"Error loading {slot_file}. Details: {e}")

# Initialize slots dictionary
slots = {
    slot_name: {"value": slots_configurations[slot_name].get("initial_value", None), "type": None}
    for slot_name in slots_configurations
}


def SlotSet(slot_name: Text, value: Any) -> None:
    '''
    SlotSet method sets slot value or update current value of specified slot

    Parameters:
    slot_name (Text): The name of the slot to be updated.
    value (Any): The value to be set for the slot.

    Returns:
    (None) -> Sets the value of the slot
    '''
    try:
        if not slot_name or not isinstance(slot_name, str):
            raise ValueError("Slot name must be a non-empty string.")
        
        slots[slot_name]["value"] = value
        slots[slot_name]["type"] = slots_configurations[slot_name]["type"]
    except Exception as e:
        raise ValueError(f"Error setting slot value: {e}. Slot name should match slot names in slots.yaml file")


entity_extractor = EntityExtractor()
class Tracker:
    '''
    Tracker class provides utility functions to extract information about the conversation session.

    Tracker stores conversation history and provide two methods vis a:
    
    get_entities()
    get_slot()
    '''
    @staticmethod
    def get_entities(entity_label: Text) -> Generator:
        '''
        get_entities method retrieves the entity value of specified entity label in input text

        Parameter:
        entity_label (Text): The entity label of interest to be extracted

        Returns: Generator object

        (TIP): Use in-built next method to yield the value(s) of the generator object and specify None as default parameter.
        '''
        try:
            if not entity_label or not isinstance(entity_label, str):
                raise ValueError("Entity label must be a non-empty string.")
            
            user_question = load_prompts()
            entity = entity_extractor.get_entities(text=user_question, entity_label=entity_label)
            
            if entity:
                return entity
            
        except Exception as e:
            raise ValueError(f"Error retrieving entities of type {entity_label}: {e}")

    @staticmethod
    def get_slot(slot_name: Text) -> Text:
        '''
        get_slot method retrieves the value of specified slot_name

        Parameters:
        slot_name (Text): The name of the slot to be retrieved.

        Returns: Value of specified slot if present, None, if not present
        '''
        try:
            if slot_name not in slots_configurations:
                raise ValueError(f"Slot {slot_name} is not defined in slots.yaml.")
            
            slot_type = slots_configurations[slot_name]["type"]
            
            if slot_name not in slots:
                raise ValueError(f"Slot {slot_name} does not exist.")
            
            # Check if the slot has a mapping from entities
            if slots_configurations[slot_name]['mappings'][0]['type'] == 'from_entity':
                entity_label = slots_configurations[slot_name]["mappings"][0]["entity"]
                entities = next(Tracker.get_entities(entity_label), None)
                # Use the extracted entity value as the slot value
                slots[slot_name]["value"] = entities
                slots[slot_name]["type"] = slots_configurations[slot_name]["type"]
                return entities
            
            # If the slot type is text or any, return the value as is
            elif slot_type in ["text", "any"]:
                slots[slot_name]["type"] = slots_configurations[slot_name]["type"]
                return slots[slot_name]["value"]
            
            # If the slot type is bool, convert the value to a boolean
            elif slot_type == "bool":
                slots[slot_name]["type"] = slots_configurations[slot_name]["type"]
                return slots[slot_name]["value"]
            
            # If the slot type is integer, convert the value to integer
            elif slot_type == "integer":
                slots[slot_name]["type"] = slots_configurations[slot_name]["type"]
                return int(slots[slot_name]["value"])
            
            # If the slot type is float, convert the value to float
            elif slot_type == "float":
                slots[slot_name]["type"] = slots_configurations[slot_name]["type"]
                return float(slots[slot_name]["value"])
            
            return None  # Default behavior
            
        except Exception as e:
            raise ValueError(f"Error retrieving slot value: {e}")