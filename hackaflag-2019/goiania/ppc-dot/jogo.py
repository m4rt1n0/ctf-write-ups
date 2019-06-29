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