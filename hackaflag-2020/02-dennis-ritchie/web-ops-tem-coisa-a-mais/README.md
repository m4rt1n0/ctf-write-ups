# OPS TEM COISA A MAIS

- Data do desafio: 2020-05-15
- Categoria: web

O desafio nos leva a uma página de login que solicita um nome e uma senha, e também possui um link para cadastrar uma conta, `cadastrar.html`. Ao cadastrar uma conta, é feita uma requisição POST para `cadastrar.php`, passando os parâmetros `username=teste&senha=teste`.

Ao realizar o login, acessamos a página `principal.php` e encontramos um texto suspeito: `{"admin":"Acesso autorizado apenas para administradores"}`. Aparentemente, vamos precisar de entrar em uma conta de administrador já existente ou transformar nossa conta em administradora para progredir no desafio.

Navegando um pouco mais, encontramos a página `alterar.html`, que nos permite alterar a senha, enviando uma requisição POST para `alterar.php` com os parâmetros `username=teste&senha=novasenha`.

Se recarregarmos a página `alterar.php` (com uma requisiçaõ GET), obtemos o seguinte erro:

```
Erro na Linha: #13 :: Undefined index: username
/var/www/html/alterar.php
Erro na Linha: #14 :: Undefined index: senha
/var/www/html/alterar.php
{"cadastro":"Nome deve ser maior que 3 caracteres\n"}
```

Repare que a última linha tem a mesma formatação que vimos anteriormente com "admin". Isto indica que há um campo `admin` que é utilizado para verificar quem é ou não é administrador. Vamos tentar alterar este campo no endpoint `alterar.php`, realizando uma nova requisição POST mas alterando os parâmetros para `username=teste&senha=novasenha&admin=true`. Obtemos a seguinte resposta:

> Erro ao Ler: SQLSTATE[HY000]: General error: 1366 Incorrect integer value: 'true' for column 'admin' at row 1
> Não foi possível validar dados

Agora sabemos que o campo existe e que é do tipo inteiro, então podemos substituir o parâmetro para `admin=1` e repetir o processo anterior. Ao retornar para a página `principal.php`, a mensagem agora é diferente: `{"admin":"Sua flag \u00e9 HACKAFLAG{masscompletoadmin}"}`.

Flag: `HACKAFLAG{masscompletoadmin}`