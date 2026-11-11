# Algoritmo Genético - Problema da Mochila

Trabalho de Inteligência Artificial. Implementação simples de um Algoritmo Genético em Python, sem usar bibliotecas prontas de otimização (só numpy para números aleatórios e vetores).

## O problema

Problema da Mochila (*Knapsack*): existem 12 itens, cada um com um **peso** e um **valor**. A mochila aguenta uma **capacidade** máxima de peso (informada pelo usuário). O objetivo é escolher quais itens levar de forma que o **valor total seja o maior possível** sem ultrapassar a capacidade.

| Item     | Peso | Valor |
|----------|------|-------|
| Notebook | 4    | 30    |
| Camera   | 2    | 20    |
| Livro    | 3    | 8     |
| Garrafa  | 1    | 4     |
| Casaco   | 5    | 14    |
| Tenda    | 8    | 26    |
| Lanterna | 1    | 9     |
| Comida   | 6    | 22    |
| Violao   | 7    | 18    |
| Tablet   | 2    | 17    |
| Tenis    | 3    | 11    |
| Fone     | 1    | 10    |

Com 12 itens existem 2^12 = 4096 combinações possíveis, o que permite conferir o resultado do algoritmo genético contra a solução exata (força bruta).

## Como funciona

### Representação

Cada **indivíduo** é uma lista de 12 valores 0 ou 1, um por item. `1` significa que o item está na mochila e `0` que ficou de fora. Exemplo: `[1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1]`.

### Treinamento (evolução)

1. O usuário informa, no início da execução, a **capacidade da mochila**, o **tamanho da população**, o **número de gerações**, a **taxa de cruzamento** e a **taxa de mutação**.
2. A população inicial é criada com indivíduos aleatórios.
3. Cada indivíduo é avaliado pela função de aptidão (*fitness*):
   ```
   aptidão = soma dos valores dos itens escolhidos   se peso total <= capacidade
   aptidão = 0                                       se peso total >  capacidade
   ```
4. **Elitismo**: o melhor indivíduo encontrado até o momento passa direto para a próxima geração.
5. **Seleção por torneio**: dois indivíduos são sorteados e o de maior aptidão vira pai (o mesmo processo escolhe a mãe).
6. **Cruzamento de ponto único**: com probabilidade igual à taxa de cruzamento, sorteia-se um ponto de corte e os filhos trocam as partes dos pais:
   ```
   pai:    1 1 0 | 0 1 0
   mae:    0 0 1 | 1 1 1
   filho1: 1 1 0 | 1 1 1
   filho2: 0 0 1 | 0 1 0
   ```
7. **Mutação**: cada gene do filho tem probabilidade igual à taxa de mutação de ser invertido (`0` vira `1` e `1` vira `0`).
8. Os filhos formam a nova população e o processo se repete pelo número de gerações informado.
9. A cada geração são exibidos o melhor indivíduo, o melhor valor da geração, o valor médio da população e o melhor valor global.

### Resultado

Ao final, o programa mostra os itens escolhidos, o peso total, o valor total e compara com o valor ótimo calculado por força bruta, informando se o algoritmo genético encontrou a solução ótima.

## Estrutura

- `AlgoritmoGenetico.ler_taxa(mensagem)`: lê a taxa digitada e, se não for um número entre 0 e 1, exibe uma mensagem de erro e pergunta de novo.
- `AlgoritmoGenetico.carregar_itens()`: retorna nomes, pesos e valores dos itens.
- `AlgoritmoGenetico.avaliar(individuo, pesos, valores, capacidade)`: calcula a aptidão de um indivíduo.
- `AlgoritmoGenetico.selecionar(populacao, notas)`: seleção por torneio.
- `AlgoritmoGenetico.cruzar(pai, mae, taxa_cruzamento)`: cruzamento de ponto único.
- `AlgoritmoGenetico.mutar(individuo, taxa_mutacao)`: mutação por inversão de bits.
- `AlgoritmoGenetico.treinamento(...)`: executa a evolução e retorna o melhor indivíduo e seu valor.
- `AlgoritmoGenetico.melhor_solucao_exata(pesos, valores, capacidade)`: testa todas as combinações para obter o valor ótimo.
- `AlgoritmoGenetico.resultado(...)`: exibe os itens escolhidos e a comparação com o ótimo.

## Como rodar

Precisa do Python instalado e da biblioteca abaixo:

```
pip install numpy
```

Depois é só rodar:

```
python main.py
```

O programa pede os parâmetros. Sugestão de valores para teste:

```
Capacidade da mochila: 20
Tamanho da população: 30
Número de gerações: 30
Taxa de cruzamento: 0.8
Taxa de mutação: 0.05
```