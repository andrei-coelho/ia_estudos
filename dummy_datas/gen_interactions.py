from datetime import datetime
from util.mysqli import mysqli

import random

conn = mysqli().instance()

def _get_idade_categoria(data_nascimento_str:str):
    data_nascimento = datetime.strptime(data_nascimento_str, '%Y-%m-%d').date()
    data_atual = datetime.now().date()
    idade = data_atual.year - data_nascimento.year - ((data_atual.month, data_atual.day) < (data_nascimento.month, data_nascimento.day))
    return "35+" if idade >= 35 else "35-"

categorias = [ "sapatenis", "botas", "chuteiras", "chinelos", "tenis" ]

min_avaliacoes = {
    "35+":3.8,
    "35-":3.0
}

chances_de_comprar = {
    "comprador":9,
    "comparador":1,
    "explorador":0
}

dinheiro_cliente = {
    "Masculino":{
        "35+":{
            "min":200,
            "max":1000
        },
        "35-":{
            "min":150,
            "max":600
        }
    },
    "Feminino":{
        "35+":{
            "min":200,
            "max":800
        },
        "35-":{
            "min":150,
            "max":400
        }
    }
}

categorias_cliente = {
    "Masculino": {
        "35+": {
            "sapatenis": 24,
            "botas": 24,
            "chuteiras": 8,
            "chinelos": 6, 
            "tenis": 8
        },
        "35-": {
            "sapatenis": 12,
            "botas": 8,
            "chuteiras": 20,
            "chinelos": 12,
            "tenis": 20 
        }
    },
    "Feminino": {
        "35+": {
            "sapatenis": 1,
            "botas": 24,
            "chuteiras": 1,
            "chinelos": 8,
            "tenis": 8
        },
        "35-": {
            "sapatenis": 1,
            "botas": 16,
            "chuteiras": 1,
            "chinelos": 10,
            "tenis": 18
        }
    }
}  

def criar_carrinho(cliente_id):
    return 1

def salvar_produto_carrinho(carrinho_id):
    pass

def finalizar_carrinho(carrinho_id):
    pass

def prob_adicionar(idade_cli, produto):

    if idade_cli == "35-":
        peso_preco = 0.7 
        peso_avaliacao = 0.3
    else:
        peso_preco = 0.3 
        peso_avaliacao = 0.7

    preco = produto['preco']
    avaliacao = produto['avaliacao']
    preco_normalizado = 1 - (preco / 600)
    avaliacao_normalizada = avaliacao / 5 
    pontuacao = (preco_normalizado * peso_preco) + (avaliacao_normalizada * peso_avaliacao)

    return pontuacao
    

def get_random_product_by_categoria(categoria):
    cursor = conn.cursor()
    cursor.execute(f'select id,nome,preco,avaliacao from produtos where categoria = "{categoria}" order by rand() limit 1;')
    res = cursor.fetchall()
    return {
        "id":res[0][0],
        "nome":res[0][1],
        "preco":float(res[0][2]),
        "avaliacao":float(res[0][3])
    }
    

def gen_interaction_client(cliente, data):
    
    idade_cli = _get_idade_categoria(cliente['data_nascimento'])
    categorias_stat = categorias_cliente[cliente['genero']][idade_cli]

    list_categorias_prods = []
    for categoria in categorias:
        multiplicador = categorias_stat[categoria]
        i = 0
        while i < multiplicador:
            list_categorias_prods.append(categoria)
            i+=1
    
    random.shuffle(list_categorias_prods)
    
    chance_comprar = random.randint(0,10) < chances_de_comprar[cliente['type']]
   
    orcamento = random.randint(
        dinheiro_cliente[cliente['genero']][idade_cli]['min'],
        dinheiro_cliente[cliente['genero']][idade_cli]['max']
    ) if chance_comprar else random.randint(0,8)

    print(f"chance de comprar: {chance_comprar}")
    print(f"orçamento: {orcamento}")
    print("----------------------------------------")

    gasto = 0
    carrinho_id = 0
    produtos_carrinho = []
    
    while gasto < orcamento:
        categoria_produto = random.choice(list_categorias_prods)
        produto = get_random_product_by_categoria(categoria_produto)
        print(produto)
        chance_de_adicionar = prob_adicionar(idade_cli, produto)
        print(f"chance: {chance_de_adicionar}")
        # pega um produto do banco de dados
        # salva no banco o produto como visualizado
        # se ele escolher o produto
        print("visualizou produto")
        if random.random() < chance_de_adicionar and chance_comprar:
            if carrinho_id == 0:
                #cria um carrinho no banco de dados
                print("criou carrinho")
                carrinho_id = criar_carrinho(cliente['id'])
            # adiciona ao carrinho
            gasto+=float(produto['preco'])
            if gasto > orcamento: break
            produtos_carrinho.append(produto)
            salvar_produto_carrinho(produto) # adiciona no carrinho do banco de dados
            print("adicionou ao carrinho")
           
        else: gasto+=1 
    
    if chance_comprar:
        comprar = (sum(p["avaliacao"] for p in produtos_carrinho) / len(produtos_carrinho)) > min_avaliacoes[idade_cli]
        if comprar:
            print("---------------------")
            print("comprou carrinho >>>>>>>>>>")
            print(f"valor: {sum([p['preco'] for p in produtos_carrinho])}")
            # altera o status do carrinho como pago
            finalizar_carrinho(carrinho_id)


def gen_interactions():

    clientes = [{"id": 200, "nome": "Carla", "sobrenome": "Guedes", "email": "carla.guedes@example.com", "data_nascimento": "1986-09-26", "data_criacao": "2024-08-05", "genero": "Feminino", "ativo": 1, "type": "comprador"}]

    for cliente in clientes:
        gen_interaction_client(cliente, "")