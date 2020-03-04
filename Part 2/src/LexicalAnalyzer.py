import re
import os
import sys
import spacy

sys.path.append(os.path.abspath(os.path.join('..')))


class LexicalAnalyzer:
    def __init__(self, input_path: str):
        with open(input_path, 'r', encoding='utf-8') as file:
            input_text = file.read().replace('\n', '')
            nlp = spacy.load('pt_core_news_sm')
        
        self._doc = nlp(input_text)

    def _convert_part_of_speech_spacy_to_portuguese(self, spacy_pos: str) -> str:
        if spacy_pos == 'PROPN':
            part_of_speech = 'nome próprio'
        elif spacy_pos == 'PRON':
            part_of_speech = 'pronome'
        elif spacy_pos == 'ADJ':
            part_of_speech = 'adjetivo'
        elif spacy_pos == 'NOUN':
            part_of_speech = 'substantivo'
        elif spacy_pos == 'VERB':
            part_of_speech = 'verbo'
        elif spacy_pos == 'AUX':
            part_of_speech = 'verbo auxiliar' 
        elif spacy_pos == 'DET':
            part_of_speech = 'determinante'
        elif spacy_pos in ['CONJ', 'CCONJ', 'SCONJ']:
            part_of_speech = 'conjunção'
        elif spacy_pos == 'INTJ':
            part_of_speech = 'interjeição'
        elif spacy_pos == 'ADP':
            part_of_speech = 'preposição'
        elif spacy_pos == 'PUNCT':
            part_of_speech = 'pontuação'
        elif spacy_pos == 'SYM':
            part_of_speech = 'símbolo'
        elif spacy_pos == 'NUM':
            part_of_speech = 'numeral'
        else:
            part_of_speech = 'desconhecido'

        return part_of_speech
    
    def create_table(self) -> list:
        table = []
        
        for element in self._doc:
            table.append({'token': element.orth_, 'class': self._convert_part_of_speech_spacy_to_portuguese(element.pos_)})
        
        return table