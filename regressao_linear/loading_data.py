import json

def salvar_modelo(modelo):
    with open('./modelo.json', 'w') as arquivo:
        json.dump(modelo, arquivo)

def salvar_dicionario_categoria(dicionario_categoria):
    with open('../dummy_datas/dicionario_categoria.json', 'w') as arquivo:
        json.dump(dicionario_categoria, arquivo)

def normalizacao(produtos):
    iniid_categoria = 1
    dicionario_categoria = {}

    categorias = {produto["categoria"] for produto in produtos}

    for categoria in categorias:
        dicionario_categoria[categoria] = iniid_categoria
        iniid_categoria += 1

    salvar_dicionario_categoria(dicionario_categoria)

    array_normalizado = []
    for produto in produtos:
        produto_normalizado = {
            "avaliacao": produto["avaliacao"],
            "categoria": dicionario_categoria[produto["categoria"]],
            "preco": produto["preco"]
        }
        array_normalizado.append(produto_normalizado)

    return array_normalizado

def load_data():

    with open('../dummy_datas/produtos_compilados_preco.json', 'r') as file:
        produtos_compilados_precos = json.load(file)
        return normalizacao(produtos_compilados_precos)
    
