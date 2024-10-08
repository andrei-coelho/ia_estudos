# from util.mysqli import mysqli
import json
import random


def add_char_email(email:str):
    char_adds = ["9","1","A","B","C","8","2","4"]
    parts = email.split('@')
    return parts[0]+random.choice(char_adds)+"@"+parts[1]


email_index = []
total = 0
lista_1k = []

with open('dummy_datas/clientes_base.json','r') as file:
    clientes = json.loads(file.read())
    while total < 1000:
        for client in clientes:
            email = client['email']
            while email in email_index:
                email = add_char_email(email)
            email_index.append(email)
            nclient = {
                "nome": client['nome'],
                "sobrenome": client['sobrenome'],
                "email": email,
                "data_nascimento": client['data_nascimento'],
                "data_criacao": client['data_criacao'],
                "genero": client['genero'],
                "ativo": client['ativo']
            }
            lista_1k.append(nclient)
            total += 1
            if total >= 1000:
                break 

random.shuffle(lista_1k)

total_clientes_compradores  = 300
total_clientes_comparadores = 200
total_clientes_exploradores = 500

for cliente in lista_1k:
    if total_clientes_compradores > 0:
        cliente['type'] = "comprador"
        total_clientes_compradores -= 1
        continue
    if total_clientes_comparadores > 0:
        cliente['type'] = "comparador"
        total_clientes_comparadores -= 1
        continue
    if total_clientes_exploradores > 0:
        cliente['type'] = "explorador"
        total_clientes_exploradores -= 1

with open('dummy_datas/clientes_compilados.json','w') as file:
    file.write(json.dumps(lista_1k, ensure_ascii=False).encode('utf8').decode())