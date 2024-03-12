from db import RAG
import os
import json
from datetime import datetime
from dotenv import load_dotenv
import gradio as gr
from rich import print, print_json
from ConversationAgentModel import ConversationalAgent
load_dotenv()



#initialize document store
docstore = RAG('final.csv')
docstore.create_collection()

api_key = os.getenv("OPEN_AI_API")

bot = ConversationalAgent(api_key)

def get_curent_datetime() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")

def chat_session(query,chat_history):
    
    #add retrieved docs from db to system prompt here
    processing_query = json.loads(query)
    if 'platform' in processing_query.keys():
        rag_query = processing_query['platform']['relative_url']
        print("########################",rag_query) 
    else:
        rag_query = processing_query['user']
    docs = docstore.retrieve_data(query=rag_query,number_of_documents=3)

    print(docs['documents'])
    sys = bot.system_prompt
    bot.system_prompt = bot.system_prompt.replace('{documents}',str(docs['documents']))
    print(bot.system_prompt)
    #query = "TimeStamp : " + get_curent_datetime() + "\n" + "User Input : " + query
    results = bot.generate_response(query,chat_history)
    bot.system_prompt = sys
    return results

with gr.Blocks() as demo:

    chatbot = gr.Chatbot(label='Contlos', height=600)
    msg = gr.Textbox()
    clear = gr.ClearButton([msg, chatbot])
    
    msg.submit(chat_session, [msg, chatbot], [msg, chatbot])
    #print(olivia.conversation_history)

demo.launch()

