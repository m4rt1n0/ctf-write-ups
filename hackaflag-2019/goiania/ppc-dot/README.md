# .

- Desafio da etapa de Goiânia do Hackaflag 2019
- Data do desafio: 2019-06-01
- Categoria: PPC
- Endereço original: 142.93.73.149 10169

## Cadê o enunciado?

Diferentemente dos desafios anteriores desta categoria, este não possui descrição. Assim, parte do desafio consiste em entender o comportamento do programa apenas por tentativa e erro, como uma caixa preta. A seguir, os resultados de algumas partidas feitas manualmente:

```
 [+] 1 / 25
 [+] 01101
 [+] Pretende jogar? (sim, nao): sim
     Posição: 2
 [+] 00X11
     Posição: 3
 [+] 00XX0
     Posição: 4
 [-] Opção inválida.
     Saindo
```

```
 [+] 1 / 25
 [+] 00100
 [+] Pretende jogar? (sim, nao): sim
     Posição: 2
 [+] 01X10
     Posição: 2
 [-] Opção inválida.
```

```
 [+] 1 / 25
 [+] 00111
 [+] Pretende jogar? (sim, nao): sim
     Posição: 4
 [+] 0010X
     Posição: 2
 [+] 01X1X
     Posição: 3
 [+] 01XXX
     Posição: 1
 [+] 1XXXX
     Posição: 0
 [+] XXXXX
 [+] 2 / 25
 [+] 10100
 [+] Pretende jogar? (sim, nao): sim
     Posição: 2
 [+] 11X10
     Posição: 3
 [+] 11XX1
     Posição: 4
 [+] 11XXX
     Posição: 1
 [+] 0XXXX
     Posição: 0
 [-] Opção inválida.
```

```
 [+] Para começar, digite start: start
     Iniciando...
 [+] 1 / 25
 [+] 00010
 [+] Pretende jogar? (sim, nao): nao

 [+] 2 / 25
 [+] 00110
 [+] Pretende jogar? (sim, nao): nao

 [+] 3 / 25
 [+] 00110
 [+] Pretende jogar? (sim, nao): nao

 [+] 4 / 25
 [+] 00100
 [+] Pretende jogar? (sim, nao): nao

 [+] 5 / 25
 [+] 11100
 [+] Pretende jogar? (sim, nao): nao

 [+] 6 / 25
 [+] 1101010
 [+] Pretende jogar? (sim, nao): nao

 [+] 7 / 25
 [+] 1010000110
 [+] Pretende jogar? (sim, nao): nao

 [+] 8 / 25
 [+] 0111000
 [+] Pretende jogar? (sim, nao): nao

 [+] 9 / 25
 [+] 1100101010
 [+] Pretende jogar? (sim, nao): nao

 [+] 10 / 25
 [+] 00100011
 [+] Pretende jogar? (sim, nao): nao

 [+] 11 / 25
 [+] 1100000011100110001101101
 [+] Pretende jogar? (sim, nao): nao

 [+] 12 / 25
 [+] 1011110101011111000101010
 [+] Pretende jogar? (sim, nao): nao

 [+] 13 / 25
 [+] 1101100100110100010100
     Posição:    
 [-] Uops!...
     Encerrando a conexão...
```

A partir destes resultados, podemos descobrir algumas regras do jogo:

- são 25 rodadas;
- o jogador deve escolher se vai jogar ou não;
- é possível deixar de jogar até 12 partidas;
- as posições começam a contagem a partir de 0;
- só é possível escolher uma posição com o caractere `1`;
- ao escolher uma posição, ela muda para `X` e os bits vizinhos são invertidos (o `X` é ignorado);
- o objetivo é transformar todas as posições em `X`;
- na última rodada, não é perguntado se você pretende jogar (e você muito provavelmente só vai descobrir isso no fim).

## Algoritmo

Agora que conhecemos o problema, precisamos pensar em um algoritmo que decida quando jogar e quais posições escolher. Para isso, podemos simular alguns cenários para testar hipóteses.

```
00100 -> 2
01X10 -> 1
1XX10 -> 0
XXX10 -> 3
XXXX1 -> 4
XXXXX -> vitória
```

Quando há apenas um `1`, há um efeito de gerar novos `1` em direção às bordas e a solução é simples.

```
01010 -> 1
1X110 -> 0
XX110 -> 2
XXX00 -> derrota
```

```
01010 -> 1
1X110 -> 0
XX110 -> 3
XX0X0 -> derrota
```

Quando há uma quantidade par de `1`, não é possível ganhar.

```
01110 -> 2
00X00 -> derrota
```

```
01110 -> 1
1X010 -> 0
XX010 -> 3
XX1X1 -> 2
XXXX1 -> 4
XXXXX -> vitória
```

Ao escolher o `1` que está no meio, perdemos. Se escolhermos apenas os `1` que estiverem nas pontas, ganhamos.

Assim, a estratégia é não jogar jogos com uma quantidade par de `1` e sempre escolher os `1` externos. Para facilitar, vamos escolher sempre o primeiro `1` à esquerda.

## Implementação

Com o algoritmo definido, resta implementar e executar para obter a flag. A seguir, uma possível implementação:

```python
import sys
import telnetlib
import math

host = '142.93.73.149'
port = 10169

connection = telnetlib.Telnet(host, port)
print(connection.read_until('start: '))
connection.write('start')

# Joga por 25 rodadas
for rodadas in range(1, 26):
	entrada = connection.read_until(': ')
	print('[Entrada] ' + entrada)

	# Obtem a sequencia a partir do conteudo lido
	seq = entrada.splitlines()[2].split()[1]

	# Na ultima rodada nao ha pergunta
	if (rodadas < 25):
		# Se qtde de '1' for par, nao joga
		if not bool(seq.count('1') % 2):
			connection.write('nao')
			print('[Resposta] nao')
			continue	
		else:
			connection.write('sim')
			print('[Resposta] sim')

			entrada = connection.read_until(': ')
			print(entrada)

	# Faz a primeira jogada
	posicao = seq.find('1')
	connection.write(str(posicao))
	print('[Jogada] ' + str(posicao))

	tamanho = len(seq)

	# Faz as jogadas restantes
	for i in range(0, tamanho - 1):
		entrada = connection.read_until(': ')
		print(entrada)

		# Obtem o proximo estado da sequencia
		seq = entrada.splitlines()[0].split()[1]

		posicao = seq.find('1')
		connection.write(str(posicao))
		print('[Jogada] ' + str(posicao))

# Exibe a flag
entrada = connection.read_until('}')
print(entrada)

connection.close()
```

Finalmente, obtemos a flag `HACKAFLAG{KNCU2RCFKNBVESODQ7BYGT3NGRZWC2LOMRQXA33TONUXMZLM}`.
