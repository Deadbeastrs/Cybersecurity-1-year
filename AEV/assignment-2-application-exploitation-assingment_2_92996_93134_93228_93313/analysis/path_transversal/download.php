<?php
ob_start();
$con = mysqli_connect("database-vulnerable", $_ENV['MYSQL_USER'], $_ENV['MYSQL_PASSWORD'], $_ENV['MYSQL_DATABASE']);

$xmlfile = file_get_contents('php://input');
$dom = new DOMDocument();
$dom->loadXML($xmlfile, LIBXML_NOENT | LIBXML_DTDLOAD);
$creds = simplexml_import_dom($dom);

$email = $creds->email;
$password = md5($creds->password);

$query = "SELECT * FROM users WHERE email='$email' AND password='$password';";
$query_result = mysqli_query($con, $query) or die(mysqli_error($con));

if (mysqli_num_rows($query_result) == 0) {
   echo 401;
   echo 'Incorrect email or password';
   echo "\n Oops! \n $email";
} else {
   $row = mysqli_fetch_array($query_result);
   $arr =  array($row['email'], $row['id'], $row['name']);
   echo 200;
   echo implode("&", $arr);
}
?>