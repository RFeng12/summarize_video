from keybert import KeyBERT
import nltk
from rake_nltk import Rake
from sentence_transformers import SentenceTransformer
import funct_paragrapher
import pandas as pd 
import spacy 
import requests 
from bs4 import BeautifulSoup
nlp = spacy.load("en_core_web_sm")
pd.set_option("display.max_rows", 200)


import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context


nltk.download('stopwords')

filepath = ""
with open("filepath.txt") as file:
    for line in file.readlines():
        filepath = line

kw_model = KeyBERT()
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
r = Rake()


 
def get_keyword_string(doc):
    keywords = []
    r.extract_keywords_from_text(doc)

    ner = nlp(doc)
 
    for ent in ner.ents:
        print("NER: ", ent.text, ent.label_)


    phrases = r.get_ranked_phrases()

    keywords.append(phrases[0])
    
    return keywords
    '''
    keywords = kw_model.extract_keywords(doc)

    lines = ""
    for pair in keywords:
        word = pair[0]
        lines += word + ' '

    is_noun = lambda pos: pos[:2] == 'NN'
    tokenized = nltk.word_tokenize(lines)
    nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)] 
    
    if len(nouns) == 0:
        lines = doc
        is_noun = lambda pos: pos[:2] == 'NN'
        tokenized = nltk.word_tokenize(lines)
        nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)] 
        if len(nouns) == 0:
            return "noimagefound"

    return nouns
    '''