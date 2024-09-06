<?php

// $dsn = "mysql:host=localhost;dbname=chatbot";
// $username = "root";
// $password = "";

// try {
//     $conn = new PDO($dsn, $username, $password);
//     $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

//     if ($_SERVER['REQUEST_METHOD'] == 'POST' && isset($_POST['message']) && !empty($_POST['message'])) {
//         $message = $_POST['message'];
//         $model_reply = ucwords("model reply AI .");

//         // Check if the message already exists 
//         $check_sql = "SELECT * FROM messages WHERE user_question = :message";
//         $check_stmt = $conn->prepare($check_sql);
//         $check_stmt->bindParam(':message', $message);
//         $check_stmt->execute();
//         $existing_record = $check_stmt->fetch(PDO::FETCH_ASSOC);

//         if ($existing_record) {
//             // Delete the existing record
//             $delete_sql = "DELETE FROM messages WHERE user_question = :message";
//             $delete_stmt = $conn->prepare($delete_sql);
//             $delete_stmt->bindParam(':message', $message);
//             $delete_stmt->execute();
//         }

//         // URL of the API endpoint
//         $model_urls = array(
//             "model1" => "http://localhost:5000/v2e",
//             "model2" => "http://localhost:5000/v2a",
//             "model3" => "http://localhost:5000/v1e",
//             "model4" => "http://localhost:5000/v1a"
//         );
//         $api_url = "http://localhost:5000/v2e" || "http://localhost:5000/v2a" || "http://localhost:5000/v1e" || "http://localhost:5000/v1a";

//         ob_start();
//         include('./project/iframe/selection/chat_history.php');
//         $chat_history_content = ob_get_clean();

//         $data = array(
//             "question" => $message,
//             "chat_history" =>  $chat_history_content,
//             "GPT" => "gpt-3.5-turbo", "gpt-4"
//         );



//         // Send POST request to the API
//         $incoming_message = curl_init($api_url);
//         curl_setopt($incoming_message, CURLOPT_RETURNTRANSFER, true);
//         curl_setopt($incoming_message, CURLOPT_POST, true);
//         curl_setopt($incoming_message, CURLOPT_POSTFIELDS, json_encode($data));
//         curl_setopt($incoming_message, CURLOPT_HTTPHEADER, array(
//             'Content-Type: application/json',
//             'Accept: application/json'
//         ));

//         $response = curl_exec($incoming_message);
//         if ($response === false) {
//             echo "Error: " . curl_error($incoming_message);
//         } else {
//             $api_response = json_decode($response);
//             $model_reply = $api_response->generated_text;

//             // Update the message with the API response
//             $update_sql = "UPDATE messages SET model_reply = CONCAT(model_reply, :response) WHERE user_question = :message";
//             $update_stmt = $conn->prepare($update_sql);
//             $update_stmt->bindParam(':response', $response);
//             $update_stmt->bindParam(':message', $message);
//             $update_stmt->execute();
//         }
//         curl_close($incoming_message);
//     }
// } catch (PDOException $e) {
//     echo "Connection failed: " . $e->getMessage();
// }
?>
<?php
// header('Content-Type: application/json');

// $dsn = "mysql:host=localhost;dbname=chatbot";
// $username = "root";
// $password = "";

// try {
//     $conn = new PDO($dsn, $username, $password);
//     $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

//     if ($_SERVER['REQUEST_METHOD'] == 'POST') {
//         $input = json_decode(file_get_contents('php://input'), true);
//         if (!isset($input['question']) || !isset($input['response'])) {
//             echo json_encode(['error' => 'No question or response provided']);
//             http_response_code(400);
//             exit;
//         }

//         $question = $input['question'];
//         $response = $input['response'];

//         // Debug messages
//         error_log("Question: $question");
//         error_log("Response: $response");

//         $check_sql = "SELECT * FROM messages WHERE user_question = :question";
//         $check_stmt = $conn->prepare($check_sql);
//         $check_stmt->bindParam(':question', $question);
//         $check_stmt->execute();

//         if ($check_stmt->rowCount() > 0) {
//             $update_sql = "UPDATE messages SET model_reply = :response WHERE user_question = :question";
//             $update_stmt = $conn->prepare($update_sql);
//             $update_stmt->bindParam(':response', $response);
//             $update_stmt->bindParam(':question', $question);
//             $update_stmt->execute();

//             echo json_encode(['message' => 'Message updated successfully']);
//         } else {
//             $insert_sql = "INSERT INTO messages (user_question, model_reply) VALUES (:question, :response)";
//             $insert_stmt = $conn->prepare($insert_sql);
//             $insert_stmt->bindParam(':question', $question);
//             $insert_stmt->bindParam(':response', $response);
//             $insert_stmt->execute();

//             echo json_encode(['message' => 'Message inserted successfully']);
//         }
//     } else {
//         echo json_encode(['error' => 'Invalid request method']);
//         http_response_code(405);
//     }
// } catch (PDOException $e) {
//     echo json_encode(['error' => 'Connection failed: ' . $e->getMessage()]);
//     http_response_code(500);
// }

?>

<?php
$dsn = "mysql:host=localhost;dbname=chatbot";
$username = "root";
$password = "";

try {
    $conn = new PDO($dsn, $username, $password);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    if ($_SERVER['REQUEST_METHOD'] == 'POST' && isset($_POST['message']) && !empty($_POST['message'])) {
        $message = $_POST['message'];
        $model_reply = ucwords("model reply AI .");

        // Check if the message already exists 
        $check_sql = "SELECT * FROM messages WHERE user_question = :message";
        $check_stmt = $conn->prepare($check_sql);
        $check_stmt->bindParam(':message', $message);
        $check_stmt->execute();
        $existing_record = $check_stmt->fetch(PDO::FETCH_ASSOC);

        if ($existing_record) {
            // Delete the existing record
            $delete_sql = "DELETE FROM messages WHERE user_question = :message";
            $delete_stmt = $conn->prepare($delete_sql);
            $delete_stmt->bindParam(':message', $message);
            $delete_stmt->execute();
        }

        // Insert the new message and model reply
        $insert_sql = "INSERT INTO messages(user_question, model_reply) VALUES (:message, :model_reply)";
        $stmt = $conn->prepare($insert_sql);
        $stmt->bindParam(':message', $message);
        $stmt->bindParam(':model_reply', $model_reply);
        $stmt->execute();

        // URL of the API endpoint
        $model_urls = array(
            "model1" => "http://localhost:49664/v2e",
            "model2" => "http://localhost:49664/v2a",
            "model3" => "http://localhost:49664/v1e",
            "model4" => "http://localhost:49664/v1a"
        );
        $api_url = $model_urls[$_POST['model_reply']] ?? "http://localhost:49664/v2e";

        ob_start();
        include('./project/iframe/selection/chat_history.php');
        $chat_history_content = ob_get_clean();

        $data = array(
            "question" => $message,
            "chat_history" => $chat_history_content,
            "GPT" => "gpt-3.5-turbo" // assuming this is the correct format for GPT version
        );

        // Send POST request to the API
        $incoming_message = curl_init($api_url);
        curl_setopt($incoming_message, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($incoming_message, CURLOPT_POST, true);
        curl_setopt($incoming_message, CURLOPT_POSTFIELDS, json_encode($data));
        curl_setopt($incoming_message, CURLOPT_HTTPHEADER, array(
            'Content-Type: application/json',
            'Accept: application/json'
        ));

        $response = curl_exec($incoming_message);
        if ($response === false) {
            echo "Error: " . curl_error($incoming_message);
        } else {
            $api_response = json_decode($response);
            $model_reply = $api_response->generated_text;

            // Update the message with the API response
            $update_sql = "UPDATE messages SET model_reply = :model_reply WHERE user_question = :message";
            $update_stmt = $conn->prepare($update_sql);
            $update_stmt->bindParam(':model_reply', $model_reply);
            $update_stmt->bindParam(':message', $message);
            $update_stmt->execute();
        }
        curl_close($incoming_message);
    }
} catch (PDOException $e) {
    echo "Connection failed: " . $e->getMessage();
}
?>
