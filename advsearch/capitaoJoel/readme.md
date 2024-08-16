Fernando Mello 00341727 - Henrique Lindemann 00343234 - Luca Fritscher 00343044
Turma B

Bibliotecas: não foram adicionadas bibliotecas extras


a)
(i) não, o minimax nem sempre ganha do random player,
em algumas instâncias (poucas), os movimentos aleatórios
levam a um empate, mas nunca (nas várias simulações) resultou
em uma vitória.

(ii) Sim, em todas vezes que simulei o minimax contra o minimax
ocorreu um empate.

(iii) Quando eu uso a melhor estratégia, eu sempre empato com a IA, 
espero que isso não significa que eu não sei jogar, mas que a IA que 
fizemos é muito avançada ;)

b)
Contagem de peças X Valor posicional: count
Valor posicional X Contagem de peças: count
Contagem de peças X Heurística customizada: custom
Heurística customizada X Contagem de peças: custom
Valor posicional X Heurística customizada: custom
Heurística customizada X Valor posicional: custom 

Observando, fica claro que nossa IA, capitãoJoel é a melhor das 3 :)

--

A estratégia utilizada combina várias ideias de estratégias para othello, como:
-cantos:  peças nos cantos não podem ser capturadas facilmente
-bordas: controlar as bordas aumenta a estabilidade e reduz as opções de movimento do oponente
-mobilidade: maior mobilidade dá mais opções táticas e reduz as jogadas possíveis do oponente
-estabilidade: peças estáveis são difíceis de capturar
-paridade: se numero de jogadas restantes favorece ou não o oponente
-posição no tabuleiro (usando template da mask)

Para o desenvolvimento usando essas estratégias, foram utilizadas LLMs em um esforço 
contínuo para melhorar o código e debugga-lo. Desse modo, ela foi um esforço nosso, do
grupo além dos seguintes modelos de linguagem natural: GPT-4o-Latest-128K e 
Claude-3.5-Sonnet-200k

O critério de parada é max_depth 5, o que irá simular até 2,5 rodadas. Quando colocava-mos 4, 
o algoritmo sempre perdia as partidas, e com 6 ele passava do tempo limite.




