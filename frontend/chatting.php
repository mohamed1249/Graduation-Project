<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chatbot</title>
</head>

<body>
    <h1>Chat with our AI</h1>
    <form id="chat-form" method="POST">
        <input id="message" name="message" required>
        <input type="hidden" name="model_reply" id="model_version">
        <button name="send" type="submit">Send Message</button>
    </form>
    <div id="chat-history"></div>


    <script>
        const form = document.getElementById('chat-form');
        form.addEventListener('submit', function(event) {
            const userIdInput = document.getElementById('user_id');
            if (userIdInput.value === '') {
                event.preventDefault(); // Prevent form submission
                alert('Please enter a valid user ID.');
                userIdInput.focus(); // Set focus on the input field
            }
        });
    </script>

    <?php

    // $dsn = "mysql:host=localhost;dbname=chatbot";
    // $username = "root";
    // $password = "";

    // try {
    //     $conn = new PDO($dsn, $username, $password);
    //     $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    //     if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    //         $message = $_POST['message'];
    //         $chat_history = "";
    //         $endpoint_url = "http://localhost:5000/v2e"
    //         $data = array('question' => $message, 'chat_history' => $chat_history);
    //         $options = array(
    //             'http' => array(
    //                 'method' => 'POST',
    //                 'header' => 'Content-Type: application/json',
    //                 'content' => json_encode($data)
    //             )
    //         );
    //         $context = stream_context_create($options);
    //         $response = file_get_contents($endpoint_url, false, $context);

    //         if ($response === false) {
    //             echo "<script>alert('Error fetching data from endpoint.')</script>";
    //         } else {
    //             $api_response = json_decode($response);
    //             $model_reply = $api_response->response;
    //             $check_sql = "SELECT * FROM messages WHERE user_question = :message";
    //             $check_stmt = $conn->prepare($check_sql);
    //             $check_stmt->bindParam(':message', $message);
    //             $check_stmt->execute();
    //             $existing_record = $check_stmt->fetch(PDO::FETCH_ASSOC);

    //             if ($existing_record) {
    //                 $old_model_reply = $existing_record['model_reply'];
    //                 $updated_model_reply = $old_model_reply . "\n\n" . $model_reply;

    //                 $update_sql = "UPDATE messages SET model_reply = :updated_model_reply WHERE user_question = :message";
    //                 $stmt = $conn->prepare($update_sql);
    //                 $stmt->bindParam(':updated_model_reply', $updated_model_reply);
    //             } else {
    //                 $insert_sql = "INSERT INTO messages(user_question, model_reply) VALUES (:message, :model_reply)";
    //                 $stmt = $conn->prepare($insert_sql);
    //             }
    //             $stmt->bindParam(':message', $message);
    //             $stmt->bindParam(':model_reply', $model_reply);
    //             $stmt->execute();

    //             // Display a success message
    //             echo "Model reply received and inserted/updated in the database.";
    //         }
    //     }
    // } catch (PDOException $e) {
    //     echo "Connection failed: " . $e->getMessage();
    // }
    ?>
    
    <?php
    $dsn = "mysql:host=localhost;dbname=chatbot";
    $username = "root";
    $password = "";

    try {
        $conn = new PDO($dsn, $username, $password);
        $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

        if ($_SERVER['REQUEST_METHOD'] == 'POST') {
            $message = $_POST['message'];
            $model_reply = ucwords("مرحبا بك كيف يممكني مساعدتك اليوم ؟");

            $check_sql = "SELECT * FROM messages WHERE user_question = :message";
            $check_stmt = $conn->prepare($check_sql);
            $check_stmt->bindParam(':message', $message);
            $check_stmt->execute();

            if ($check_stmt->rowCount() > 0) {
                $update_sql = "UPDATE messages SET model_reply = :model_reply WHERE user_question = :message";
                $update_stmt = $conn->prepare($update_sql);
                $update_stmt->bindParam(':model_reply', $model_reply);
                $update_stmt->bindParam(':message', $message);
                $update_stmt->execute();
            } else {
                $insert_sql = "INSERT INTO messages (user_question, model_reply) VALUES (:message, :model_reply)";
                $insert_stmt = $conn->prepare($insert_sql);
                $insert_stmt->bindParam(':message', $message);
                $insert_stmt->bindParam(':model_reply', $model_reply);
                $insert_stmt->execute();
            }
        }
    } catch (PDOException $e) {
        echo "Connection failed: " . $e->getMessage();
    }
    ?>




</body>

</html>