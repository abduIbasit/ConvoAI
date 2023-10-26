import os
import yaml
import random
import importlib
from colorama import init, Fore
# from actions import actions
from sentence_transformers import SentenceTransformer, util
from entity_extractor.entity_extractor import EntityExtractor

model = SentenceTransformer('paraphrase-distilroberta-base-v1')
# Shukroh Mosunmola Ajike loves Abdulbasit Ayinla Olanrewaju
class ConvoAI:
    def __init__(self, data_file="data.yaml"):
        with open(data_file, 'r') as file:
            self.data = yaml.safe_load(file)

        self.actions_dir = os.path.join(os.getcwd(), 'actions')
        self.prompts = [item["prompts"] for key, item in self.data.items()]
        self.question_embeddings = [model.encode(prompt, convert_to_tensor=True) for sublist in self.prompts for prompt in sublist]
        self.entity_extractor = EntityExtractor()

    def get_response(self, user_question, threshold=0.4):
        user_embedding = model.encode(user_question, convert_to_tensor=True)
        similarities = [util.pytorch_cos_sim(user_embedding, qe).item() for qe in self.question_embeddings]
        
        if max(similarities) < threshold:
            return "I'm sorry, I do not understand."

        key_name = self._get_key_name(similarities)
        
        if "ACTION" in self.data[key_name]["responses"]:
            return self._perform_action(key_name, user_question)
        else:
            return random.choice(self.data[key_name]["responses"])
        
    def _get_key_name(self, similarities):
        closest_idx = similarities.index(max(similarities))
        
        accumulated_length = 0
        for key, sublist in self.data.items():
            accumulated_length += len(sublist["prompts"])
            if closest_idx < accumulated_length:
                return key
        return None

    def _perform_action(self, key_name, user_question):
        # Get all the .py files in the actions directory
        action_files = [f for f in os.listdir(self.actions_dir) if f.endswith('.py')]

        for action_file in action_files:
            action_path = os.path.join(self.actions_dir, action_file)
            spec = importlib.util.spec_from_file_location("module_name", action_path)
            action_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(action_module)

            action_func = getattr(action_module, key_name, None)
            
            if action_func and callable(action_func):
                try:
                    return action_func(user_question)
                except Exception as e:
                    print(f"Error while executing {key_name}: \n{e}")

        return f"Error performing {key_name}."


    
    def main(self):
        init(autoreset=True)
        while True:
            try:
                user_input = input(Fore.MAGENTA + "Your Input ->" + Fore.YELLOW + " ")

                if not user_input:
                    continue
                
                if user_input == '/help':
                    print("Available commands: \n - /quit or q: Exit the chat\n - /help: View commands")
                    continue
                
                if user_input in ['/quit']:
                    # print("ConvoAI: Goodbye!")
                    exit()

                response = self.get_response(user_question=user_input)
                print(Fore.BLUE + response)

            except Exception as e:
                print(f"Oops! Something went wrong. Details: {e}")

bot = ConvoAI()
bot.main()