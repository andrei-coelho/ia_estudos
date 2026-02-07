import json
import helper
import math
import random

# APENAS ORGANIZANDO O DATASET INICIAL 

def gerar_dataset_formatado():
    with open('../../dummy_datas/produtos_compilados.json', 'r') as file:
        
        lista = json.loads(file.read())
        
        palavras = []
        data = []
        
        for item in lista:
            data.append(helper.remover_acentos(item['descricao']))
            palavras += helper.get_words_in_text(item['descricao'])

    palavras_unicas = list(set(palavras))

    with open('palavras_unicas.json', 'w') as f1:
        json.dump(palavras_unicas, f1, ensure_ascii=False)
        f1.close()

    with open('data_set.json', 'w') as f2:
        json.dump(data, f2, ensure_ascii=False)
        f2.close()


def gerar_idf(dataset, dicionario):
    
    df = {}
    totaldocs = len(dataset)
    
    for data in dataset:
        termos = helper.get_words_in_text(data)
        for termo in set(termos):
            if termo not in df:
                df[termo] = 0
            df[termo] += 1

    idf = {}
    for termo in dicionario:
        idf[termo] = math.log( (totaldocs + 1) / (df.get(termo, 0) + 1) )

    return idf


def vetorizar_dataset():

    dataset    = []
    dicionario = []

    with open('data_set.json', 'r') as file:
        dataset = json.loads(file.read())

    with open('palavras_unicas.json', 'r') as file:
        dicionario = json.loads(file.read())

    idf = gerar_idf(dataset, dicionario)

    vetores = []
    ctermos = {}

    for item in dicionario:
        ctermos[item] = 0

    tovector = []

    for data in dataset:
        tcterm = ctermos.copy() 
        termos = helper.get_words_in_text(data)
        for term in termos:
            if term in dicionario:
                tcterm[term] += 1
        tovector.append(tcterm)

    for vect in tovector:
        vector = []
        for termo in dicionario:
            v = 0
            if vect[termo] > 0: 
                v = vect[termo] * idf[termo] 
            vector.append(v)
        vetores.append(vector)

    random.shuffle(vetores)

    with open('modelo.json', 'w') as file:
        json.dump(vetores, file, ensure_ascii=False)


vetorizar_dataset()
