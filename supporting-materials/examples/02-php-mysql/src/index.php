<?php
$host = getenv('DB_HOST') ?: 'db';
$db   = getenv('DB_NAME') ?: 'appdb';
$user = getenv('DB_USER') ?: 'appuser';
$pass = getenv('DB_PASSWORD') ?: 'apppass';

$mysqli = @new mysqli($host, $user, $pass, $db);

header('Content-Type: text/html; charset=UTF-8');

echo '<!doctype html><html><head><meta charset="utf-8"><title>PHP + MySQL Demo</title>';
echo '<style>body{font-family:Arial,sans-serif;margin:2rem;}code,pre{background:#f4f4f4;padding:.25rem .5rem;border-radius:4px;}table{border-collapse:collapse}td,th{border:1px solid #ddd;padding:.4rem .6rem}</style>';
echo '</head><body>';
echo '<h1>PHP + MySQL (docker-compose) — simple demo</h1>';

echo '<p><strong>DB connection status:</strong> ';
if ($mysqli->connect_errno) {
    echo '<span style="color:#b00">Failed: (' . $mysqli->connect_errno . ') ' . htmlspecialchars($mysqli->connect_error) . '</span></p>';
    echo '<p>Check that the database container is healthy and credentials match.</p>';
    echo '</body></html>';
    exit;
}

echo '<span style="color:#070">OK</span></p>';

$mysqli->query("CREATE TABLE IF NOT EXISTS notes (id INT AUTO_INCREMENT PRIMARY KEY, message VARCHAR(255) NOT NULL) ENGINE=InnoDB;");

if (isset($_POST['message']) && $_POST['message'] !== '') {
    $stmt = $mysqli->prepare('INSERT INTO notes (message) VALUES (?)');
    $stmt->bind_param('s', $_POST['message']);
    $stmt->execute();
    $stmt->close();
}

$result = $mysqli->query('SELECT id, message FROM notes ORDER BY id DESC');

echo '<h2>Add a note</h2>';
echo '<form method="post"><input name="message" placeholder="Type a message" required> <button type="submit">Save</button></form>';

echo '<h2>Notes</h2>';
echo '<table><tr><th>ID</th><th>Message</th></tr>';
while ($row = $result->fetch_assoc()) {
    echo '<tr><td>' . (int)$row['id'] . '</td><td>' . htmlspecialchars($row['message']) . '</td></tr>';
}
echo '</table>';

$result->free();
$mysqli->close();

echo '<p style="margin-top:2rem;color:#555">Open this app at <code>http://localhost:8080</code>. DB host: <code>' . htmlspecialchars($host) . "</code></p>";
echo '</body></html>';
