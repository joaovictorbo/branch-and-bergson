import mip

class BranchAndBoundBinary:
    def __init__(self, caminho_arquivo_txt):
        self.caminho_arquivo_txt = caminho_arquivo_txt
        self.qtd_variaveis = None
        self.qtd_restrições = None
        self.funcao_objetivo = None
        self.restricoes = None
        self.solucao = []
        self.limite_superior = float('inf')
        self.limite_inferior = float('-inf')
        self.model = mip.Model(sense = mip.MAXIMIZE, solver_name= mip.CBC)
        self.__leitor_txt()
        self.__criacao_do_modelo()

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
        x = [self.model.add_var(var_type=mip.CONTINUOUS, name = f"x_{i}") for i in range(self.qtd_variaveis)]
        self.model.objective = mip.xsum(self.funcao_objetivo[i] * x[i] for i in range(self.qtd_variaveis))
        # Adicionando as restrições
        for i in range(self.qtd_restrições):
            self.model += mip.xsum(self.restricoes[i][j] * x[j] for j in range(self.qtd_variaveis)) <= self.restricoes[i][-1]
        # Resolvendo o modelo
        self.model.optimize()
        # Adicionando os resultados das variaveis na lista solucao
        for v in self.model.vars:
            self.solucao.append(v.x)

    def is_integer(self, x):
        lista_nao_inteiros = []
        for i in range(len(x)):
            if (int(x[i]) - x[i]) != 0:
                lista_nao_inteiros.append(x[i])
        return lista_nao_inteiros
    
    def var_ramification(self):
        variaveis_nao_inteiras = self.is_integer(self.solucao)
        variavel_mais_proxima_de_05 = [abs(round(x - int(x), 4) - 0.5) for x in variaveis_nao_inteiras]
        index = variavel_mais_proxima_de_05.index(min(variavel_mais_proxima_de_05))
        return variaveis_nao_inteiras[index]
    
    def subproblemas(self):
        pass

        
        

    


teste = BranchAndBoundBinary('teste1.txt')
teste.var_ramification()

        

        