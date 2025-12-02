<?php
include "db.php";

$username = $_POST['username'];
$password = password_hash($_POST['password'], PASSWORD_DEFAULT);

$sql = "INSERT INTO users (username, password) VALUES ('$username', '$password')";

if (mysqli_query($conn, $sql)) {
    header("Location: index.html");
    exit();
} else {
    echo "Ошибка: " . mysqli_error($conn);
}
?>

