from typing import Text, Any, Dict
import os
import sys
import json
import time
import yaml
import random
import importlib
from colorama import init, Fore
from sentence_transformers import SentenceTransformer, util
from convoai_sdk.entity_extractor import EntityExtractor

model = SentenceTransformer('paraphrase-distilroberta-base-v1')
# Shukroh Mosunmola Ajike loves Abdulbasit Ayinla Olanrewaju
class ConvoAI:
    def __init__(self, data_file="data.yaml"):
        try:
            with open(data_file, 'r') as file:
                self.data = yaml.safe_load(file)
        except FileNotFoundError:
            print(f"Error: {data_file} not found.")
            exit()
        except yaml.YAMLError as exc:
            print(f"Error parsing YAML file {data_file}.Details: \n{exc}")
            exit()

        self.actions_dir = os.path.join(os.getcwd(), 'actions')
        self.prompts = [item["prompts"] for key, item in self.data.items()]
        self.question_embeddings = [model.encode(prompt, convert_to_tensor=True) for sublist in self.prompts for prompt in sublist]
        self.entity_extractor = EntityExtractor()
        self.current_input = None

    def get_response(self, user_input: Text, threshold=0.4):
        try:
            user_embedding = model.encode(user_input, convert_to_tensor=True)
        except Exception as e:
            return f"Error processing your input. Details: {e}"
        similarities = [util.pytorch_cos_sim(user_embedding, qe).item() for qe in self.question_embeddings]
        
        if max(similarities) < threshold:
            return "I'm sorry, I do not understand."

        key_name = self._get_key_name(similarities)
        
        if "ACTION" in self.data[key_name]["responses"]:
            return self._perform_action(key_name, user_input)
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
        try:
            action_files = [f for f in os.listdir(self.actions_dir) if f.endswith('.py')]
        except OSError as e:
            return f"Error accessing actions directory. Details:\n {e}"
        
        # Add the actions directory to sys.path to allow module imports
        sys.path.append(self.actions_dir)
        
        for action_file in action_files:
            module_name = action_file.rstrip('.py')  # Strip .py extension
            # if module_name == "actions":
            #     # Directly execute actions.py
            #     with open(os.path.join(self.actions_dir, action_file), 'r') as file:
            #         exec(file.read())
            # else:
            #     # Dynamically import other .py files
            try:
                action_module = importlib.import_module(module_name)
                action_func = getattr(action_module, key_name, None)            
                if action_func and callable(action_func):
                    try:
                        return action_func()
                    except Exception as e:
                        print(f"Error while executing {key_name}. Details: \n{e}")
                        return f"Could not complete the action {key_name}"
                        
            except Exception as e:
                    print(f"Error loading or executing {action_file}. \nDetails: {e}")
                    exit()

        return f"Action {key_name} not found in the actions directory."
    
    def _form_loop(self, key_name):
        pass

        
        # for action_file in action_files:
        #     try:
        #         action_path = os.path.join(self.actions_dir, action_file)
        #         spec = importlib.util.spec_from_file_location("module_name", action_path)
        #         action_module = importlib.util.module_from_spec(spec)
        #         spec.loader.exec_module(action_module)
        #     except Exception as e:
        #         return f"Error loading or executing {action_file}. \n{e}"


        #     action_func = getattr(action_module, key_name, None)            
        #     if action_func and callable(action_func):
        #         try:
        #             return action_func()
        #         except Exception as e:
        #             print(f"Error while executing {key_name}: \n{e}")
        #             return f"Could not complete the action {key_name}"


    
    def main(self):
        init(autoreset=True)
        while True:
            try:
                user_input = input(Fore.MAGENTA + "Your Input ->" + Fore.YELLOW + " ")
                self.current_input = user_input

                if not user_input:
                    continue
                
                if user_input == '/help':
                    print("Available commands: \n - /quit or q: Exit the chat\n - /help: View commands")
                    continue
                
                if user_input in ['/quit']:
                    # print("ConvoAI: Goodbye!")
                    exit()

                self.response = self.get_response(user_input=user_input)
                if not self.response:
                    continue

                self.save_conversation()

                print (Fore.BLUE + self.response)
                # return user_input

            # except KeyboardInterrupt:
            #     # print("\nExiting chat. Goodbye!")
            #     exit()

            except Exception as e:
                print(f"Oops! Something went wrong. Details: \n{e}")


    def save_conversation(self):
        entry = {'time': time.ctime(), 'text': self.current_input, 'response':self.response}
        with open("./conversation/conversation.json", "a") as file:
            json.dump(entry, file)
            file.write('\n')

bot = ConvoAI()
bot.main()