import math
import os
import json


def escalar_pela_variancia(data):

    total_rows = len(data)
    total_fields = len(data[0])

    variancias = [0.0] * total_fields

    for j in range(total_fields):
        soma = 0.0
        for i in range(0, total_rows):
            soma += data[i][j] ** 2 
        variancias[j] = soma / total_rows

    desvios_padrao = [math.sqrt(v) for v in variancias]

    newData = []

    for i in range(0, total_rows):
        temp = []
        for j in range(total_fields):
            if desvios_padrao[j] != 0:
                temp.append(data[i][j] / desvios_padrao[j])
            else:
                temp.append(0)
        newData.append(temp)

    return newData, desvios_padrao


def normalizacao_z_score(data):

    total_features = len(data[0])
    total_rows = len(data)

    medias = [0.0] * total_features

    for j in range(total_features):
        soma = 0.0
        for i in range(0, total_rows):
            soma += data[i][j]
        medias[j] =  soma / total_rows

    newData = []

    for i in range(0, total_rows):
        temp = []
        for j in range(total_features):
            temp.append(data[i][j] - medias[j])
        newData.append(temp)

    data, desvios_padrao = escalar_pela_variancia(newData)

    return data, desvios_padrao, medias



caminho = 'dataset_vetores'

vetores_normalizados = []
rotulos_vetores      = {}
vetores_agrupados    = []

classes = {}
x = 0

for file in os.listdir(caminho):
    
    classename = file.split('.')[0]
    classes[classename] = x
    x += 1

    file_path = os.path.join(caminho, file)
    
    with open(file_path, 'r') as f:
        vetores = json.load(f)
    rotulos_vetores[classename] = [classes[classename]] * len(vetores)
    vetores_agrupados += vetores

vetores_normalizados, desvios_padrao, medias  = normalizacao_z_score(vetores_agrupados)
    
    
with open('model/dataset_normalizado.json', 'w') as f:
    json.dump(vetores_normalizados, f)

with open('model/model.json', 'w') as f:
    json.dump({
        "rotulos": rotulos_vetores,
        "bias": {},
        "escalar": {
            "medias":medias,
            "desvios_padrao":desvios_padrao
        }
    }, f)