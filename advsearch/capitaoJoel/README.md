# README

**Fernando Mello (00341727)**

**Henrique Lindemann (00343234)**

**Luca Fritscher (00343044)**

Turma B

## Bibliotecas

Não foram adicionadas bibliotecas extras.

---

### a)

**(i)** Não, o minimax nem sempre ganha do random player. Em algumas instâncias (poucas), os movimentos aleatórios levam a um empate, mas nunca (nas várias simulações) resultou em uma vitória.

**(ii)** Sim, em todas as vezes que simulei o minimax contra o minimax, ocorreu um empate.

**(iii)** Quando eu uso a melhor estratégia, eu sempre empato com a IA. Espero que isso não significa que eu não sei jogar, mas que a IA que fizemos é muito avançada ;)

### b)

- **Contagem de peças X Valor posicional:** `count`
- **Valor posicional X Contagem de peças:** `count`
- **Contagem de peças X Heurística customizada:** `custom`
- **Heurística customizada X Contagem de peças:** `custom`
- **Valor posicional X Heurística customizada:** `custom`
- **Heurística customizada X Valor posicional:** `custom`

Observando, fica claro que nossa IA, *capitãoJoel* é a melhor das três :)

---

## Estratégia Utilizada

A estratégia utilizada combina várias ideias de estratégias para Othello, como:

- **Cantos:** Peças nos cantos não podem ser capturadas facilmente.
- **Bordas:** Controlar as bordas aumenta a estabilidade e reduz as opções de movimento do oponente.
- **Mobilidade:** Maior mobilidade dá mais opções táticas e reduz as jogadas possíveis do oponente.
- **Estabilidade:** Peças estáveis são difíceis de capturar.
- **Paridade:** Considera se o número de jogadas restantes favorece ou não o oponente.
- **Posição no Tabuleiro:** Usando template da máscara (*mask*).

Para o desenvolvimento usando essas estratégias, foram utilizadas LLMs em um esforço contínuo para melhorar o código e depurá-lo. Desse modo, ela foi um esforço nosso, do grupo, além dos seguintes modelos de linguagem natural: **GPT-4o-Latest-128K** e **Claude-3.5-Sonnet-200k**.

### Critério de Parada

O critério de parada é `max_depth 5`, o que irá simular até 2,5 rodadas. Quando colocávamos 4, o algoritmo sempre perdia as partidas, e com 6 ele passava do tempo limite.
