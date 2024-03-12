import chromadb
import pandas as pd
from rich import print

class RAG:
    def __init__(self,file_name):

        self.file_name = file_name
        self.chroma_client = chromadb.Client()
        #self.chroma_client.delete_collection("contlo2")
        self.collection = None
        
    def create_collection(self):
        df = pd.read_csv('onboarding.csv')
        urls_description = df['text'].to_list()
        ids = [str(x) for x in df.index.to_list()]
        self.collection = self.chroma_client.create_collection(name="contlo_onboarding",metadata={"hnsw:space": "cosine"})
        self.collection.add(
            documents=urls_description,
            ids = ids
            )
        #return self.collection
    
    def retrieve_data(self,query,number_of_documents):
        results = self.collection.query(
                    query_texts=[query],
                    n_results=number_of_documents)   
        return results

# docstore = RAG("final.csv")
# docstore.create_collection()

# while(True):
#     query = input("Enter the query : ")
#     docs = docstore.retrieve_data(query=query,number_of_documents=2)
#     print(docs)