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
