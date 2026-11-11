import sys
import itertools
import numpy as np

sys.stdout.reconfigure(encoding="utf-8")

class AlgoritmoGenetico:
    def __init__(self):
        pass

    def ler_taxa(self, mensagem):
        while True:
            try:
                taxa = float(input(mensagem))
            except ValueError:
                print("Erro: digite um número válido entre 0 e 1.\n")
                continue

            if taxa < 0 or taxa > 1:
                print("Erro: a taxa deve estar entre 0 e 1.\n")
                continue

            return taxa

    def carregar_itens(self):
        itens = [
            ("Notebook", 4, 30),
            ("Camera", 2, 20),
            ("Livro", 3, 8),
            ("Garrafa", 1, 4),
            ("Casaco", 5, 14),
            ("Tenda", 8, 26),
            ("Lanterna", 1, 9),
            ("Comida", 6, 22),
            ("Violao", 7, 18),
            ("Tablet", 2, 17),
            ("Tenis", 3, 11),
            ("Fone", 1, 10),
        ]

        nomes = [item[0] for item in itens]
        pesos = [item[1] for item in itens]
        valores = [item[2] for item in itens]

        return nomes, pesos, valores

    def avaliar(self, individuo, pesos, valores, capacidade):
        peso_total = 0
        valor_total = 0
        for k in range(len(individuo)):
            if individuo[k] == 1:
                peso_total += pesos[k]
                valor_total += valores[k]

        if peso_total > capacidade:
            return 0

        return valor_total

    def selecionar(self, populacao, notas):
        a = np.random.randint(len(populacao))
        b = np.random.randint(len(populacao))

        if notas[a] >= notas[b]:
            return populacao[a].copy()
        return populacao[b].copy()

    def cruzar(self, pai, mae, taxa_cruzamento):
        if np.random.rand() > taxa_cruzamento:
            return pai.copy(), mae.copy()

        corte = np.random.randint(1, len(pai))
        filho1 = np.concatenate((pai[:corte], mae[corte:]))
        filho2 = np.concatenate((mae[:corte], pai[corte:]))

        return filho1, filho2

    def mutar(self, individuo, taxa_mutacao):
        for k in range(len(individuo)):
            if np.random.rand() < taxa_mutacao:
                individuo[k] = 1 - individuo[k]

        return individuo

    def treinamento(self, pesos, valores, capacidade, tamanho_populacao, geracoes, taxa_cruzamento, taxa_mutacao):
        self.pesos = pesos
        self.valores = valores
        self.capacidade = capacidade
        n = len(pesos)

        populacao = [np.random.randint(0, 2, n) for _ in range(tamanho_populacao)]

        melhor_individuo = None
        melhor_nota = -1

        for i in range(geracoes):
            notas = [self.avaliar(ind, pesos, valores, capacidade) for ind in populacao]

            indice_melhor = int(np.argmax(notas))
            if notas[indice_melhor] > melhor_nota:
                melhor_nota = notas[indice_melhor]
                melhor_individuo = populacao[indice_melhor].copy()

            media = sum(notas) / len(notas)

            print(f"Geração: {i}\n"
                + f"Melhor Indivíduo: {populacao[indice_melhor].tolist()}\n"
                + f"Melhor Valor da Geração: {notas[indice_melhor]}\n"
                + f"Valor Médio: {media:.2f}\n"
                + f"Melhor Valor Global: {melhor_nota}\n")

            nova_populacao = [melhor_individuo.copy()]

            while len(nova_populacao) < tamanho_populacao:
                pai = self.selecionar(populacao, notas)
                mae = self.selecionar(populacao, notas)
                filho1, filho2 = self.cruzar(pai, mae, taxa_cruzamento)
                nova_populacao.append(self.mutar(filho1, taxa_mutacao))
                if len(nova_populacao) < tamanho_populacao:
                    nova_populacao.append(self.mutar(filho2, taxa_mutacao))

            populacao = nova_populacao

        print("========FIM DO TREINAMENTO========")
        print(f"Quantidade de Gerações: {geracoes}")
        print(f"Melhor Indivíduo: {melhor_individuo.tolist()}")
        print(f"Melhor Valor: {melhor_nota}\n")

        return melhor_individuo, melhor_nota

    def melhor_solucao_exata(self, pesos, valores, capacidade):
        melhor_valor = 0
        for combinacao in itertools.product([0, 1], repeat=len(pesos)):
            valor = self.avaliar(combinacao, pesos, valores, capacidade)
            if valor > melhor_valor:
                melhor_valor = valor

        return melhor_valor

    def resultado(self, nomes, pesos, valores, individuo, nota, otimo):
        print("========RESULTADO========")
        peso_total = 0
        for k in range(len(individuo)):
            if individuo[k] == 1:
                peso_total += pesos[k]
                print(f"Item: {nomes[k]} | Peso: {pesos[k]} | Valor: {valores[k]}")

        print(f"\nPeso Total: {peso_total}")
        print(f"Valor Total: {nota}")
        print(f"Valor Ótimo (força bruta): {otimo}")
        print(f"Solução ótima encontrada: {'SIM' if nota == otimo else 'NÃO'}\n")


ag = AlgoritmoGenetico()

capacidade = int(input("Digite a capacidade da mochila: "))
tamanho_populacao = int(input("Digite o tamanho da população: "))
geracoes = int(input("Digite o número de gerações: "))
taxa_cruzamento = ag.ler_taxa("Digite a taxa de cruzamento (0 a 1): ")
taxa_mutacao = ag.ler_taxa("Digite a taxa de mutação (0 a 1): ")

nomes, pesos, valores = ag.carregar_itens()
melhor_individuo, melhor_nota = ag.treinamento(pesos, valores, capacidade, tamanho_populacao, geracoes, taxa_cruzamento, taxa_mutacao)

otimo = ag.melhor_solucao_exata(pesos, valores, capacidade)
ag.resultado(nomes, pesos, valores, melhor_individuo, melhor_nota, otimo)
