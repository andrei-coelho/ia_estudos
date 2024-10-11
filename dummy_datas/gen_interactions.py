

def _get_idade(data_nascimento_str:str):
    
    data_nascimento = datetime.strptime(data_nascimento_str, '%Y-%m-%d').date()
    data_atual = datetime.now().date()
    
    return data_atual.year - data_nascimento.year - ((data_atual.month, data_atual.day) < (data_nascimento.month, data_nascimento.day))

"""

"""

def gen_interactions():

    categorias = {
        "homem": {
            "35+": {
                "sapatenis": 3,
                "botas": 3,
                "chuteiras": 1.5,
                "chinelos": 0.75, 
                "tenis": 1
            },
            "35-": {
                "sapatenis": 1.5,
                "botas": 1,
                "chuteiras": 2.5,
                "chinelos": 1.5,
                "tenis": 2.5 
            }
        },
        "mulher": {
            "35+": {
                "sapatenis": 0.1,
                "botas": 3,
                "chuteiras": 0.1,
                "chinelos": 1,
                "tenis": 1
            },
            "35-": {
                "sapatenis": 0.1,
                "botas": 2,
                "chuteiras": 0.1,
                "chinelos": 1.75,
                "tenis": 2.25
            }
        }
    }    
