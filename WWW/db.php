
<?php
$host = "localhost";
$user = "root"; 
$pass = ""; 
$db   = "mysite"; // название базы которое ты создал!

$conn = mysqli_connect($host, $user, $pass, $db);

if (!$conn) {
    die("Ошибка подключения: " . mysqli_connect_error());
}
?>
