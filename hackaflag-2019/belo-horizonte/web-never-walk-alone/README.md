# Never walk alone

- Desafio da etapa de Belo Horizonte do Hackaflag 2019
- Data do desafio: 2019-06-29
- Categoria: web
- URL original: `http://68.183.31.62:33332/cfcd208495d565ef66e7dff9f98764da.php`

A URL nos leva a uma página chama `c4ca4238a0b923820dcc509a6f75849b.php` com um link para outra página, `c81e728d9d4c2f636f067f89cc14862c.php`. Nesta outra página, encontramos outro link para outra página, `eccbc87e4b5ce2fe28308fd9f2a7baf3.php`, e assim continuamos indefinidamente.

Poderíamos automatizar o percorrimento destes links, mas é mais eficiente (e interessante) entender a lógica deles. Procurando pelos nomes dos arquivos, percebemos que se tratam dos hashes MD5 dos números 0, 1, 2, 3 etc.

```
$ echo -n "0" | md5sum
cfcd208495d565ef66e7dff9f98764da  -
$ echo -n "1" | md5sum
c4ca4238a0b923820dcc509a6f75849b  -
$ echo -n "2" | md5sum
c81e728d9d4c2f636f067f89cc14862c  -
$ echo -n "3" | md5sum
eccbc87e4b5ce2fe28308fd9f2a7baf3  -
```

Assim, fica muito mais fácil encontrar a última página, testando valores e realizando uma busca binária. A página 500, por exemplo, deverá se chamar `cee631121c2ec9232f3a2f028ad5c89b.php`.

Se tentarmos acessar estas páginas diretamente, a resposta do servidor será vazia. Inspecionando a diferença entre as chamadas, é possível encontrar o cabeçalho `Referer` da página anterior. Vamos tentar acessar a página 500 inserindo como referrer a página 499. Sendo `md5(500) = cee631121c2ec9232f3a2f028ad5c89b.php` e `md5(499) = 3cf166c6b73f030b4f67eeaeba301103`, a chamada será `curl -e http://68.183.31.62:33332/3cf166c6b73f030b4f67eeaeba301103.php http://68.183.31.62:33332/cee631121c2ec9232f3a2f028ad5c89b.php`. Obtemos uma resposta que corresponde ao número 501, indicando que ainda há mais páginas.

```html
<a href=5b69b9cb83065d403869739ae7f0995e.php>x</a>
```

Continuando este teste, chegaremos à página 9999, que possui o link `http://68.183.31.62:33332/350208e449a15d3ca155db335ae219b9.php`, diferente de `md5("10000") = b7a782741f667201b54880c925faec4b`. Ao acessar a página, encontramos o seguinte código:

```php
<?php
include('flag.php');

if(isset($_GET['u']) && isset($_GET['x'])){
 $u = (string)$_GET['u'];
 $x = (string)$_GET['x'];
 if($u === $x){
  echo ':(';
 }else if (sha1($x) === sha1($u)){
  die($flag);
 }else{
  echo ':(';
 }
}
highlight_file(__FILE__);
```

O código da página indica que, para obtermos a flag, devemos passar dois parâmetros `u` e `x` na URL tais que `u` e `x` sejam diferentes mas o hash SHA1 deles sejam iguais; é o que chamamos de [colisão](https://en.wikipedia.org/wiki/Collision_(computer_science)).

Pesquisando por colisões SHA1, encontramos notícias de 2017 sobre ataques de colisão terem se tornado factíveis. Uma publicação notável sobre o assunto é o site [SHAttered.io](https://shattered.io/), que fornece dois PDFs diferentes mas que possuem o mesmo hash SHA1. No entanto, os arquivos são grandes demais para serem enviados como parâmetro de URL devido ao [limite de caracteres](https://stackoverflow.com/questions/417142/what-is-the-maximum-length-of-a-url-in-different-browsers). Seria interessante estudar o ataque de colisão para criar arquivos menores com o mesmo SHA1, mas isto levaria muito tempo. Felizmente, arquivos assim [já foram criados](https://twitter.com/arw/status/834883944898125824).

Agora, resta apenas converter o arquivo para a codificação de URL. Basicamente, devemos acrescentar um caractere `%` antes de cada byte em hexadecimal:

```python
def readfile(filename):
	output = ''
	with open(filename, 'rb') as f:
		byte = f.read(1)
		while byte != '':
			output += '{:02x}'.format(ord(byte))
			byte = f.read(1)
	return output

str1 = readfile('sha1_1.html')
str2 = readfile('sha1_2.html')

str1fmt = ''.join(['%' + str1[i] + str1[i + 1] for i in range(0, len(str1)) if i % 2 == 0])
str2fmt = ''.join(['%' + str2[i] + str2[i + 1] for i in range(0, len(str2)) if i % 2 == 0])

url = 'http://68.183.31.62:33332/350208e449a15d3ca155db335ae219b9.php'

print(url + '?u=' + str1fmt + '&x=' + str2fmt)
```

O resultado é uma URL enorme:

```
http://68.183.31.62:33332/350208e449a15d3ca155db335ae219b9.php?u=%25%50%44%46%2D%31%2E%33%0A%25%E2%E3%CF%D3%0A%0A%0A%31%20%30%20%6F%62%6A%0A%3C%3C%2F%57%69%64%74%68%20%32%20%30%20%52%2F%48%65%69%67%68%74%20%33%20%30%20%52%2F%54%79%70%65%20%34%20%30%20%52%2F%53%75%62%74%79%70%65%20%35%20%30%20%52%2F%46%69%6C%74%65%72%20%36%20%30%20%52%2F%43%6F%6C%6F%72%53%70%61%63%65%20%37%20%30%20%52%2F%4C%65%6E%67%74%68%20%38%20%30%20%52%2F%42%69%74%73%50%65%72%43%6F%6D%70%6F%6E%65%6E%74%20%38%3E%3E%0A%73%74%72%65%61%6D%0A%FF%D8%FF%FE%00%24%53%48%41%2D%31%20%69%73%20%64%65%61%64%21%21%21%21%21%85%2F%EC%09%23%39%75%9C%39%B1%A1%C6%3C%4C%97%E1%FF%FE%01%7F%46%DC%93%A6%B6%7E%01%3B%02%9A%AA%1D%B2%56%0B%45%CA%67%D6%88%C7%F8%4B%8C%4C%79%1F%E0%2B%3D%F6%14%F8%6D%B1%69%09%01%C5%6B%45%C1%53%0A%FE%DF%B7%60%38%E9%72%72%2F%E7%AD%72%8F%0E%49%04%E0%46%C2%30%57%0F%E9%D4%13%98%AB%E1%2E%F5%BC%94%2B%E3%35%42%A4%80%2D%98%B5%D7%0F%2A%33%2E%C3%7F%AC%35%14%E7%4D%DC%0F%2C%C1%A8%74%CD%0C%78%30%5A%21%56%64%61%30%97%89%60%6B%D0%BF%3F%98%CD%A8%04%46%29%A1%3C%68%74%6D%6C%3E%0A%3C%73%63%72%69%70%74%20%6C%61%6E%67%75%61%67%65%3D%6A%61%76%61%73%63%72%69%70%74%20%74%79%70%65%3D%22%74%65%78%74%2F%6A%61%76%61%73%63%72%69%70%74%22%3E%0A%3C%21%2D%2D%20%40%61%72%77%20%2D%2D%3E%0A%0A%76%61%72%20%68%20%3D%20%64%6F%63%75%6D%65%6E%74%2E%67%65%74%45%6C%65%6D%65%6E%74%73%42%79%54%61%67%4E%61%6D%65%28%22%48%54%4D%4C%22%29%5B%30%5D%2E%69%6E%6E%65%72%48%54%4D%4C%2E%63%68%61%72%43%6F%64%65%41%74%28%31%30%32%29%2E%74%6F%53%74%72%69%6E%67%28%31%36%29%3B%0A%69%66%20%28%68%20%3D%3D%20%27%37%33%27%29%20%7B%0A%20%20%20%20%64%6F%63%75%6D%65%6E%74%2E%62%6F%64%79%2E%69%6E%6E%65%72%48%54%4D%4C%20%3D%20%22%3C%53%54%59%4C%45%3E%62%6F%64%79%7B%62%61%63%6B%67%72%6F%75%6E%64%2D%63%6F%6C%6F%72%3A%52%45%44%3B%7D%20%68%31%7B%66%6F%6E%74%2D%73%69%7A%65%3A%35%30%30%25%3B%7D%3C%2F%53%54%59%4C%45%3E%3C%48%31%3E%26%23%78%31%66%36%34%38%3B%3C%2F%48%31%3E%22%3B%0A%7D%20%65%6C%73%65%20%7B%0A%20%20%20%20%64%6F%63%75%6D%65%6E%74%2E%62%6F%64%79%2E%69%6E%6E%65%72%48%54%4D%4C%20%3D%20%22%3C%53%54%59%4C%45%3E%62%6F%64%79%7B%62%61%63%6B%67%72%6F%75%6E%64%2D%63%6F%6C%6F%72%3A%42%4C%55%45%3B%7D%20%68%31%7B%66%6F%6E%74%2D%73%69%7A%65%3A%35%30%30%25%3B%7D%3C%2F%53%54%59%4C%45%3E%3C%48%31%3E%26%23%78%31%66%36%34%39%3B%3C%2F%48%31%3E%22%3B%0A%7D%0A%0A%3C%2F%73%63%72%69%70%74%3E%0A%0A&x=%25%50%44%46%2D%31%2E%33%0A%25%E2%E3%CF%D3%0A%0A%0A%31%20%30%20%6F%62%6A%0A%3C%3C%2F%57%69%64%74%68%20%32%20%30%20%52%2F%48%65%69%67%68%74%20%33%20%30%20%52%2F%54%79%70%65%20%34%20%30%20%52%2F%53%75%62%74%79%70%65%20%35%20%30%20%52%2F%46%69%6C%74%65%72%20%36%20%30%20%52%2F%43%6F%6C%6F%72%53%70%61%63%65%20%37%20%30%20%52%2F%4C%65%6E%67%74%68%20%38%20%30%20%52%2F%42%69%74%73%50%65%72%43%6F%6D%70%6F%6E%65%6E%74%20%38%3E%3E%0A%73%74%72%65%61%6D%0A%FF%D8%FF%FE%00%24%53%48%41%2D%31%20%69%73%20%64%65%61%64%21%21%21%21%21%85%2F%EC%09%23%39%75%9C%39%B1%A1%C6%3C%4C%97%E1%FF%FE%01%73%46%DC%91%66%B6%7E%11%8F%02%9A%B6%21%B2%56%0F%F9%CA%67%CC%A8%C7%F8%5B%A8%4C%79%03%0C%2B%3D%E2%18%F8%6D%B3%A9%09%01%D5%DF%45%C1%4F%26%FE%DF%B3%DC%38%E9%6A%C2%2F%E7%BD%72%8F%0E%45%BC%E0%46%D2%3C%57%0F%EB%14%13%98%BB%55%2E%F5%A0%A8%2B%E3%31%FE%A4%80%37%B8%B5%D7%1F%0E%33%2E%DF%93%AC%35%00%EB%4D%DC%0D%EC%C1%A8%64%79%0C%78%2C%76%21%56%60%DD%30%97%91%D0%6B%D0%AF%3F%98%CD%A4%BC%46%29%B1%3C%68%74%6D%6C%3E%0A%3C%73%63%72%69%70%74%20%6C%61%6E%67%75%61%67%65%3D%6A%61%76%61%73%63%72%69%70%74%20%74%79%70%65%3D%22%74%65%78%74%2F%6A%61%76%61%73%63%72%69%70%74%22%3E%0A%3C%21%2D%2D%20%40%61%72%77%20%2D%2D%3E%0A%0A%76%61%72%20%68%20%3D%20%64%6F%63%75%6D%65%6E%74%2E%67%65%74%45%6C%65%6D%65%6E%74%73%42%79%54%61%67%4E%61%6D%65%28%22%48%54%4D%4C%22%29%5B%30%5D%2E%69%6E%6E%65%72%48%54%4D%4C%2E%63%68%61%72%43%6F%64%65%41%74%28%31%30%32%29%2E%74%6F%53%74%72%69%6E%67%28%31%36%29%3B%0A%69%66%20%28%68%20%3D%3D%20%27%37%33%27%29%20%7B%0A%20%20%20%20%64%6F%63%75%6D%65%6E%74%2E%62%6F%64%79%2E%69%6E%6E%65%72%48%54%4D%4C%20%3D%20%22%3C%53%54%59%4C%45%3E%62%6F%64%79%7B%62%61%63%6B%67%72%6F%75%6E%64%2D%63%6F%6C%6F%72%3A%52%45%44%3B%7D%20%68%31%7B%66%6F%6E%74%2D%73%69%7A%65%3A%35%30%30%25%3B%7D%3C%2F%53%54%59%4C%45%3E%3C%48%31%3E%26%23%78%31%66%36%34%38%3B%3C%2F%48%31%3E%22%3B%0A%7D%20%65%6C%73%65%20%7B%0A%20%20%20%20%64%6F%63%75%6D%65%6E%74%2E%62%6F%64%79%2E%69%6E%6E%65%72%48%54%4D%4C%20%3D%20%22%3C%53%54%59%4C%45%3E%62%6F%64%79%7B%62%61%63%6B%67%72%6F%75%6E%64%2D%63%6F%6C%6F%72%3A%42%4C%55%45%3B%7D%20%68%31%7B%66%6F%6E%74%2D%73%69%7A%65%3A%35%30%30%25%3B%7D%3C%2F%53%54%59%4C%45%3E%3C%48%31%3E%26%23%78%31%66%36%34%39%3B%3C%2F%48%31%3E%22%3B%0A%7D%0A%0A%3C%2F%73%63%72%69%70%74%3E%0A%0A
```

A URL nos dá a flag `HACKAFLAG{14m_4_3ngl4nd_guy_n0w}`.

---

Este desafio provavelmente foi baseado no desafio Prudentialv2, que tem um write-up [aqui](https://github.com/bl4de/ctf/blob/master/2017/BostonKeyParty_2017/Prudentialv2/Prudentialv2_Cloud_50.md).
