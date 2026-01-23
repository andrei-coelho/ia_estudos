from helper import get_json_file, permutacao, multiplicar_matrizes, transposta_da_matriz, reducao_por_gauss_jordan



def treinamento_regressao():
    matriz_X = get_json_file('model/dataset_normalizado.json')[0]
    matriz_transposta = transposta_da_matriz(matriz_X)
    matriz_A = multiplicar_matrizes(matriz_transposta, matriz_X)
    matriz_identidade = reducao_por_gauss_jordan(matriz_A)
    
    # bias = 
    

treinamento_regressao()