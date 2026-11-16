from collections import deque

def criar_grafo():
    print("\n--- CONFIGURAÇÃO DO GRAFO ---")
    print("[1] GRAFO NÃO DIRECIONADO")
    print("[2] GRAFO DIRECIONADO")
    opcao = input("Escolha o tipo de grafo: ").strip()
    
    if opcao == '2':
        direcionado = True
        print("\n✅ GRAFO DIRECIONADO CRIADO COM SUCESSO!!")
    else:
        direcionado = False
        print("\n✅ GRAFO NÃO DIRECIONADO CRIADO COM SUCESSO!!")
        
    return {}, direcionado


def inserir_vertice(grafo, vertice):
    if vertice not in grafo:
        grafo[vertice] = []
        print(f"Vértice '{vertice}' foi inserido.")
    else:
        print(f"O vértice '{vertice}' já existe.")


def inserir_aresta(grafo, origem, destino, nao_direcionado=False):
    if origem not in grafo or destino not in grafo:
        print(f"❌ Erro: Não é possível inserir a aresta. O(s) vértice(s) '{origem}' e/ou '{destino}' não existem.")
        return 
    
    if destino not in grafo[origem]:
        grafo[origem].append(destino)

    if nao_direcionado:
        if origem not in grafo[destino]:
            grafo[destino].append(origem)
    print(f"Aresta entre '{origem}' e '{destino}' foi adicionada!")


def vizinhos(grafo, vertice):
    if vertice in grafo:
        return grafo[vertice]
    return []


def listar_vizinhos(grafo, vertice):
    if vertice in grafo:
        lista = vizinhos(grafo, vertice)
        print(f"Vizinhos do vértice '{vertice}': {lista}")
        return lista
    else:
        print(f"O vértice '{vertice}' não existe.")
        return []


def exibir_grafo(grafo):
    if not grafo:
        print("O GRAFO ESTÁ VAZIO!!")
        return
    for v, lista_vizinhos in grafo.items():
        print(f"Vértice {v} --> {vizinhos(grafo, v)}")


def remover_aresta(grafo, origem, destino, nao_direcionado=True):
    removido = False
    if origem in grafo and destino in grafo[origem]:
        grafo[origem].remove(destino)
        removido = True

    if nao_direcionado:
        if destino in grafo and origem in grafo[destino]:
            grafo[destino].remove(origem)
            removido = True

    if removido:
        print(f"A aresta entre '{origem}' e '{destino}' foi removida!")
    else:
        print(f"A aresta entre '{origem}' e '{destino}' não existe.")


def existe_aresta(grafo, origem, destino):
    if origem in grafo and destino in grafo[origem]:
        return True
    return False


def remover_vertice(grafo, vertice):
    if vertice in grafo:
        for outro in list(grafo.keys()):
            if vertice in grafo[outro]:
                grafo[outro].remove(vertice)
        del grafo[vertice]
        print(f"Vértice '{vertice}' foi removido.")
    else:
        print(f"O vértice '{vertice}' não existe no grafo.")


def grau_vertices(grafo):
    graus = {}
    for v in grafo:
        graus[v] = {'out': len(grafo[v]), 'in': 0, 'total': 0}
        
    for u in grafo:
        for v in grafo[u]:
            if v in graus:
                graus[v]['in'] += 1

    for v in graus:
        graus[v]['total'] = graus[v]['out'] + graus[v]['in']
        
    return graus


def percurso_valido(grafo, caminho):
    if len(caminho) < 2:
        print(f"O percurso {caminho} é válido (trivial).")
        return True
        
    for i in range(len(caminho) - 1):
        origem = caminho[i]
        destino = caminho[i + 1]
        if not existe_aresta(grafo, origem, destino):
            print(f"O percurso {caminho} não é possível (falha com os vértices '{origem}' e '{destino}').")
            return False
            
    print(f"O percurso {caminho} é possível.")
    return True


def busca_largura(grafo, inicio):
    if inicio not in grafo:
        print(f"O vértice inicial '{inicio}' não existe no grafo.")
        return []

    visitados = set()
    fila = deque([inicio])
    visitados.add(inicio)
    ordem_visita = []

    print(f"\n-=-=-=-=- BUSCA EM LARGURA (BFS) a partir do vértice '{inicio}' -=-=-=-=-")
    while fila:
        atual = fila.popleft()
        ordem_visita.append(atual)
        print(f"Visitando vértice: {atual}")

        for vizinho in grafo[atual]:
            if vizinho not in visitados:
                visitados.add(vizinho)
                fila.append(vizinho)

    print(f"Ordem de visitação: {ordem_visita}")
    return ordem_visita


def busca_largura_menor_caminho(grafo, inicio, destino):
    if inicio not in grafo or destino not in grafo:
        print(f"Vértice inicial ou destino não existe no grafo.")
        return None

    fila = deque([
        {
            'vertice': inicio,
            'caminho': [inicio]
        }
    ])
    visitados = {inicio}

    print(f"\n-=-=-=-=- BUSCA EM LARGURA (MENOR CAMINHO) de '{inicio}' até '{destino}' -=-=-=-=-")
    while fila:
        atual_dict = fila.popleft()
        vertice_atual = atual_dict['vertice']
        caminho_atual = atual_dict['caminho']

        if vertice_atual == destino:
            print(f"Caminho encontrado: {' -> '.join(caminho_atual)}")
            print(f"Lista do caminho: {caminho_atual}")
            return caminho_atual

        for vizinho in grafo[vertice_atual]:
            if vizinho not in visitados:
                visitados.add(vizinho)
                novo_caminho = list(caminho_atual)
                novo_caminho.append(vizinho)
                fila.append({
                    'vertice': vizinho,
                    'caminho': novo_caminho
                })

    print(f"Não há caminho entre '{inicio}' e '{destino}'.")
    return None


def main():
    grafo = None
    eh_direcionado = False

    while True:
        print("""
        -=-=-=-=-=-=-=- MENU -=-=-=-=-=-=-=-
        [1] - Criar / Reinicializar Grafo
        [2] - Inserir Vértice
        [3] - Inserir Aresta
        [4] - Remover Vértice
        [5] - Remover Aresta
        [6] - Calcular Grau
        [7] - Verificar Aresta
        [8] - Verificar Vizinhos
        [9] - Verificar Percurso
        [10] - Exibir Grafo
        [11] - Busca em Largura (BFS Padrão)
        [12] - Busca em Largura (Menor Caminho)
        [0] - Sair
        -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        """)

        try:
            op = int(input("Escolha a opção: ").strip())
        except ValueError:
            print("Opção inválida. Por favor, insira um número inteiro.")
            continue

        if op == 0:
            print("SAINDO...")
            break
        elif op == 1:
            grafo, eh_direcionado = criar_grafo()
        else:
            if grafo is None:
                print("\n⚠️ ATENÇÃO: Você precisa criar o grafo primeiro! Escolha a opção [1].")
                continue

            match op:
                case 2:
                    v = input("Insira um VÉRTICE: ").strip()
                    inserir_vertice(grafo, v)
                case 3:
                    u = input("Insira o 1º vértice da aresta: ").strip()
                    v = input("Insira o 2º vértice da aresta: ").strip()
                    inserir_aresta(grafo, u, v, nao_direcionado=not eh_direcionado)
                case 4:
                    v = input("Digite o nome do vértice para ser removido: ").strip()
                    remover_vertice(grafo, v)
                case 5:
                    u = input("Insira o 1° vértice da aresta a remover: ").strip()
                    v = input("Insira o 2° vértice da aresta a remover: ").strip()
                    remover_aresta(grafo, u, v, nao_direcionado=not eh_direcionado)
                case 6:
                    graus = grau_vertices(grafo)
                    print("\n-=-=-=-=- GRAU DOS VÉRTICES -=-=-=-=-")
                    for v, g in graus.items():
                        print(f"Vértice '{v}' -> Entrada: {g['in']} | Saída: {g['out']} | Total: {g['total']}")
                case 7:
                    u = input("Digite o 1° vértice: ").strip()
                    v = input("Digite o 2° vértice: ").strip()
                    if existe_aresta(grafo, u, v):
                        print("A aresta em questão EXISTE!")
                    else:
                        print("A aresta em questão NÃO EXISTE!")
                case 8:
                    u = input("Digite o vértice para listar os vizinhos: ").strip()
                    listar_vizinhos(grafo, u)
                case 9:
                    entrada = input("Digite o percurso, separado por vírgulas (A,B,C etc): ").strip()
                    percurso = [x.strip() for x in entrada.split(",")]
                    percurso_valido(grafo, percurso)
                case 10:
                    exibir_grafo(grafo)
                case 11:
                    v = input("Digite o vértice inicial para a busca em Largura: ").strip()
                    busca_largura(grafo, v)
                case 12:
                    inicio = input("Digite o vértice inicial: ").strip()
                    destino = input("Digite o vértice destino: ").strip()
                    busca_largura_menor_caminho(grafo, inicio, destino)
                case _:
                    print("OPÇÃO INCORRETA. TENTE NOVAMENTE!!")

if __name__ == "__main__":
    main()