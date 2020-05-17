# Times

- Data do desafio: 2020-05-15
- Categoria: PPC
- Endereço original: 142.93.73.149:15052

```
                    +++     HACKAFLAG - Times     +++

 [+] Esse ano, as competições de CTF estão aparecendo das formas mais diferentes 
     possíveis. Para entrar no ritmo, o Roadsec também resolveu fazer alguns
     testes de competições onde eles mesmos realizam a separação dos times, a
     partir dos competidores cadastrados. A dúvida que apareceu foi: qual a
     melhor forma de dividir os competidores?

 [+] Para descobrir a resposta, eles decidiram fazer o seguinte experimento: 
     dada a especialidade de cada jogador, dividir todos os competidores
     cadastrados em dois times com a mesma quantiade, onde em um time todos os
     competidores deverão possuir a mesma especialidade; e no outro time, todos
     os competidores deverão possuir, necessariamente, especialidades diferentes
     uns dos outros.

 [+] Dessa forma, sua ajuda foi solicitada para responder a seguinte  pergunta:
     dada a lista de competidores, qual a quantidade máxima de jogadores para
     cada time é possível, cumprindo os requisitos apresentados?
 
 [+] Digite 'start' para começar:
```

Em cada etapa, vamos receber uma lista (por exemplo: `['crypto', 'for', 'rev', 'web', 'web', 'web']`) e precisamos de duas informações: quantas categorias existem e a maior ocorrência de uma mesma categoria. Se a variável `lista` for a entrada, podemos definir `conjunto = set(lista)` e achar os dois valores:

- `categorias = len(conjunto)`
- `maior = max([lista.count(item) for item in conjunto])`

Se os valores forem diferentes, a resposta será o menor valor. Se os valores forem iguais, precisamos subtrair 1 do valor, porque um dos jogadores não poderá ficar nos dois times.

O código fica assim:

```python
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
```

Flag: `HACKAFLAG{IIYECICKGBDUCRBQKIQSCIBSGM3TIOJTHA3TEOIK}`