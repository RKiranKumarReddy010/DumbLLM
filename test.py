from DataScrapper._wikiscrapper import Scrapper
from Preprocessing._datacleaner import Processor
from Encoder._encoding import BPE

scr = Scrapper()
scr.langchain_get_data()

preprocess = Processor()
preprocess.run()

with open('./Data/fData.txt',"r") as file:
    data = file.read()

bpe = BPE(100)
bpe.fit(data)
bpe.save_model('anthony_jesenlik')

bpe.load_model('anthony_jesenlik')
encoded_text = bpe.encode("Hello there, it's saiman says")
print(encoded_text)
decoded_text = bpe.decode(encoded_text)
print(decoded_text)




