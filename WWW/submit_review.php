<?php
file_put_contents('debug.log', date('H:i:s') . '  POST: ' . print_r($_POST, true) . PHP_EOL, FILE_APPEND);

// подключение к БД
$pdo = new PDO('mysql:host=localhost;dbname=feedback_system', 'root', '');

// получаем данные
$professor_name = $_POST['professor_name'] ?? '';
$course        = $_POST['course']        ?? '';
$rating        = (int)($_POST['rating']   ?? 0);
$review_text   = $_POST['review_text']    ?? '';

// валидация и запись
if ($professor_name && $course && $rating >= 1 && $rating <= 5 && $review_text) {
    $stmt = $pdo->prepare("INSERT INTO reviews (professor_name, course, rating, review_text) VALUES (?, ?, ?, ?)");
    $stmt->execute([$professor_name, $course, $rating, $review_text]);
}

// редирект
header("Location: professor.html?success=1");
exit;
// валидация и запись
if ($professor_name && $course && $rating >= 1 && $rating <= 5 && $review_text) {
    $stmt = $pdo->prepare("INSERT INTO reviews (professor_name, course, rating, review_text) VALUES (?, ?, ?, ?)");
    $stmt->execute([$professor_name, $course, $rating, $review_text]);

    // ✅ Проверка
    file_put_contents('debug.log', date('H:i:s') . '  INSERT OK' . PHP_EOL, FILE_APPEND);
} else {
    file_put_contents('debug.log', date('H:i:s') . '  INSERT FAIL: ' . json_encode([$professor_name, $course, $rating, $review_text]) . PHP_EOL, FILE_APPEND);
}
?>