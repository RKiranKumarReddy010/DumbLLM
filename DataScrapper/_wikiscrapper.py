#Importing all required dependencies
import wikipedia
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_transformers import Html2TextTransformer
import os

#Load key- value pairs from .env
load_dotenv()

#Create a scrapper class
class Scrapper:
    def __init__(self):
        #get data from the en file
        uf = os.getenv('Unfiltered_DATAPATH')
        DATA = os.getenv('DATA')
        self.path = DATA
        self.uf = uf
        pass

    def get_data(self):
        response = requests.get(self.path)
        html_content = response.content
        #create a object for bs4 html parser
        text = BeautifulSoup(html_content,"html.parser")
        try:
            with open(self.uf,"w") as file:
                file.write(str(text))    
            return True
        except Exception as e:
            print(e)
            return False

    def langchain_get_data(self):
        loader = WebBaseLoader(self.path)
        docs = loader.load()
        html2text = Html2TextTransformer()
        transformed_docs = html2text.transform_documents(docs)
        try:
            with open(self.uf,"w") as file:
                file.write(str(transformed_docs))    
            return True
        except Exception as e:
            print(e)
            return False





