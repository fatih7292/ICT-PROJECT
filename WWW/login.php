<?php
session_start();
include "db.php";

$username = $_POST['username'] ?? '';
$password = $_POST['password'] ?? '';

// 🔐 АДМИН — ПЕРВЫМ
if ($username === 'admin' && $password === '1234') {
    $_SESSION['admin'] = true;
    header("Location: admin.php");
    exit;
}

// 🧑‍🎓 ОБЫЧНЫЙ ПОЛЬЗОВАТЕЛЬ — ПОТОМ
include "db.php";

$sql = "SELECT * FROM users WHERE username='$username'";
$result = mysqli_query($conn, $sql);

if (mysqli_num_rows($result) == 1) {
    $user = mysqli_fetch_assoc($result);
    if (password_verify($password, $user['password'])) {
        $_SESSION['user'] = $user;
        header("Location: index.html");
        exit;
    } else {
        echo "Неверный пароль";
        exit;
    }
} else {
    echo "Пользователь не найден";
    exit;
}
?>