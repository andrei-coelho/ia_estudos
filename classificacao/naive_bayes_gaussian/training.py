import json
from helper import multiply_vetor, multiplicar_por_escalar, subtracao_vetor, calcular_modulo_vetor
import os
from classify import classificar


def ortonormalizacao_gram_shimit(matriz, rotulos, eps=1e-8):
    base = []

    for v in matriz:

        w = v.copy()

        for q in base:
            alpha = multiply_vetor(w, q)
            w = subtracao_vetor(w, multiplicar_por_escalar(alpha, q))

        norma = calcular_modulo_vetor(w)

        if norma > eps:
            w = [comp / norma for comp in w]
            base.append(w)
        else:
            del rotulos[matriz.index(v)]

    return base, rotulos


def generate_index_average_feature(rotulo):
    
    try:
        with open('models/naive_bayes_gaussian_model.json', 'r') as f:
            items_data = json.load(f)
    except Exception as e:
        raise Exception(f"Error loading vetores.json: {e}")
    
    try:
        with open('models/rotulos.json', 'r') as f:
            rotulos = json.load(f)
    except Exception as e:
        raise Exception(f"Error loading vetores.json: {e}")


    total_items = 0
    average_features = []
    sum_features = []
    variancias = []
    items = []

    index = 0
    
    for i in items_data:
        if rotulos[index] == rotulo:
            total_items += 1
            items.append(i)
        index += 1
    
    for item in items:
        for feature in item:
            if len(sum_features) < len(item):
                sum_features.append(feature)
            else:
                sum_features[len(average_features)] += feature

    for sum_feature in sum_features:
        average_features.append(sum_feature / total_items)
    
    for item in items:
        for i in range(len(item)):
            diferenca = item[i] - average_features[i]
            if len(variancias) < len(item):
                variancias.append(diferenca * diferenca)
            else:
                variancias[i] += diferenca * diferenca

    features_dados = []

    for i in range(len(variancias)):
        variancia = variancias[i] / total_items
        desvio_padrao = variancia ** 0.5
        features_dados.append({
            'media': average_features[i],
            'variancia': variancia,
            'desvio_padrao': desvio_padrao
        })

    with open(f"models/features_dados_{rotulo}.json", 'w') as f:
        json.dump(features_dados, f)


def training_naive_bayes_gaussian():
    try:
        caminho = 'dataset_vetores/'

        print("Iniciando treinamento...")
        print("Gerando o modelo Naive Bayes Gaussian...")
        matriz  = []
        testes  = []
        rotulos = []

        for arquivojson in os.listdir(caminho):
            
            categoria = arquivojson.replace('.json', '')
            arquivo = os.path.join(caminho, arquivojson)
            
            with open(arquivo, 'r') as f:
                data = f.readlines()
                jdata = [json.loads(item) for item in data][0]
                data_training = jdata[:int(len(jdata) * 0.8)]
                rotulos += [categoria] * len(data_training)
                testes.append({
                    'categoria': categoria,
                    'total': len(jdata),
                    'treinamento': len(data_training),
                    'teste': len(jdata) - len(data_training),
                    'data': jdata[int(len(jdata) * 0.8):]
                })
                matriz += data_training

        matriz, rotulos = ortonormalizacao_gram_shimit(matriz, rotulos)

        with open('models/naive_bayes_gaussian_model.json', 'w') as f:
            json.dump(matriz, f)

        with open('models/rotulos.json', 'w') as f:
            json.dump(rotulos, f)
    
        print("Modelo Naive Bayes Gaussian gerado com sucesso.")
        print("Gerando índices médios das features...")

        rotulos_unicos = set(rotulos)
        
        for r in rotulos_unicos:
            generate_index_average_feature(r)
            
        print("Índices médios das features gerados com sucesso.")
        print("Iniciando testes...")
       
        total_acertos = 0
        total_testes = 0
        for teste in testes:
            # print(teste)
            categoria = teste['categoria']
            data_teste = teste['data']
            acertos = 0

            for item in data_teste:
                classificada, probabilidades = classificar(item)
                if classificada == categoria:
                    acertos += 1

            total_acertos += acertos
            total_testes += len(data_teste)
            print(f"Categoria: {categoria} - Acertos: {acertos} de {len(data_teste)} testes.")

        taxa_acerto = (total_acertos / total_testes) * 100 if total_testes > 0 else 0
        print(f"Taxa de acerto total: {taxa_acerto:.2f}% ({total_acertos}/{total_testes})")

    except Exception as e:
        print(f"Erro durante o treinamento do Naive Bayes Gaussian: {e}")


training_naive_bayes_gaussian()