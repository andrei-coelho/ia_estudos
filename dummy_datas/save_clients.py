from util.mysqli import mysqli
import json

def save_clients():
    
    db = mysqli.instance()
    cursor = db.cursor()
    
    with open('dummy_datas/clientes_compilados.json', 'r') as file:
        clientes = json.loads(file.read())
        for client in clientes:
            try:
                cursor.execute("""
                    INSERT INTO clientes ( id, nome, sobrenome, email, data_nascimento, data_criacao, genero, ativo ) 
                    values (%s, %s, %s, %s, %s, %s, %s, 1)
                """, (
                    client['id'],
                    client['nome'],
                    client['sobrenome'],
                    client['email'],
                    client['data_nascimento'],
                    client['data_criacao'],
                    client['genero']
                ))
                db.commit()
            except Exception as e:
                print(f"Erro ao inserir dados no banco: {e}")
                db.rollback() 