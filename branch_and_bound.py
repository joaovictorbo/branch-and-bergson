from scipy.optimize import linprog

def branch_and_bound(c, A_ub, b_ub, A_eq=None, b_eq=None, bounds=None):
    # Inicializa a melhor solução encontrada até agora
    best_solution = None
    best_value = float('-inf')

    # Inicializa a lista de nós a serem explorados
    nodes = [(None, None, None, None, None, bounds)]

    while nodes:
        # Seleciona o próximo nó com a menor solução fracionária
        node = min(nodes, key=lambda x: x[1])

        # Remove o nó selecionado da lista de nós a serem explorados
        nodes.remove(node)

        # Extrai as informações do nó selecionado
        _, _, _, _, _, (lb, ub) = node

        # Resolve o problema de programação linear não inteira correspondente
        res = linprog(c, A_ub, b_ub, A_eq, b_eq, bounds=(lb, ub))

        # Verifica se a solução encontrada é inteira
        if all(x.is_integer() for x in res.x):
            # Atualiza a melhor solução encontrada até agora
            if res.fun > best_value:
                best_solution = res.x
                best_value = res.fun
        else:
            # Seleciona a variável fracionária na solução atual
            frac_var = next(i for i, x in enumerate(res.x) if not x.is_integer())

            # Adiciona uma restrição que limite a variável selecionada a ser menor ou igual ao menor inteiro maior que a variável fracionária
            lb1, ub1 = lb, int(res.x[frac_var])
            A_ub1 = A_ub.copy()
            b_ub1 = b_ub.copy()
            A_ub1 = np.vstack([A_ub1, np.zeros((1, A_ub1.shape[1]))])
            A_ub1[-1, frac_var] = 1
            b_ub1 = np.append(b_ub1, ub1)

            # Adiciona uma restrição que limite a variável selecionada a ser maior ou igual ao maior inteiro menor que a variável fracionária
            lb2, ub2 = int(res.x[frac_var]) + 1, ub
            A_ub2 = A_ub.copy()
            b_ub2 = b_ub.copy()
            A_ub2 = np.vstack([A_ub2, np.zeros((1, A_ub2.shape[1]))])
            A_ub2[-1, frac_var] = -1
            b_ub2 = np.append(b_ub2, -lb2)

            # Adiciona os novos nós à lista de nós a serem explorados
            nodes.append((frac_var, res.x[frac_var], A_ub1, b_ub1, A_eq, b_eq, (lb1, ub1)))
            nodes.append((frac_var, res.x[frac_var], A_ub2, b_ub2, A_eq, b_eq, (lb2, ub2)))

    return best_solution, best_value
