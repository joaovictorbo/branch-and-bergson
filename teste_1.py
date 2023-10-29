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
        if len(self.is_integer(self.solucao)) == 0:
            print('Solução inteira')
            print('Solução: ', self.solucao)
            return self.solucao
        self.limite_superior = self.model.objective_value()
        modelo = self.modelo_geral
        solucao = []
        while True:
            p1, p2 = self.sub_problema(modelo)
            if p1.objective_value() > p2.objective_value():
                modelo = p1
                solucao = []
                for v in modelo.vars:
                    solucao.append(v.x)
            else:
                solucao = []
                modelo = p2
                for v in modelo.vars:
                    solucao.append(v.x)
            if len(self.is_integer(solucao)) == 0:
                print('Solução inteira')
                print('Solução: ', solucao)
                return solucao
    
    def sub_problema(self, modelo):
        # cria uma copia do modelo
        modelo_p1 = self.model
        modelo_p2 = self.model
        # adiciona a restrição de ramificação
        modelo_p1 += self.x[variavel_ramificar] <= inferior
        modelo_p2 += self.x[variavel_ramificar] >= superior
        # resolve o modelo
        modelo_p1.optimize()
        modelo_p2.optimize()

        return modelo_p1, modelo_p2

        
        

    


teste = BranchAndBoundBinary('teste1.txt')


        

        