import pytextrank
import spacy
import pandas as pd


def text_rank(title): #text rank 알고리즘 사용 
    nlp = spacy.load('en_core_web_sm')
    nlp.add_pipe("textrank")
    doc = nlp(title)
    for phrase in doc._.phrases:
        rank = print('{:.4f} {}'.format(phrase.rank, phrase.text),)
        rank_text = print(phrase.chunks)
    return rank, rank_text
