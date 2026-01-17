import json

def open_model():
    models = {
        "features_dados": {},
        "words": [],
        "vetores":[],
        "rotulos": []
    }

    with open('models/rotulos.json', 'r') as f:
        rotulos = json.load(f)
        models['rotulos'] = rotulos
    
    for rotulo in rotulos:
        with open(f"models/features_dados_{rotulo}.json", 'r') as f:
            features_dados = json.load(f)
            models['features_dados'][rotulo] = features_dados 

    with open('models/words.json', 'r') as f:
        words = json.load(f)
        models['words'] = words
    
    with open('models/naive_bayes_gaussian_model.json', 'r') as f:
        vetores = json.load(f)
        models['vetores'] = vetores


    return models


def classificar(vetor):

    models = open_model()
    features_dados_all = models['features_dados']
    vetores = models['vetores']
    rotulos = models['rotulos']
    rotulos_unicos = list(set(rotulos))

    vetores_model_list = { }

    for classe in rotulos_unicos:
        vetores_model_list[classe] = []

    for i in range(len(vetores)):
        classe = rotulos[i]
        vetores_model_list[classe].append(vetores[i])


    probabilidades = {}

    for classe in rotulos_unicos:
        
        vetores_model  = vetores_model_list[classe]
        features_dados = features_dados_all[classe]

        for item_model in vetores_model:
            probabilidade_class = 1.0

            for i in range(len(vetor)):

                media = features_dados[i]['media']
                variancia = features_dados[i]['variancia']
                desvio_padrao = features_dados[i]['desvio_padrao']
                x = vetor[i]

                if variancia == 0:
                    continue

                expoente = -((x - media) ** 2) / (2 * variancia)
                coeficiente = 1 / ((2 * 3.1416 * variancia) ** 0.5)
                probabilidade_feature = coeficiente * (2.71828 ** expoente)

                probabilidade_class *= probabilidade_feature

            probabilidades[classe] = probabilidade_class

        categoria_classificada = max(probabilidades, key=probabilidades.get)

    return categoria_classificada, probabilidades