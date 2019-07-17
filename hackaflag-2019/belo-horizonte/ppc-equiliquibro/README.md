# Equilíquibro

- Desafio da etapa de Belo Horizonte do Hackaflag 2019
- Data do desafio: 2019-06-29
- Categoria: PPC
- Endereço original: IP: 142.93.73.149 Porta: 12969

## Análise do problema

Para entender melhor este desafio, vamos criar duas variáveis: `sobra` e `falta`. Para um valor `n` qualquer, `sobra` é a quantidade de líquido que está acima de `n` e `falta` é a quantidade de líquido que falta para chegar a `n`.

O cálculo é simples: basta subtrair `n` de cada valor da lista; a soma dos valores positivos é a `sobra` e a soma dos valores negativos é a `falta`. No exemplo \[1, 2, 4, 8\], para `n` = 3, a subtração resulta em \[-2, -1, 1, 5\] e, portanto, a `sobra` é (1 + 5) = 6 e a `falta` é (-2 + -1) = -3. O objetivo, então, é encontrar um valor `n` tal que `sobra/2 + falta = 0`, com margem de erro de ±0.001.

Ilustração do exemplo \[-2, -1, 1, 5\] para `n` = 3:

```
[ ] => não muda
[-] => sobra
(+) => falta

             [-]
             [-]
             [-]
             [-]
         [-] [-]
 (+) (+) [ ] [ ]
 (+) [ ] [ ] [ ]
 [ ] [ ] [ ] [ ]
```

O próximo passo é perceber que, se aumentarmos `n`, `sobra` e `falta` sempre diminuem; da mesma forma, se diminuirmos `n`, `sobra` e `falta` sempre aumentam. Uma função com esta propriedade é chamada de [função monotônica](https://en.wikipedia.org/wiki/Monotonic_function) e, neste caso, é útil porque podemos nos aproximar do valor desejado usando uma [busca binária](https://en.wikipedia.org/wiki/Binary_search_algorithm).

Agora, precisamos definir os limites superior e inferior. O limite superior pode ser a média simples dos elementos da lista, já que esta seria a solução se não houvesse desperdício; como há desperdício, a solução certamente será menor que a média simples. O limite inferior pode ser 0, pois um copo não pode ter uma quantidade negativa de líquido (isto é diferente de representar a quantidade que falta como um número negativo). Quaisquer que sejam os limites, se a solução estiver dentro do intervalo, a busca binária rapidamente convergerá para ela.

## Implementação

A função `tentativa` realiza recursivamente uma busca binária na lista informada e retorna o primeiro valor com diferença inferior a 0.001: 

```python
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
```

Com esta solução, obtemos a flag `HACKAFLAG{NJQWQ5DFNZZWCZTMMFTW4ZJ7}`.