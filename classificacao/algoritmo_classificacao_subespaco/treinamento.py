import json
import os
from helper import multiply_vetor, multiplicar_por_escalar, subtracao_vetor, calcular_modulo_vetor
from classificador import classificar

def get_data_from_file(file):
    try:
        with open(file, 'r') as f:
            data = f.readlines()
            jdata = [json.loads(item) for item in data]
            return jdata
        
    except Exception as e:
        print(f"An error occurred: {e}")



def ortonormalizacao_gram_shimit(matriz, eps=1e-8):
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

    return base


def train_subspace_model():

    caminho = 'dataset_vector/'
    testes = []

    print("Iniciando treinamento...")

    for arquivojson in os.listdir(caminho):

        if(arquivojson in 'words.json'):
            continue

        categoria = arquivojson.replace('.json', '')
        arquivo = os.path.join(caminho, arquivojson)
        data = get_data_from_file(arquivo)[0]
        total = len(data)
        data_training = data[:int(total * 0.8)]
        data_test = data[int(total * 0.8):]
        result = ortonormalizacao_gram_shimit(data_training)
        
        print(f"Treinamento da categoria: {categoria} concluído. Total de vetores treinados: {len(result)}")

        testes.append({
            'categoria': categoria,
            'total': total,
            'treinamento': len(data_training),
            'teste': len(data_test),
            'data': data_test,
            'acertos': 0,
            'erros': 0,
            'projecoes': {}
        })

        try:
            with open(f'modelos_subespaces/{arquivojson}', 'w') as file:
                json.dump([list(v) for v in result], file)
        except Exception as e:
            print(f"Erro: {e}")

    print("Iniciando testes de classificação...")
    for teste in testes:
        print("Testando categoria:", teste['categoria'])
        for vetor_teste in teste['data']:
            categoria_classificada, projecoes = classificar(vetor_teste, transformar=False)
            teste['projecoes'] = projecoes
            if categoria_classificada == teste['categoria']:
                teste['acertos'] += 1
            else:
                teste['erros'] += 1
    
    print("Resultados dos testes:")
    for teste in testes:
        total_testes = teste['acertos'] + teste['erros']
        taxa_acerto = (teste['acertos'] / total_testes) * 100 if total_testes > 0 else 0
        print(f"Categoria: {teste['categoria']}, Acertos: {teste['acertos']}, Erros: {teste['erros']}, Taxa de Acerto: {taxa_acerto:.2f}%")
        print(f"Projeções: {teste['projecoes']}")


train_subspace_model()