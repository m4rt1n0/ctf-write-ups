import sys
import telnetlib
import math

host = '142.93.73.149'
port = 12969

def tentativa(lista, inicio, fim):
	media = (inicio + fim)/2.0
	sobra = 0.0
	falta = 0.0
	for item in lista:
		if item > media:
			sobra += (item - media)
		else:
			falta += (item - media)
	diferenca = sobra/2.0 + falta
	print('Media: %.3f Sobra: %.3f Falta: %.3f Diferenca: %.4f' % (media, sobra, falta, diferenca))
	if abs(diferenca) < 0.001:
		return media
	if diferenca > 0:
		return tentativa(lista, media, fim)
	else:
		return tentativa(lista, inicio, media)

connection = telnetlib.Telnet(host, port)
print(connection.read_until('start: '))
connection.write('start')

for i in range(0, 25):
	print(connection.read_until(': '))
	entrada = connection.read_until(']')
	print(entrada)
	print(connection.read_until(': '))

	lista = eval(entrada)
	lista.sort()

	media = float(reduce(lambda x, y: x + y, lista) / float(len(lista)))

	resposta = tentativa(lista, 0, media)

	str_resposta = '%.3f' % resposta

	print('Resposta: ' + str_resposta)
	connection.write(str_resposta)

print(connection.read_until('}'))

connection.close()