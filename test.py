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
bpe.load_model('jesenlik')
encode = bpe.encode("i am a comedian")
print(encode)
decode = bpe.decode(encode)
print(decode)




