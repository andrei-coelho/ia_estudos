from util.jsoni import decode,encode
import random

precos = {
    "sapatenis":{
        "min":89,
        "max":199
    },
    "botas":{
        "min":199,
        "max":450
    },
    "chuteiras":{
        "min":120,
        "max":350
    },
    "chinelos":{
        "min":19,
        "max":100
    },
    "tenis":{
        "min":150,
        "max":600
    }
}


def save_edited_products(produtos:list[dict]):
    with open('dummy_datas/produtos_compilados_preco.json', 'w') as arquivo:
        arquivo.write(encode(produtos))
        arquivo.close()


def add_preco():
    produtos = []
    with open('dummy_datas/produtos_compilados.json', 'r') as arquivo:
        produtos = decode(arquivo.read())
        for produto in produtos:
            preco  = random.randrange(precos[produto['categoria']]['min'], precos[produto['categoria']]['max'])
            cents  = random.choice([0,50,99])
            preco += (cents/100)
            produto['preco'] = preco
    save_edited_products(produtos)
        