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

    def character_init(self):

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
    def sendMessage(self, user_message, message_chain):


        message_chain.append({'role': 'user', 'message': user_message})
        response = openai.ChatCompletion.create(
            model='gpt-4-0613',
            temperature=0.5,
            messages=message_chain,
            functions = [

            ], 
            function_call='auto',          
        )


        response_message = response['choices'][0]['message']


        pass


        