# ConvoAI - Conversational Chatbot Framework

ConvoAI is an open-source conversational chatbot framework designed to simplify and streamline the development of powerful conversational AI chatbots. Built on the robust sentence transformer model 'paraphrase-distilroberta-base-v1,' ConvoAI excels in understanding semantic similarity and efficiently mapping user inputs to intents with minimal data.

## Features
- **Developer-Friendly:** ConvoAI prioritizes ease of use for developers, simplifying the chatbot creation process.

- **Versatile Custom Actions:** The framework allows developers to integrate custom actions, enabling external operations such as API calls and database queries to enhance the bot's capabilities.

- **Rule-Based Development:** Chatbot development is rule-based, with defined intent prompts mapped to responses or custom actions. Training is skipped, leveraging the transformer model's proficiency in capturing semantic similarity.

- **Flexible Intent Definitions:** Intent prompts require a minimum of one example, but developers can include additional examples for intents with diverse phrasings. Responses can be either text or custom actions.

- **Entities and Slots Management:** ConvoAI efficiently manages entities and slots, facilitating the extraction and storage of crucial information from user input.

## Requirements
- <u>**Data.yaml:**</u> Defines intents, prompts, and responses.
- <u>**Entities.yaml:**</u>  Maps entity examples to entity types.
- <u>**Slots.yaml:**</u>  Configures memory slots for storing important information.
- <u>**Forms.yaml:**</u>  Defines structured forms for information acquisition.
- <u>**Rules.yaml:**</u>  Designs conversation flows and paths.
- <u>**Config.yaml:**</u>  Manages the integrated action execution engine.

## Usage
1. Define intents, prompts, and responses in **Data.yaml**.
2. Map entity examples to entity types in **Entities.yaml**.
3. Configure memory slots in **Slots.yaml**.
4. Define structured forms in **Forms.yaml**.
5. Design conversation flows in **Rules.yaml**.
6. Execute actions seamlessly with the integrated action execution engine.

## Installation
'''bash
 pip install convoai 

## Getting Started
Refer to the documentation and example files for detailed usage instructions and best practices.

## Contributing
Contributions are welcome! Check out the Contribution Guidelines for details.

## License
This project is licensed under the MIT License.
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
