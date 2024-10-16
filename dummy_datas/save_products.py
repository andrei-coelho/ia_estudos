from util.jsoni import decode
from util.mysqli import mysqli

def insert(produtos):
    sql = """
            INSERT INTO produtos (id, urli, nome, descricao, avaliacao, categoria, preco)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

    prods = [(p['id'],p['urli'],  p['descricao'], p['descricao'], float(p['avaliacao']), p['categoria'], float(p['preco'])) for p in produtos]
    db = mysqli.instance()
    cursor = db.cursor()
    cursor.executemany(sql, prods)
    db.commit()

def save_products():
    with open('dummy_datas/produtos_compilados_preco.json', 'r') as arquivo:
        produtos = decode(arquivo.read())
        insert(produtos)
        