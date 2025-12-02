<?php
$pdo = new PDO('mysql:host=localhost;dbname=feedback_system', 'root', '');
$stmt = $pdo->query("SELECT * FROM reviews ORDER BY created_at DESC");
$reviews = $stmt->fetchAll(PDO::FETCH_ASSOC);
?>
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <title>Admin — Feedback System</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/animejs/3.2.1/anime.min.js"></script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Playfair+Display:wght@600&display=swap" rel="stylesheet">
  <style>
    body {
      background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
      min-height: 100vh;
      font-family: 'Inter', sans-serif;
    }
    .review-card {
      background: white;
      border-radius: 20px;
      padding: 24px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.1);
      opacity: 0;
      transform: translateY(30px);
    }
    .star-gold { color: #d97706; }
  </style>
</head>
<body class="text-white">

  <!-- Заголовок -->
  <section class="py-16 text-center">
    <h1 class="text-5xl font-bold font-['Playfair_Display'] mb-4">Admin Panel</h1>
    <p class="text-xl text-blue-100">Все отзывы из системы</p>
  </section>

  <!-- Белый контейнер -->
  <main class="max-w-5xl mx-auto px-6 pb-16">
    <div class="bg-white/90 backdrop-blur-md rounded-3xl p-8 shadow-2xl">
      <div class="grid gap-8 md:grid-cols-2 lg:grid-cols-3" id="reviewsContainer">
        <?php foreach ($reviews as $r):
          $stars = str_repeat('<span class="star-gold">★</span>', $r['rating']) .
                   str_repeat('<span class="text-gray-300">★</span>', 5 - $r['rating']);
        ?>
          <div class="review-card">
            <div class="flex items-center justify-between mb-2">
              <h3 class="font-bold text-lg text-gray-900"><?= htmlspecialchars($r['professor_name']) ?></h3>
              <span class="text-sm text-gray-500"><?= htmlspecialchars($r['course'] ?? '—') ?></span>
            </div>
            <div class="flex items-center mb-3 text-xl"><?= $stars ?><span class="ml-2 text-gray-700 font-semibold"><?= $r['rating'] ?></span></div>
            <p class="text-gray-800 leading-relaxed"><?= nl2br(htmlspecialchars($r['review_text'])) ?></p>
            <p class="text-xs text-gray-500 mt-3"><?= date('d.m.Y', strtotime($r['created_at'])) ?></p>
          </div>
        <?php endforeach; ?>
      </div>
    </div>
  </main>

  <!-- Анимация -->
  <script>
    anime({
      targets: '.review-card',
      opacity: [0, 1],
      translateY: [30, 0],
      delay: anime.stagger(100),
      duration: 800,
      easing: 'easeOutQuad'
    });
  </script>

</body>
</html>