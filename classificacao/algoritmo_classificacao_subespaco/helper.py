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
    
    words = text.strip().lower().split()
    padrao = r"[^\d\s:\-0-9\+]+"
    palavras_validas = []
    for word in words:
        if(len(word) < 4):
            continue 
        if re.fullmatch(padrao, word):
            palavras_validas.append(remover_acentos(word))

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


def vetorizar_tf_idf(texto):

    data = get_json_file('modelos_subespaces/words.json')
    if data is None:
        return None
    palavras_vetor = data[0]
    palavras_texto = get_words_in_text(texto)
    vetor = [0] * len(palavras_vetor)

    for i, palavra in enumerate(palavras_vetor):
        if palavra in palavras_texto:
            vetor[i] += 1

    return vetor 
    


def aumentar_densidade_feature_e_transmormar_em_vetor(val, dim=200):
    val_encode = val.strip().lower().encode("utf-8")
    seed = int(hashlib.sha256(val_encode).hexdigest(), 16)

    vetor = [0.0] * dim

    a = 1664525
    c = 1013904223
    m = 2**32

    atual = seed % m
    for i in range(dim):
        atual = (a * atual + c) % m
        vetor[i] = (atual / m) * 2.0 - 1.0

    return vetor


def calcular_modulo_vetor(vetor):
    return math.sqrt(sum(v * v for v in vetor))


def somar_vetor(a, b):
    return [x + y for x, y in zip(a, b)]


def subtracao_vetor(a, b):
    return [x - y for x, y in zip(a, b)]


def multiply_vetor(a, b):
    if len(a) != len(b):
        print("Vetor A: {}".format(a))
        print("Vetor B: {}".format(b))
        raise ValueError("Vetores devem ter o mesmo tamanho. Tamnho a: {}, Tamanho b: {}".format(len(a), len(b)))
    return sum(x * y for x, y in zip(a, b))


def multiplicar_por_escalar(escalar, vetor):
    return [escalar * x for x in vetor]