
from loading_data import carregar_modelo

produto_avaliar = {"id": 939, "urli": "https://www.netshoes.com.br/p/tenis-new-balance-480-low-masculino-bege+branco-39V-0297-396", "descricao": "Tênis New Balance 480 Low Masculino - Bege+Branco", "avaliacao": 5.0, "categoria": 4, "preco": 180.5}

pesos = carregar_modelo()

def avaliar_produto(produto, pesos):
    preco_previsto = pesos["bias"] + (pesos["avaliacao"] * produto["avaliacao"]) + (pesos["categoria"] * produto["categoria"])
    return preco_previsto


print("Preço previsto para o produto:")
print(
    avaliar_produto(produto_avaliar, pesos)
)

print("===================================================")
print("Preço real do produto:")
print(produto_avaliar["preco"])