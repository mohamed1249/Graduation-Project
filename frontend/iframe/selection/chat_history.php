<?php
$host = "localhost";
$dbname = "chatbot";
$username = "root";
$password = "";

try {
    $conn = new PDO("mysql:host=$host;dbname=$dbname", $username, $password);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $conn->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
    $sql = "SELECT user_question, model_reply FROM messages";
    $stmt = $conn->prepare($sql);
    $stmt->execute();
    $chatData = $stmt->fetchAll(PDO::FETCH_ASSOC);
    $conn = null;
    $chathistory_json = json_encode($chatData);
} catch (PDOException $e) {
    echo json_encode(['error' => 'Error fetching data: ' . $e->getMessage()]);
}
