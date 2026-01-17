import hashlib
import math
import os
import json
import re

import unicodedata

def remover_acentos(texto):
    processado = unicodedata.normalize('NFD', texto)
    return "".join(c for c in processado if unicodedata.category(c) != 'Mn')

def limpar_e_anonimizar_email(texto: str) -> str:

    texto = texto.encode('ascii', 'ignore').decode()

    regras = [
        # -----------------------------
        # 1. CSS SOLTO / MEDIA QUERIES
        # -----------------------------
        (r'@media[^{]+\{[\s\S]*?\}', ''),
        (r'(^|\n)\s*[.#]?[a-zA-Z0-9_\- >:#\[\]="\']+\s*\{[\s\S]*?\}', ''),
        (r'\b[a-zA-Z\-]+\s*:\s*[^;\n]+;', ''),

        # -----------------------------
        # 2. HTML RESIDUAL
        # -----------------------------
        (r'<[^>]+>', ' '),

        # -----------------------------
        # 3. ANONIMIZAÇÃO
        # -----------------------------

        # Emails genéricos (opcional, mas deixei desligado por padrão)
        (r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b', ' [EMAIL] '),

         # NORMALIZAÇÃO SEMÂNTICA
        (r'\b(19|20)\d{2}\b', ' [YEAR] '),
        (r'\b\d+\s?%\b', ' [PERCENT] '),
        (r'(?:<\s*)?(r\$|\$)\s?\d{1,3}(?:[.,]\d{3})*(?:[.,]\d+)?\b', ' [MONEY] '),
        (r'\b\d{2,}\s?(BRL|USD|EUR)\b', ' [MONEY] '),
        (r'\b(at|por|apenas|only|from|starting)\s+\d{2,}\b', ' [MONEY] '),
        (r'\b(code|codigo|cdigo)\s*:?\s+(?=[A-Za-z0-9\-_]{4,})(?=.*[A-Za-z])(?=.*\d)[A-Za-z0-9\-_]+\b', ' [CODE] '),
        (r'\b\d+\s?(h|horas?|dias?|meses?|minutos?)\b', ' [TIME] '),

        # CPF
        (r'\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b', '[CPF] '),

        # CNPJ
        (r'\b\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}\b', ' [CNPJ] '),

        # Telefones BR
        (r'\(?\d{2}\)?\s?\d{4,5}-?\d{4}', ' [PHONE] '),

        # -----------------------------
        # 4. LIMPEZA FINAL
        # -----------------------------
        (r'(\r?\n){3,}', '\n\n'),
        (r'\s{2,}', ' ')
    ]

    for pattern, repl in regras:
        texto = re.sub(pattern, repl, texto, flags=re.I)

    return texto.strip()

def get_words_in_text(text):
    tokens = text.lower().split()
    palavras_validas = []

    padrao = re.compile(r"(\[[a-z_]+\]|[a-záàâãéêíóôõúç]{4,})", re.I)

    for token in tokens:
        if padrao.fullmatch(token):
            if token.startswith('['):
                palavras_validas.append(token.strip('[]'))
            else:
                palavras_validas.append(remover_acentos(token))

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

    data = get_json_file('models/words.json')
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