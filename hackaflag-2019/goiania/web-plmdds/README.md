# plmdds

- Desafio da etapa de Goiânia do Hackaflag 2019
- Data do desafio: 2019-06-01
- Categoria: web
- URL original: `http://68.183.31.62:7456/`

## Análise

A URL leva a uma página com a mensagem "welcome to this easy challenge :D!". Ao inspecionar o código-fonte, encontramos um código JavaScript ofuscado. Este tipo de desafio requer fluência e conhecimento de recursos mais obscuros da linguagem para entender o código e identificar trechos suspeitos. 

Para facilitar a análise, podemos utilizar programas ou serviços que formatam e tentam desofuscar o código. O navegador Chrome, por exemplo, permite formatar (_pretty-print_) o código na aba _Sources_ das ferramentas de desenvolvedor.

### Técnicas de ofuscação

O código começa com um array `_0x439c` contendo várias strings em base 64. Se tentarmos decodificá-las, não obteremos nada relevante. Este array só aparece mais duas vezes no código: em uma função anônima que rotaciona os elementos do array e na função `_0x3414`, que é chamada várias vezes ao longo do código. Se executarmos no console do navegador algumas chamadas dessa função, percebermos que é uma forma de ofuscar strings. Por exemplo, `_0x3414('0x73', 'jO#I')` retorna `charCodeAt`, uma função do JavaScript.

Outra função do código que é utilizada da mesma forma é `_0x56ae`. `_0x56ae(_0x3414('0x7e', 'jO#I'), _0x3414('0x7f', 'xGlY'))`, por exemplo, retorna `location`.

Um trecho suspeito do código consiste em três `if`s aninhados com um método do objeto `console` (possivelmente `console.log`, utilizado para saída no console) e um trecho uniforme de código. Antes deste trecho, há o comando `window[_0x56ae(_0x3414('0x89', '!V3('), _0x3414('0x8a', 'h(Gl'))] = function() { ...`, sendo que `_0x56ae(_0x3414('0x89', '!V3('), _0x3414('0x8a', 'h(Gl'))` corresponde à string `onload`, portanto estes testes provavelmente estão sendo executados assim que a página é carregada. Vamos analisar este trecho.

### Primeiro `if`

```js
if (location[_0x56ae(_0x3414('0x8b', '&5Z1'), _0x3414('0x8c', 's712'))][_0x56ae(_0x3414('0x8d', '&5Z1'), _0x3414('0x8e', '&5Z1'))](0x1) === String[_0x56ae(_0x3414('0x8f', '(fvJ'), 'Yi1V')](0x48, 0x41, 0x43, 0x4b, 0x41, 0x46, 0x4c, 0x41, 0x47))
```

Executando no console cada ocorrência de `_0x56ae`, obtemos as seguintes strings:

- `[_0x56ae(_0x3414('0x8b', '&5Z1'), _0x3414('0x8c', 's712'))]` = `hash`
- `[_0x56ae(_0x3414('0x8d', '&5Z1'), _0x3414('0x8e', '&5Z1'))]` = `substr`
- `[_0x56ae(_0x3414('0x8f', '(fvJ'), 'Yi1V')]` = `fromCharCode`

O código desofuscado é `if (location.hash.substr(1) === String.fromCharCode(0x48, 0x41, 0x43, 0x4b, 0x41, 0x46, 0x4c, 0x41, 0x47)` ou, mais simplesmente `if (location.hash.substr(1) === "HACKAFLAG"`, que verifica se há a âncora `#HACKAFLAG` na URL.

### Segundo `if`

```js
if (window[_0x56ae(_0x3414('0x90', 'A#iH'), 'DFTS')][_0x56ae(_0x3414('0x91', 'sUOz'), 'BakY')] > 0x14)
```

O código desofuscado é `if (window.name.length > 20)`. A propriedade `window.name` geralmente é definida por uma página que abre outra. Podemos definir esta propriedade usando a função `window.open("URL", "nome maior que 20 caracteres")` e verificando o valor de `window.name` no console da página aberta.

### Terceiro `if`

```js
if (_0x1bc67d[_0x56ae(_0x3414('0x92', '$qgC'), 'gQAR')] === String[_0x3414('0x93', '4tCn')](0x68, 0x61, 0x63, 0x6b, 0x61, 0x66, 0x6c, 0x61, 0x67, 0x2e, 0x63, 0x6f, 0x6d))
```

Neste `if` a função `_0x1bc67d` é utilizada, e antes dos `if`s é definida como `var _0x1bc67d = x()`. Precisamos entender o que a função `x` faz.

#### Função `x`

```js
window[_0x56ae(_0x3414('0x7e', 'jO#I'), _0x3414('0x7f', 'xGlY'))][_0x56ae(_0x3414('0x80', 'O[&m'), _0x3414('0x81', 'EDHq'))][_0x3414('0x82', 'A#iH')]('?', '')[_0x56ae(_0x3414('0x83', '!WGQ'), _0x3414('0x84', '6@7O'))]('&')[_0x56ae(_0x3414('0x85', 'h(Gl'), _0x3414('0x86', 'xGlY'))]
```

Executando cada trecho:

- `_0x56ae(_0x3414('0x7e', 'jO#I'), _0x3414('0x7f', 'xGlY'))` = `location`
- `_0x56ae(_0x3414('0x80', 'O[&m'), _0x3414('0x81', 'EDHq'))` = `search`
- `_0x3414('0x82', 'A#iH')` = `replace`
- `_0x56ae(_0x3414('0x83', '!WGQ'), _0x3414('0x84', '6@7O'))` = `split`
- `_0x56ae(_0x3414('0x85', 'h(Gl'), _0x3414('0x86', 'xGlY'))` = `forEach`

A função final é `window.location.search.replace('?', '').split('&').forEach`. O método `forEach` recebe uma função que será executada para cada elemento do array (neste caso, para cada parâmetro e valor na URL). A função fornecida é:

```js
function(_0x173872) {
	var _0x450119;
	return _0x450119 = _0x173872[_0x56ae(_0x3414('0x87', 'kxF)'), _0x3414('0x88', 'ZwUW'))]('='),
		_0x3f5eff[_0x450119[0x0]] = _0x450119[0x1];
	}
```

O trecho `_0x56ae(_0x3414('0x87', 'kxF)'), _0x3414('0x88', 'ZwUW'))` é igual a `split`. A função recebe uma string (representada por `_0x173872`), separa o par `parametro=valor` pelo caractere `=` e insere o valor no array `_0x3f5eff` no formato `_0x3f5eff["parametro"] = valor`. Portanto, a função `x` retorna um array com os pares de parâmetro e valor da URL.

#### Voltando ao terceiro `if`

```js
if (_0x1bc67d[_0x56ae(_0x3414('0x92', '$qgC'), 'gQAR')] === String[_0x3414('0x93', '4tCn')](0x68, 0x61, 0x63, 0x6b, 0x61, 0x66, 0x6c, 0x61, 0x67, 0x2e, 0x63, 0x6f, 0x6d))
```

- `_0x56ae(_0x3414('0x92', '$qgC'), 'gQAR')` = `redirect`
- `_0x3414('0x93', '4tCn')` = `fromCharCode`
- `String.fromCharCode(0x68, 0x61, 0x63, 0x6b, 0x61, 0x66, 0x6c, 0x61, 0x67, 0x2e, 0x63, 0x6f, 0x6d)` = `hackaflag.com`

Este `if` verifica se há um parâmtro `redirect` na URL com o valor `hackaflag.com`. Em código: `if (arrayDeParametros["redirect"] === "hackaflag.com")`. Portanto, basta acresentar `?redirect=hackaflag.com` na nossa URL.

### Solução

Agora que identificamos os testes realizados, o payload consiste em inserir o seguinte comando no console do navegador:

```js
window.open("index.html?redirect=hackaflag.com#HACKAFLAG", "nome maior que 20 caracteres")
```

Um `alert` executado contendo a flag `HACKAFLAG{1ts_n0t_4_XSS_challenge}`.

### Bypass

Há uma forma mais simples de encontrar a flag. Em vez de avaliar o que cada `if` faz, podemos simplesmente copiar o conteúdo dentro dos `if`s e executá-lo no console do navegador, obtendo a flag. O código poderia não funcionar caso um dos valores não fosse o esperado, mas neste caso funciona sem problemas.
