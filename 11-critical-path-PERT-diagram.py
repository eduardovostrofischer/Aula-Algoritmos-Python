from collections import defaultdict, deque

def relaxar(u, v, peso, distancias, predecessores):
    """
    Relaxa uma aresta u → v e atualiza a distância máxima se um caminho mais longo for encontrado.
    
    Args:
        u: Nó de origem
        v: Nó de destino
        peso: Tempo da atividade
        distancias: Lista com as maiores distâncias conhecidas
        predecessores: Lista que armazena o vértice predecessor de cada vértice
    """
    if distancias[v] < distancias[u] + peso:
        distancias[v] = distancias[u] + peso
        predecessores[v] = u

def ordenacao_topologica(grafo, num_vertices):
    """
    Retorna uma ordenação topológica do grafo usando o algoritmo de Kahn (baseado em BFS).
    
    Args:
        grafo: Dicionário que representa o grafo (lista de adjacência)
        num_vertices: Número total de vertices no grafo
        
    Returns:
        Lista com os vertices em ordem topológica
    """
    grau_entrada = defaultdict(int)
    
    # Calcula o grau de entrada para cada vértice
    for u in grafo:
        for (v, _) in grafo[u]:
            grau_entrada[v] += 1
    
    # Inicializa fila com vertices de grau de entrada zero
    fila = deque([u for u in range(num_vertices) if grau_entrada[u] == 0])
    ordem_topologica = []
    
    while fila:
        u = fila.popleft()
        ordem_topologica.append(u)
        
        # Reduz o grau de entrada dos vizinhos
        for (v, _) in grafo[u]:
            grau_entrada[v] -= 1
            if grau_entrada[v] == 0:
                fila.append(v)
    
    return ordem_topologica

def caminho_critico_pert(grafo, num_vertices, no_inicio):
    """
    Encontra o caminho crítico em um diagrama PERT (DAG).
    
    Args:
        grafo: Dicionário representando o grafo (lista de adjacência)
        num_vertices: Número total de vertices
        no_inicio: Nó de início do projeto
        
    Returns:
        Uma tupla com (caminho_critico, duracao_total)
    """
    # Passo 1: Inicializa distâncias com -infinito e predecessores como -1
    distancias = [-float('inf')] * num_vertices
    predecessores = [-1] * num_vertices
    distancias[no_inicio] = 0  # Tempo para o vértice inicial é zero
    
    # Passo 2: Obtém a ordem topológica dos vertices
    ordem_top = ordenacao_topologica(grafo, num_vertices)
    
    # Passo 3: Atualizar a distancia máxima de cada vertice para cada vértice
    for u in ordem_top:
        for (v, peso) in grafo[u]:
            relaxar(u, v, peso, distancias, predecessores)
    
    # Passo 4: Encontra o vértice final (com maior distância)
    no_final = distancias.index(max(distancias))
    
    # Passo 5: Reconstrói o caminho crítico do final para o início
    caminho = []
    no_atual = no_final
    while no_atual != -1:
        caminho.append(no_atual)
        no_atual = predecessores[no_atual]
    caminho.reverse()  # Inverte para obter do início ao fim
    
    return caminho, distancias[no_final]

 #============== EXEMPLO DE USO ==============
if __name__ == "__main__":
    # Exemplo de grafo PERT (Diagrama de rede)
    # Nós: 0 (início), 1, 2, 3 (fim)
    # Arestas: (nó_origem, nó_destino, duração)
    grafo_pert = {
        0: [(1, 3), (2, 2)],    # Início → A (3), Início → B (2)
        1: [(3, 4), (4, 2)],     # A → C (4), A → D (2)
        2: [(4, 3), (5, 1)],     # B → D (3), B → E (1)
        3: [(6, 5)],             # C → G (5)
        4: [(6, 2), (7, 4)],      # D → G (2), D → Fim (4)
        5: [(7, 3)],              # E → Fim (3)
        6: [(7, 6)],              # G → Fim (6)
        7: []                     # Fim
    }
    
    total_nos = 8
    inicio = 0
    
    caminho, duracao = caminho_critico_pert(grafo_pert, total_nos, inicio)
    
    # Mapeamento de vertices para atividades
    atividades = {
        0: "Início",
        1: "A",
        2: "B",
        3: "C",
        4: "D",
        5: "E",
        6: "G",
        7: "Fim"
    }
    
    print("=== ANÁLISE DO CAMINHO CRÍTICO ===")
    print(f"Caminho crítico: {[atividades[n] for n in caminho]}")
    print(f"Duração total do projeto: {duracao} unidades de tempo")
    print("\nSequência detalhada:")
    for i in range(len(caminho)-1):
        u = caminho[i]
        v = caminho[i+1]
        duracao_atividade = next(p for (no, p) in grafo_pert[u] if no == v)
        print(f"{atividades[u]} → {atividades[v]} (Duração: {duracao_atividade})")
