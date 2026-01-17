from helper import get_words_in_text 
import os
import json

def count_dif_links_content(text, domain):
    count = 0
    tokens = text.lower().split()
    for token in tokens:
        if token.startswith('http://') or token.startswith('https://') or token.startswith('www.'):
            if domain not in token:
                count += 1
    return count



def generate_obj(item):

    total_links = count_dif_links_content(item['content'], item['domain'])
    palavras_texto = get_words_in_text(item['content'])
    palavras_subject = get_words_in_text(item['subject'])
    return {
        'total_links': total_links,
        'total_words_content': len(palavras_texto),
        'total_words_subject': len(palavras_subject),
        'palavras': palavras_texto + palavras_subject
    }



try:
    
    caminho  = 'raw_data/'
    palavras_tf_idf = []
    items = []

    for arquivojson in os.listdir(caminho):
        
        file = os.path.join(caminho, arquivojson)
        class_name = arquivojson.replace('_cleaned.json', '')

        with open(file, 'r') as f:
            data = json.load(f)
            for item in data:
                obj = generate_obj(item)
                palavras_tf_idf += obj['palavras']
                item['total_links'] = obj['total_links']
                item['total_words_content'] = obj['total_words_content']
                item['total_words_subject'] = obj['total_words_subject']
                item['class'] = class_name
                item['palavras'] = obj['palavras']
                items.append(item)

    
    with open('models/words.json', 'w') as f:
        unique_words = list(set(palavras_tf_idf))
        json.dump(unique_words, f)

    for item in items:
        vetor = [0] * len(unique_words)
        for palavra in item['palavras']:
            if palavra in unique_words:
                index = unique_words.index(palavra)
                vetor[index] += 1
        
        item['vetor'] = vetor
    
    vetores_classify = {
        'spam': [],
        'not_spam': []
    }

    for item in items:
        item_class = item['class']
        vetores_classify[item_class].append(item['vetor'])

    for class_name, vetores in vetores_classify.items():
        with open(f'dataset_vetores/{class_name}.json', 'w') as f:
            json.dump(vetores, f)


except Exception as e:
    print(f"erro: {e}")

    

