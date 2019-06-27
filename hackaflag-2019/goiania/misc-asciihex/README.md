# ASCIIHEX

- Desafio da etapa de Goiânia do Hackaflag 2019
- Data do desafio: 2019-06-01
- Categoria: misc
- Arquivo fornecido: `flag.txt`

## Arquivo `flag.txt`

O arquivo possui ASCII art de diversas teclas representando caracteres hexadecimais, de forma que não é possível obter a string hexadecimal diretamente. Cada tecla tem 20 caracteres de largura e 11 caracteres de altura. Cada linha possui 25200, o que indica que há um total de 1260 caracteres hexadecimais.

```
 .----------------.  .----------------. 
| .--------------. || .--------------. |
| |   _______    | || |   _    _     | |
| |  |  _____|   | || |  | |  | |    | |
| |  | |____     | || |  | |__| |_   | |
| |  '_.____''.  | || |  |____   _|  | | . . .
| |  | \____) |  | || |      _| |_   | |
| |   \______.'  | || |     |_____|  | |
| |              | || |              | |
| '--------------' || '--------------' |
 '----------------'  '----------------' 
```

Há várias formas de resolver este desafio. Neste write-up, modificaremos o arquivo para que cada tecla apareça verticalmente após a anterior, permitindo processar linearmente cada tecla. Para isto, usaremos um pequeno script em Python que armazena cada tecla e em seguida imprime no formato desejado.

```python
f = open('flag.txt', 'r')

linhas = {}

x = f.readline()
for i in range(2, 13):
	linhas[i] = f.readline()

while len(linhas[2]) > 10:
	for i in range(2, 13):
		print(linhas[i][:20])
		linhas[i] = linhas[i][20:]
```

Neste novo formato, podemos selecionar a ASCII art de uma tecla e substituir todas as ocorrências dela por um único caractere com o valor representado na tecla. Como são apenas caracteres hexadecimais, o processo pode ser feito manualmente sem tomar muito tempo. Cada caractere estará em uma linha, então basta remover todas as ocorrências de nova linha (`\n`). Ao fim, devemos ter 1260 caracteres hexadecimais (aqui divididos em linhas para melhor apresentação):

```
54686973206973206F757220776F726C64206E6F7720262074686520776F726C64206F6620746865
20656C656374726F6E20616E6420746865207377697463682C2074686520626561757479206F6620
74686520626175642E205765206D616B6520757365206F662061207365727669636520616C726561
6479206578697374696E6720776974686F757420706179696E6720666F72207768617420636F756C
6420626520646972742D6368656170206966206974207761736E2019742072756E2062792070726F
666974656572696E6720676C7574746F6E732C20616E6420796F752063616C6C207573206372696D
696E616C732E205765206578706C6F7265202620616E6420796F752063616C6C207573206372696D
696E616C73204841434B41464C41477B456173795F676F69616E69615F323031395F686578626C6F
636B737D202E205765207365656B206166746572206B6E6F776C65646765202620616E6420796F75
2063616C6C207573206372696D696E616C732E20576520657869737420776974686F757420736B69
6E20636F6C6F722C20776974686F7574206E6174696F6E616C6974792C20776974686F7574207265
6C6967696F75732062696173202620616E6420796F752063616C6C207573206372696D696E616C73
2E20596F75206275696C642061746F6D696320626F6D62732C20796F75207761676520776172732C
20796F75206D75726465722C2063686561742C20616E64206C696520746F20757320616E64207472
7920746F206D616B652075732062656C6965766520697420197320666F72206F7572206F776E2067
6F6F642C207965742077652019726520746865206372696D696E616C732E
```

Convertendo os bytes para caracteres ASCII (como o nome do desafio sugere), obtemos (com alguns erros no caractere `'`) um trecho do [Hacker Manifesto](https://archive.org/stream/The_Conscience_of_a_Hacker/hackersmanifesto.txt) com a flag escondida no meio.

```
This is our world now & the world of the electron and the switch, the beauty of the baud. We make use of a service already existing without paying for what could be dirt-cheap if it wasn t run by profiteering gluttons, and you call us criminals. We explore & and you call us criminals HACKAFLAG{Easy_goiania_2019_hexblocks} . We seek after knowledge & and you call us criminals. We exist without skin color, without nationality, without religious bias & and you call us criminals. You build atomic bombs, you wage wars, you murder, cheat, and lie to us and try to make us believe it s for our own good, yet we re the criminals.
```
