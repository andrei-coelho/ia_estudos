from loading_data import load_data, salvar_modelo
import random

produtos = load_data()
"""
produtos = [ 
    {'avaliacao': 3.33, 'categoria': 1, 'preco': 249.0}, 
    {'avaliacao': 4.86, 'categoria': 1, 'preco': 357.99}, 
    {'avaliacao': 4.33, 'categoria': 1, 'preco': 212.0}, 
    {'avaliacao': 4.0, 'categoria': 1, 'preco': 237.5}, 
    {'avaliacao': 4.19, 'categoria': 1, 'preco': 421.5} 
]
"""

pesos = {
    "bias": random.uniform(-1, 1),
    "avaliacao": random.uniform(-1, 1),
    "categoria": random.uniform(-1, 1),
}

alpha = 0.01  

def condicao_de_parada(erro, interacao, max_interacoes):
    return abs(erro) < 1e-6 or interacao >= max_interacoes



def gradient_descent(produtos, erros, alpha):

    gradientes = {
        "bias"     : 0,
        "avaliacao": 0,
        "categoria": 0
    }

    total = len(produtos)

    for i, produto in enumerate(produtos):
        erro = erros[i]
        gradientes["bias"]      += alpha * erro
        gradientes["avaliacao"] += alpha * erro * produto["avaliacao"]
        gradientes["categoria"] += alpha * erro * produto["categoria"]

    return {
        "bias"     : gradientes["bias"]      / total,
        "avaliacao": gradientes["avaliacao"] / total,
        "categoria": gradientes["categoria"] / total
    }

def atualizar_pesos(pesos, gradientes):
    return {
        "bias"     : pesos["bias"]      + gradientes["bias"],
        "avaliacao": pesos["avaliacao"] + gradientes["avaliacao"],
        "categoria": pesos["categoria"] + gradientes["categoria"]
    }


def funcao_custo(produtos, pesos):

    erros_sem_sinal = []
    erros = []

    for produto in produtos:
        
        preco_previsto = pesos["bias"] + (pesos["avaliacao"] * produto["avaliacao"]) + (pesos["categoria"] * produto["categoria"])
        preco_real = produto["preco"]
        erro = preco_real - preco_previsto
        erros_sem_sinal.append(erro ** 2)
        erros.append(erro)

    return sum(erros_sem_sinal) / len(erros), erros


def medicao_erro_geral(preco_previsto, preco_real):
    erro = preco_real - preco_previsto
    erro = erro ** 2
    return erro


def treinamento(produtos, pesos, alpha, max_interacoes):
    
    erro_geral = 1
    interacao = 1

    while not condicao_de_parada(erro_geral, interacao, max_interacoes):

        if interacao % 1000 == 0:
            print(f"Iteração: {interacao}, Erro Geral: {erro_geral:.6f}")
            
        erro_geral, erros = funcao_custo(produtos, pesos)
        gradientes = gradient_descent(produtos, erros, alpha)
        pesos = atualizar_pesos(pesos, gradientes)
        interacao += 1

    salvar_modelo(pesos)
    print(pesos)
    print(f"Treinamento concluído em {interacao} iterações com erro geral de {erro_geral:.6f}")
    

treinamento(produtos, pesos, alpha, max_interacoes=10000)