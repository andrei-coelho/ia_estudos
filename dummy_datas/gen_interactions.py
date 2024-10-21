from datetime import datetime, timedelta
from util.mysqli import mysqli
from util.jsoni import decode,encode
import calendar 
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

def visualizar_produto(produto_id, cliente_id, data_hora):
    cursor = conn.cursor()
    cursor.execute(f"insert into produtos_visualizados (cliente_id, produto_id, visualizado_em) values ( %s, %s, %s ) ", (cliente_id, produto_id, data_hora))
    conn.commit()

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
    

def gen_interaction_client(cliente, data_hora):

    print(cliente['id'])
    print(cliente['type'])
    print(data_hora)
    print("--------------")
    
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

    gasto = 0
    carrinho_id = 0
    produtos_carrinho = []
    
    while gasto < orcamento:

        categoria_produto = random.choice(list_categorias_prods)
        produto = get_random_product_by_categoria(categoria_produto)

        chance_de_adicionar = prob_adicionar(idade_cli, produto)
        data_hora += timedelta(minutes=random.randint(1,3))
        visualizar_produto(produto['id'], cliente['id'], data_hora)
        if random.random() < chance_de_adicionar and chance_comprar:
            if carrinho_id == 0:
                carrinho_id = criar_carrinho(cliente['id'])
            gasto+=float(produto['preco'])
            if gasto > orcamento: break
            produtos_carrinho.append(produto)
            salvar_produto_carrinho(produto) # adiciona no carrinho do banco de dados
           
        else: gasto+=1 
    
    if chance_comprar and len(produtos_carrinho) > 0:
        comprar = (sum(p["avaliacao"] for p in produtos_carrinho) / len(produtos_carrinho)) > min_avaliacoes[idade_cli]
        if comprar:
            finalizar_carrinho(carrinho_id)


def gerar_timestamps_randomicos(inicio, fim, max_por_dia=1):

    timestamps = []
    data_atual = inicio

    while data_atual <= fim:

        qtd_por_dia = random.randint(0, max_por_dia)
        
        for _ in range(qtd_por_dia):

            hora = random.randint(9, 23)  # Hora entre 9 e 23
            minuto = random.randint(0, 59)  # Minuto entre 0 e 59
            segundo = random.randint(0, 59)  # Segundo entre 0 e 59
            
            timestamp = datetime(
                year=data_atual.year, 
                month=data_atual.month, 
                day=data_atual.day, 
                hour=hora, 
                minute=minuto, 
                second=segundo
            )
            
            timestamps.append(timestamp)
        
        data_atual += timedelta(days=1)
    
    return timestamps


def gen_interactions():

    clientes = []

    with open('dummy_datas/clientes_compilados.json', 'r') as arquivo:
        clientes = decode(arquivo.read())

    compradores  = []
    comparadores = []
    exploradores = []

    chances = {
        "comprador":1,
        "comparador":0.6,
        "explorador":0.2
    }

    for cliente in clientes:
        if cliente['type'] == 'comprador':
            compradores.append(cliente)
        elif cliente['type'] == 'comparador':
            comparadores.append(cliente)
        else:
            exploradores.append(cliente)
    
    
    mes_atual = 7
    total_meses = 4
    ano = 2024

    while total_meses > 0:

        exploradores_c = exploradores[:]

        _, ultimo_dia = calendar.monthrange(ano, mes_atual)
        inicio = datetime(ano, mes_atual, 1)
        fim = datetime(ano, mes_atual, ultimo_dia)

        timestamps_gerados = gerar_timestamps_randomicos(inicio, fim)

        mes_atual  +=1
        total_meses-=1

        for timestamp_gerado in timestamps_gerados:
            num_rand = random.random()
            if num_rand < chances['explorador']:
                i = random.randint(0, len(exploradores_c) -1)
                explorador_selecionado = exploradores_c.pop(i)
                gen_interaction_client(explorador_selecionado, timestamp_gerado)
            elif num_rand < chances['comparador']:
                i = random.randint(0, len(comparadores) -1)
                gen_interaction_client(comparadores[i], timestamp_gerado)
            else:
                i = random.randint(0, len(compradores) -1)
                gen_interaction_client(compradores[i], timestamp_gerado)
            return
        return