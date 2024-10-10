from util.mysqli import mysqli 
import util.jsoni as jsoni
from decimal import Decimal


conn = mysqli().instance()
cursor = conn.cursor()

cursor.execute("SELECT * FROM produtos")
rows = cursor.fetchall()

lista:list[dict] = [] 

for produto in rows:
    
    id = produto[0]
    urli = produto[1]
    nome = produto[2]
    descricao = produto[3]
    avaliacao = produto[4]
    categoria = produto[5]

    lista.append({
        "id":id,
        "urli":urli,
        "descricao":descricao,
        "avaliacao":Decimal(avaliacao),
        "categoria":categoria
    })


with open('dummy_datas/produtos_compilados.json', 'w') as arquivo:
    arquivo.write(jsoni.encode(lista))