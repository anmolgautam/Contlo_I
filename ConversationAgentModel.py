import openai
import os
import json
from datetime import datetime
from rich import print
import tiktoken

from dotenv import load_dotenv

load_dotenv()
# api_key = os.getenv("OPEN_AI_API")
# miner = TaskMiner(api_key=api_key
#                   ,role="EA")

#encoding = tiktoken.encoding_for_model("gpt-4-1106-preview")

class ConversationalAgent:
    def __init__(self,api_key):
        self.api_key = api_key
        self.conversation_history = []
        self.client = openai.Client(api_key = self.api_key)
        self.system_prompt = self.get_system_prompt()    
        
    def get_system_prompt(self):

        #get base prompt

        with open('main_prompt.txt', 'r') as file:
            self.system_prompt = file.read()
            
        return self.system_prompt.strip()
    

    def chat_completion(self,messages: list):
        
        completion = self.client.chat.completions.create(
        model="gpt-4-1106-preview",
        #model = "gpt-3.5-turbo-1106",
        #model = "gpt-3.5-turbo-0125",
        #model = "gpt-4-0125-preview",
        max_tokens=500,
        temperature=0.5,
        response_format={ "type": "json_object" },
        messages=messages)

        #print("Input tokens are : ",len(encoding.encode(str(messages))))
        print(dict(completion)['usage'])
        out = dict(completion)
        out = dict(out['choices'][0])
        out = dict(out['message'])
        out = out['content']
        return out
        
        
    def generate_messages(self,messages: list, query: str) -> list:
    
        formated_messages = [
            {
                'role': 'system',
                'content': f'{self.system_prompt}'
            }
        ]
        for m in messages:
            
            formated_messages.append({
                'role': 'user',
                'content': m[0]
                          
            })
            formated_messages.append({
                'role': 'assistant',
                'content':m[1]
            })
        formated_messages.append(
            {
                'role': 'user',
                'content': query
            }
        )

        print("-----------------------------------")
        #print(formated_messages)
        print("-----------------------------------")
            

        return formated_messages
    
    def generate_response(self,query: str, chat_history: list) :
        
        messages = self.generate_messages(chat_history, query)
        
        
        bot_message = self.chat_completion(messages)
        
        
        chat_history.append([query, bot_message])
        
        #print("Number of message packs being send for CA: ",len(chat_history))
        
        
        return '', chat_history