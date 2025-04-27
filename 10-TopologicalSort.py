def ordenacao_topologica(grafo):
    """
    Função para realizar a ordenação topológica de um grafo direcionado acíclico (DAG).
    
    Parâmetros:
    - grafo: lista de listas, onde grafo[u] contém todos os vértices v para os quais existe uma aresta (u -> v).

    Retorna:
    - Uma lista representando uma ordem dos vértices onde cada vértice vem antes de seus vizinhos.
    """

    quantidade_vertices = len(grafo)  # Número total de vértices no grafo
    grau_entrada = [0] * quantidade_vertices  # Lista para armazenar o grau de entrada de cada vértice
    ordem_linear = []  # Lista onde vamos construir a ordem topológica

    # Passo 1: Calcular o grau de entrada de cada vértice
    for vertice in range(quantidade_vertices):
        for vizinho in grafo[vertice]:
            grau_entrada[vizinho] += 1  # Cada vez que alguém aponta para v, aumentamos o grau de entrada dele

    # Passo 2: Encontrar todos os vértices com grau de entrada igual a zero
    proximos_vertices = []
    for vertice in range(quantidade_vertices):
        if grau_entrada[vertice] == 0:
            proximos_vertices.append(vertice)  # Vértices sem dependências podem ser processados primeiro

    # Passo 3: Processar os vértices até que todos sejam ordenados
    while proximos_vertices:
        vertice = proximos_vertices.pop()  # Remove um vértice da lista (pode ser visto como pilha ou fila)
        ordem_linear.append(vertice)  # Adiciona o vértice na ordem final

        # Para cada vizinho que depende do vértice atual
        for vizinho in grafo[vertice]:
            grau_entrada[vizinho] -= 1  # Tiramos a dependência (pois o vértice atual já foi colocado na ordem)
            if grau_entrada[vizinho] == 0:
                proximos_vertices.append(vizinho)  # Se o vizinho ficou sem dependências, podemos processá-lo também

    # Passo 4: Verificação final
    if len(ordem_linear) != quantidade_vertices:
        raise ValueError("O grafo não é acíclico. Não é possível realizar ordenação topológica.")

    return ordem_linear


# --------------------------
# Exemplo de uso do algoritmo
# --------------------------

# Representação do grafo:
# 0 → 1 → 3
# ↓
# 2
#
# Ou seja:
# - Vértice 0 aponta para 1 e 2
# - Vértice 1 aponta para 3
# - Vértices 2 e 3 não apontam para ninguém

grafo_sem_ciclo = [
    [1, 2],  # Vértice 0
    [3],     # Vértice 1
    [],      # Vértice 2
    []       # Vértice 3
]

# Executa a ordenação topológica
resultado = ordenacao_topologica(grafo_sem_ciclo)

# Mostra a ordem topológica obtida
print("Ordem topológica:", resultado)
