import json
from helper import calcular_modulo_vetor, get_words_in_text, vetorizar_tf_idf

def rows_to_columns(matriz):

    if not matriz:
        return []
        
    num_columns = len(matriz[0])
    columns = []
    for i in range(num_columns):
        column = [row[i] for row in matriz]
        columns.append(column)
        
    return columns



def get_raw_data():
    try:
        with open('../../dummy_datas/produtos_compilados_preco.json', 'r') as file:
            data = file.readlines()
            jdata = [json.loads(item) for item in data]
            return jdata[0]
    except Exception as e:
        print(f"An error occurred: {e}")


def transform_dataset_in_vector(data_list):

    newItems  = []
    categoria = data_list[0]['categoria']
    print(f"Transforming data for category: {categoria}")
    lenvect = 0
    for item in data_list:
        vetor = vetorizar_tf_idf(item['descricao'])
        if lenvect == 0:
            lenvect = len(vetor)
        
        if len(vetor) != lenvect:
            print(f"Vector length mismatch for item: {item}. Expected length: {lenvect}, got: {len(vetor)}")
            continue

        if vetor is not None and calcular_modulo_vetor(vetor) > 0:
            newItems.append(vetor)
        else:
            print(f"Failed to vectorize item: {item}")

    print("tamanho dos vetores: " + str(lenvect))

    return newItems


def transform_data():

    data_list = get_raw_data()
    categories = {}

    for item in data_list:
        category = item['categoria']
        if category not in categories:
            categories[category] = []
        categories[category].append(item)
        
    # criar word list do vetor
    palavras = set()
    for item in data_list:
        words = get_words_in_text(item['descricao'])
        for palavra in words:
            palavras.add(palavra) 

    try:
        palavras = list(palavras)
        with open(f'modelos_subespaces/words.json', 'w') as file:
            json.dump(palavras, file)
    except Exception as e:
        print(f"An error occurred while writing to file: {e}")

    for category, items in categories.items():
        print(f"Processing category: {category} with {len(items)} items")
        data_vectors = transform_dataset_in_vector(items)
        try:
            with open(f'dataset_vector/{category}.json', 'w') as file:
                json.dump([list(vec) for vec in data_vectors], file)
        except Exception as e:
            print(f"An error occurred while writing to file: {e}")

transform_data()