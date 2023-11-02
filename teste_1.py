import mip

class BranchAndBoundBinary:
    def __init__(self, caminho_arquivo_txt):
        self.caminho_arquivo_txt = caminho_arquivo_txt
        self.qtd_variaveis = None
        self.qtd_restrições = None
        self.funcao_objetivo = None
        self.restricoes = None
        self.limite_superior = float('inf')
        self.limite_inferior = float('-inf')
        self.__leitor_txt()
        self.modelo_geral = mip.Model(sense = mip.MAXIMIZE, solver_name= mip.CBC)
        self.variaveis = self.__criacao_do_modelo()
        self.fila = []

    def __leitor_txt(self):
        try:
            with open(self.caminho_arquivo_txt, 'r') as arquivo:
                conteudo = arquivo.readlines()
                conteudo = [x.split() for x in conteudo]
                conteudo = [[int(y) for y in x] for x in conteudo]
                self.qtd_variaveis = conteudo[0][0]
                self.qtd_restrições = conteudo[0][1]
                self.funcao_objetivo = conteudo[1]
                self.restricoes = conteudo[2:]
        except FileNotFoundError:
            print('Arquivo não encontrado')
    
    def __criacao_do_modelo(self):
        x = [self.modelo_geral.add_var(var_type=mip.CONTINUOUS, name = f"x_{i}") for i in range(self.qtd_variaveis)]
        self.modelo_geral.objective = mip.xsum(self.funcao_objetivo[i] * x[i] for i in range(self.qtd_variaveis))
        # Adicionando as restrições
        for i in range(self.qtd_restrições):
            self.modelo_geral += mip.xsum(self.restricoes[i][j] * x[j] for j in range(self.qtd_variaveis)) <= self.restricoes[i][-1]
        # Resolvendo o modelo
        self.modelo_geral.optimize()
        # Adicionando os resultados das variaveis na lista solucao
        return x

    def __is_integer(self, solucao):
        lista_nao_inteiros = []
        for i in range(len(solucao)):
            if (int(solucao[i]) - solucao[i]) != 0:
                lista_nao_inteiros.append(solucao[i])
        return lista_nao_inteiros
    
    def __var_ramification(self, solucao):
        variaveis_nao_inteiras = self.__is_integer(solucao)
        variavel_mais_proxima_de_05 = [abs(round(x - int(x), 4) - 0.5) for x in variaveis_nao_inteiras]
        index = variavel_mais_proxima_de_05.index(min(variavel_mais_proxima_de_05))
        return index
    
    def resolver_modelo(self):
        # verifica se a solução é inteira
        solucao = [x.x for x in self.modelo_geral.vars]
        if len(self.__is_integer(solucao)) == 0:
            print('Solução inteira')
            print('Solução: ', self.solucao)
        # Define o limite superior
        self.limite_superior = self.modelo_geral.objective_value
        self.fila.append([self.modelo_geral, solucao])
        while self.fila:
            modelo = self.fila.pop(0)
            # verifica se a solução é inteira
            print(modelo[0])
            input()
            if len(self.__is_integer(modelo[1])) == 0:
                print('Solução inteira')
                print('Solução: ', modelo[1])
            # se não for inteira, ramifica
            else:
                p1, p2 = self.sub_problema(modelo[0])
                self.fila.append(p1)
                self.fila.append(p2)
    
    def sub_problema(self, modelo):
        # cria uma copia do modelo
        modelo_p1 = modelo.copy()
        modelo_p2 = modelo.copy()
        # variavel a ser ramificada
        var = [x for x in modelo.vars]
        var_values = [x.x for x in modelo.vars]
        indice_variavel_ramificar = self.__var_ramification(var_values)
        # adiciona a restrição de ramificação
        modelo_p1 += var[indice_variavel_ramificar] <= 0
        modelo_p2 += var[indice_variavel_ramificar] >= 1
        # resolve o modelo
        solucao_p1 = modelo_p1.optimize()
        solucao_p2 = modelo_p2.optimize()


        return [modelo_p1, solucao_p1], [modelo_p2, solucao_p2]

        
        

    


teste = BranchAndBoundBinary('teste1.txt')
teste.resolver_modelo()


        

        