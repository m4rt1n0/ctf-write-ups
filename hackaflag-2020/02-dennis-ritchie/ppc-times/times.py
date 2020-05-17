import sys
import telnetlib
import math

host = '142.93.73.149'
port = 15052

connection = telnetlib.Telnet(host, port)
print(connection.read_until('ar: '))
connection.write('start')

while True:
  print(connection.read_until('Jogadores: '))
  entrada = connection.read_until(']\n')
  print(entrada)
  print(connection.read_until(': '))
  
  lista = eval(entrada)
  conjunto = set(lista)
  maior = max([lista.count(item) for item in conjunto])
  categorias = len(conjunto)
  minimo = min([maior, categorias])
  if maior == categorias:
    minimo -= 1
  resposta = minimo
  
  print('Resposta: ' + str(resposta))
  connection.write(str(int(resposta)))

connection.close()
