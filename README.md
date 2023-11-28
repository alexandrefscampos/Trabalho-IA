# Trabalho de MATA64 - Inteligência artificial

# Trabalho de Redes - MATA59
##  Alunos: Alexandre Campos, Pedro Beckhauser

Neste trabalho nossa equipe implementou algoritmos de IA que visam resolver o jogo 2048, foram implementados os algoritmos de busca gulosa e diferença temporal. A linguagem escolhada para a realização do trabalho foi o python.

Para rodar é necessário ter o python instalado em sua máquina, para o passso-a-passo consulte [este link](https://www.python.org/downloads/).
Nosso projeto tem como dependência alguns pacotes, para instalar rode:

```
pip3 install numpy
pip3 install pygame
pip3 install matplotlib
```

Para rodar nosso projeto temos 3 principais funcionalidades, no arquivo `play.py`, que estarão comentadas.


Caso queira jogar o 2048 propriamente dito:
```
gameLoop()
```
Comandos: Cima, Baixo, Esquerda, Direita para movimentação, R para resetar e Espaço para ativar a AI guloas.

Caso queira rodar nossos benchmarks de diferença temporal:
```
scores = run_games_and_store_scores(use_reinforced_learning=True, num_games=num_games)
plot_scores(scores, output_filename="time_diffence_histogram.png", algorithm="diferença temporal", num_games=num_games)
```

Caso queira rodar nossos benchmarks de diferença temporal:
```
scores = run_games_and_store_scores(num_games=num_games)
plot_scores(scores, output_filename="greedy_histogram.png", num_games=num_games)
```
