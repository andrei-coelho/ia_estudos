from helper import somar_vetor, multiplicar_por_escalar, vetorizar_tf_idf, multiply_vetor, calcular_modulo_vetor, subtracao_vetor
import os 
import json

def get_all_models():
    modelos = []
    try:
        caminho = 'modelos_subespaces/'
        for arquivojson in os.listdir(caminho):
            if(arquivojson in 'words.json'):
                continue
            categoria = arquivojson.replace('.json', '')
            arquivo = os.path.join(caminho, arquivojson)
            with open(arquivo, 'r') as f:
                data = f.readlines()
                jdata = [json.loads(item) for item in data]
                modelos.append({
                    'categoria': categoria,
                    'model': jdata
                })
        return modelos
    except Exception as e:
        print(f"erro: {e}")


def classificar(input, transformar=True):

    modelos = get_all_models()
    
    x = vetorizar_tf_idf(input) if transformar else input
    projecoes = {}
    
    for modelo in modelos:
        alphas = []
        matriz = modelo['model'][0]
        for v in matriz:
            alpha = multiply_vetor(x, v)
            alphas.append(alpha)

        sum_vetores = []
        for i in range(len(matriz)):
            ax = alphas[i]
            vx = matriz[i]
            sum_vetores.append(multiplicar_por_escalar(ax, vx))

        y = []

        for vsum in sum_vetores:
            y = somar_vetor(y, vsum) if y else vsum

        projecao = calcular_modulo_vetor(subtracao_vetor(x, y))
        projecoes[modelo['categoria']] = projecao

    categoria_classificada = min(projecoes, key=projecoes.get)
    
    return categoria_classificada, projecoes


get_all_models()