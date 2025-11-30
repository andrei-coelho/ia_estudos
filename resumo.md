👉 entendendo os algoritmos por dentro primeiro,
👉 construindo versões simples do zero,
👉 para depois usar frameworks com domínio total.

A ideia aqui é você implementar cada algoritmo com dados sintéticos simples, só para entender o mecanismo matemático.
Depois, em outro estágio, você aplicará em projetos reais.

🌱 Estágio 1 — Algoritmos Introdutórios (Fundação da IA)

Esses são os algoritmos que constroem as bases do raciocínio estatístico e do machine learning clássico.
Para cada um deles o objetivo não é só usar — é implementar.

1. Regressão Linear

Conceito: modelo com equação de reta para prever valores contínuos.

O que implementar:

cálculo dos pesos com gradiente descendente

cálculo da função de custo MSE

Insight final: como um modelo “aprende reduzindo erro”.

2. Regressão Logística

Conceito: classificador binário com função sigmoide.

O que implementar:

sigmoide

entropia cruzada (binary cross entropy)

gradiente descendente

Insight final: quando prever probabilidade > 0.5 define classe.

3. k-Nearest Neighbors (kNN)

Conceito: classificação por proximidade.

O que implementar:

cálculo da distância Euclidiana

escolha dos k vizinhos

Insight final: não há aprendizado — só comparação inteligente.

4. k-Means

Conceito: agrupamento não supervisionado.

O que implementar:

escolha de centróides

realocação via distância

critério de convergência

Insight final: como encontrar estrutura em dados sem rótulos.

5. Naive Bayes

Conceito: classificador probabilístico baseado no Teorema de Bayes.

O que implementar:

cálculo de probabilidade condicional

multiplicação das features (com log-sum para evitar estouro)

Insight final: quando independência entre features é suficiente para classificação ótima.

6. Árvore de Decisão (ID3 ou CART)

Conceito: classificação dividindo o espaço de decisão em ramos.

O que implementar:

entropia / Gini

melhor feature de corte

criação recursiva da árvore

Insight final: modelos interpretáveis e lógica sequencial.

7. Perceptron (a base das redes neurais)

Conceito: versão mais simples de uma rede neural.

O que implementar:

pesos

função de ativação (step ou ReLU)

regra de atualização

Insight final: como neurônios artificiais convergem e porque precisão depende da linearidade do problema.

🌳 Estágio 2 — Algoritmos Avançados (Deep Learning e IA moderna)

Depois de dominar o Estágio 1, você entra nos algoritmos que regem a IA atual.

🔥 Redes Neurais Avançadas

Perceptron multicamadas (MLP)

Backpropagation (detalhado)

Funções de ativação (ReLU, Tanh, Softmax)

🔥 Aprendizado com Memória e Sequência

RNN

LSTM / GRU

Mecanismos de atenção

🔥 Visão Computacional

CNN

Pooling / Padding / Convolução

Transfer learning

🔥 Modelos de Linguagem

Encoder–Decoder

Self-Attention

Transformers

Embeddings

Depois disso, você fecha com:

Autoencoders

GANs

Reinforcement Learning (Q-Learning, DQN)

Algoritmos evolutivos e otimização

Mas não precisa ter pressa — cada camada destrava a seguinte.

📘 Livro recomendado (o que mais combina com você)

Pelo seu estilo de aprendizado, o melhor livro não é o mais teórico — é o que explica os algoritmos com implementações do zero:

Hands-On Machine Learning – Aurélien Géron

👉 Ensina algoritmos do zero + matemática + implementação + aplicações reais.

Ele não exige matemática pesada e explica com profundidade e código.
É o livro que faz você entender o mecanismo dos modelos.
