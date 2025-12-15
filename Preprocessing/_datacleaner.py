import re
import os 
from dotenv import load_dotenv

load_dotenv()

class Processor:
    def __init__(self):
        ufdata = os.getenv("Unfiltered_DATAPATH")
        fdata = os.getenv("Filtered_DATAPATH")
        self.ufdata = ufdata
        self.fdata = fdata
        pass

    def run(self):
        """Run the regex pattern to filter or preprocess the data for preparing the data for training the model"""
        data = Processor.reader(self=self, data_path=self.ufdata)
        clean_text = re.sub(r'\[.*?\]|\(.*?\)', ' ', data) # remove the brackets
        clean_text = re.sub(r'[^A-Za-z0-9\s.,?!]', ' ', clean_text) # remove the symbols excepts letters ,nums, .!? symbols.
        clean_text = re.sub(r'\s+', ' ', clean_text).strip() # merging the corpus
        clean_text = re.sub(r'\+?\d[\d\s().-]{7,}\d', ' ', clean_text) # remove the phonenumber
        clean_text = re.sub(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', ' ', clean_text) # remove the email id
        clean_text = re.sub(r'http[s]?://\S+|www\.\S+', ' ', clean_text) # remove the web url
        ### Now we get a clean text  ###
        try:
            with open(self.fdata,'w') as file:
                file.write(clean_text)
            return True
        except Exception as e:
            print(e)
            return False

    def reader(self, data_path):
        """Read the content from the file"""
        try:
            with open(data_path, "r") as file:
                data = file.read()
            return data
        except Exception as e:
            print(e)
            return "Not able to read !!!"