import os
import json
import tqdm
import unicodedata
from collections import defaultdict, Counter
import re

class BPE:
    def __init__(self, num_merges):
        self.num_merges = num_merges
        self.vocabs = {}
        self.merges = []
        pass

    def get_vocabs(self, text:str):
        vocab = defaultdict(int)
        for word in text.split():
            vocab[" ".join(list(word))+ " </w>"] += 1
        return vocab
    
    def get_pair_stats(self):
        pairs = defaultdict(int)
        for word, freq in self.vocabs.items():
            symbols =  word.split()
            for i in range(len(symbols)-1):
                pairs[(symbols[i], symbols[i+1])] += freq
        return pairs
    
    def merge_vocab(self, pair):
        pattern = re.compile(r"(?<!\S)" + re.escape(" ".join(pair)) + r"(?!\S)")
        new_vocab = {}
        for word in self.vocabs:
            next_word = pattern.sub("".join(pair), word)
            new_vocab[next_word] = self.vocabs[word]
        self.vocabs = new_vocab

    def fit(self,text):
        self.vocabs = self.get_vocabs(text)

        for _ in range(self.num_merges):
            pairs = self.get_pair_stats()
            if not pairs:
                break
            best_pairs = max(pairs, key=pairs.get)
            self.merges.append(best_pairs)
            self.merge_vocab(best_pairs)

    def encode(self, word):
        token = list(word) + ["</w>"]
        for a ,b in self.merges:
            i = 0
            while i < len(token) - 1:
                if token[i] == a  and token[i+1] == b:
                    token[i:i+2] = [a+b]
                else:
                    i+=1
        return token

    def decode(self, token):
        word = "".join(token)
        return word.replace("</w>","")
    
    def save_model(self, file:str):
        if not os.path.isdir('models'):
            os.mkdir('models')
        try:
            with open(f'models/{file}.json', 'w') as file:
                json.dump(
                    {
                        "num_merges":self.num_merges,
                        "merges": self.merges
                    },
                    file
                )
        except Exception as e:
            print(e)
    
    def load_model(self, file:str):
        if not os.path.isdir('models'):
            os.mkdir('models')
        try:
            with open(f'models/{file}.json', 'r') as file:
                data = json.load(file)
                self.num_merges = data["num_merges"]
                self.merges = data["merges"]
        except Exception as e:
            print(e)

        




