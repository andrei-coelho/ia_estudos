from dummy_datas.gen_interactions import gen_interactions
import random

cliente_test = {"id": 200, "nome": "Carla", "sobrenome": "Guedes", "email": "carla.guedes@example.com", "data_nascimento": "1986-09-26", "data_criacao": "2024-08-05", "genero": "Feminino", "ativo": 1, "type": "comprador"}

gen_interactions(cliente_test, "")