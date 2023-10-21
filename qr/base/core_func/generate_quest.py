'''
Generate Quest Function

Get all characters and locations 
-> Generate a chain of events
-> Check Admin panel for requirements 
-> Generate quest line if they player does not have one
->
'''
import openai 
import json
import os

openai.api_key = os.environ.get('OPENAI_API_KEY')

from ..models import Quest

class QuestGenerator:

    def __init__(self, characters, locations, context): 
        self.characters = characters
        self.locations = locations
        self.content = context
        pass

    #Generate 3 quests for the player initially 
    def generate_quests_intial(self, characters, locations, story_context):


        quests_completed = Quest.objects.filter(completed=True)
        quests_completed = {quest.name: quest.description for quest in quests_completed}

        context = [
            {'role': 'system', 'content': 'You are a quest generator, you must generate quests for the player based off the characters in the game, the locations and the games context'},
            {'role': 'system', 'content': 'The quests must be simple and only involve either a character or a location, not both. Quests involve visiting a location or talking to a certain character'},
            {'role': 'system', 'content': 'This is what has happened in the game so far: ' + str(story_context)},
            {'role': 'system', 'content': 'These are the quests already completed by the player: ' + str(quests_completed)},
            {'role': 'system', 'content': 'These are the characters in the game: ' + str(characters)},
            {'role': 'system', 'content': 'These are the locations in the game: ' + str(locations)},
        ]
        print(context)
        quests = openai.ChatCompletion.create(
            model='gpt-4-0613',
            temperature=0.3,
            messages=context,
            functions = [

                {
                    'name': 'generate_quests',
                    'description': 'Generate quests for the player',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'name': {
                                'type': 'string',
                                'description': 'The name of the quest',
                            },
                            'description': {
                                'type': 'string',
                                'description': 'The description of the quest',
                            },
                            'character': {
                                'type': 'string',
                                'description': 'The character the quest is for',
                            },
                            'location': {
                                'type': 'string',
                                'description': 'The location the quest is associated with',
                            }
                        }
                 }
                }
                                              
            ], 
            
        )
        parsed_quests = self.parse_quests(str(quests))
        print(parsed_quests)
        return parsed_quests

    def clean_string(self,s):
        if isinstance(s, str):
            return s.replace('\n', '').replace('\\n', '')  # Handles both escaped and unescaped newlines
        return s  # Return as is if not a string

    #From GPT - Parse quest and add as Django entry 
    def parse_quests(self, json_string): 

        data = json.loads(json_string)

        # Navigate to the function_call arguments
        function_arguments = data.get("choices", [])[0].get("message", {}).get("function_call", {}).get("arguments", "")

        # Remove newline characters
        clean_arguments = function_arguments.replace('\n', '').replace('\\n', '')  # Handles both escaped and unescaped newlines

        # Convert the arguments JSON string to a dictionary
        arguments_dict = json.loads(clean_arguments)

        return arguments_dict
    

    def generate_quest(self, story_context):
        response = self.generate_quests_intial(self.characters, self.locations, story_context)
        return response



def main():

    characters = [{"name": "Arthur", "description": "The brave king."}, {"name": "Merlin", "description": "The wise wizard."}]
    locations = ["Camelot", "Dark Forest"]
    story_context = "The kingdom is in peril and needs a hero."

    quest_generator = QuestGenerator(characters, locations)
    quest_generator.generate_quests_intial(characters, locations, story_context)

    pass



if __name__ == "__main__":
    main()