#Give quest 
#Complete quests
#Interact and chat



#Game Context 
#user context -> Current quests, other characters 

import openai


openai.api_key = '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'

class Character: 

    def __init__(self, creationDic):

        pass

    '''
    Send message to user 
    '''
    def character_init(self, creation_dic):

        pass

    #Sent prompt + context to head of message chain 
    def set_chain(self):

        pass

    #Get GPT to check for flags/give quests, etc. 
    def check_flags(self, message_segment):

        pass

    def issue_quest(self):

        pass


    def confirm_quest(self): 


        pass


    def issue_lore(self): 


        pass

    #Pigmalion Hopefully, automatically route to generate dialog
    def generate_dialogue(self, messages, user_input):

        messages.append({'role': 'user', 'content': user_input})
        response = openai.ChatCompletion.create(
            model='gpt-4-0613',
            temperature=0.1,
            messages = messages, 
            max_tokens=200,
            functions = [
                {
                    'name': 'confirm_quest', 
                    'description': 'If the player achieves the quest, call this function ',
                    'parameters': {
                        'type': 'object', 
                        'properties': {
                        },
                    }
                }
            ], 
            function_call='auto', 
        )
        response_message = response["choices"][0]["message"]

        try:
            function_name = response_message["function_call"]["name"]
            return response['choices'][0].message['content'], True

        except KeyError:
            print("Nothing to confess")


        messages.append({'role': 'system', 'content': response['choices'][0].message['content']})
        return response['choices'][0].message['content']








        