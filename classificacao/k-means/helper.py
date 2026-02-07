import hashlib
import math
import os
import json
import re

import unicodedata

def remover_acentos(texto):
    processado = unicodedata.normalize('NFD', texto)
    return "".join(c for c in processado if unicodedata.category(c) != 'Mn')


def get_words_in_text(text):
    
    text = remover_acentos(text)
    words = text.strip().lower().split()
    padrao = r"[^\d\s:\-0-9\+]+"
    palavras_validas = []

    for word in words:
        if(len(word) < 4):
            continue 
        if re.fullmatch(padrao, word):
            palavras_validas.append(word)

    return palavras_validas


def get_json_file(caminho):
    try:
        with open(caminho, 'r') as file:
            data = file.readlines()
            jdata = [json.loads(item) for item in data]
            return jdata
    except Exception as e:
        print(f"An error occurred: {e}")
        return None



def calcular_modulo_vetor(vetor):
    return math.sqrt(sum(v * v for v in vetor))

def distancia_eclidiana(vetorA, vetorB):
    vetor_diferenca = [(a - b) for a, b in zip(vetorA, vetorB)]
    return calcular_modulo_vetor(vetor_diferenca)



