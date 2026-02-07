import json
import math
import random
import helper


def kmeans_plus_plus_init(X, k):

    n = len(X)
    centroids = []

    first_index = random.randint(0, n - 1)
    centroids.append(X[first_index])

    while len(centroids) < k:

        distances = []

        for x in X:
            min_dist = None
            for c in centroids:
                d = helper.distancia_eclidiana(x, c)
                if min_dist is None or d < min_dist:
                    min_dist = d
            distances.append(min_dist)

        total_distance = sum(distances)

        r = random.uniform(0, total_distance)
        cumulative = 0.0

        for i in range(n):
            cumulative += distances[i]
            if cumulative >= r:
                centroids.append(X[i])
                break

    return centroids



def k_means(matriz, k, eps=1e-3, max_iter=100):

    centroides = kmeans_plus_plus_init(matriz, k)

    for _ in range(max_iter):
 
        grupo_centroides = {i: [] for i in range(k)}

        for vetor in matriz:
            distancias = []
            for c in centroides:
                distancias.append(
                    helper.distancia_eclidiana(vetor, c)
                )

            idx = distancias.index(min(distancias))
            grupo_centroides[idx].append(vetor)

    
        novos_centroides = []

        for i in range(k):
            cluster = grupo_centroides[i]

  
            if not cluster:
                novos_centroides.append(centroides[i])
                continue

            n_features = len(cluster[0])
            novo_centroide = []

            for j in range(n_features):
                soma = 0.0
                for vetor in cluster:
                    soma += vetor[j]
                novo_centroide.append(soma / len(cluster))

            novos_centroides.append(novo_centroide)


        max_delta = 0.0
        for i in range(k):
            delta = helper.distancia_eclidiana(
                novos_centroides[i], centroides[i]
            )
            if delta > max_delta:
                max_delta = delta

        centroides = novos_centroides

        if max_delta < eps ** 2:
            break

    return centroides


def training():

    with open('matriz.json', 'r') as file:
        matriz = json.loads(file.read())

    centroides = k_means(matriz, 5)

    with open('palavras_unicas.json', 'r') as file:
        dicionario = json.loads(file.read())

    classes = []

    for centroid in centroides:
        max_valor = -math.inf
        classe_index = 0

        for i in range(len(centroid)):
            if centroid[i] > max_valor:
                max_valor = centroid[i]
                classe_index = i

        classes.append(dicionario[classe_index])

    print(classes)


training()
