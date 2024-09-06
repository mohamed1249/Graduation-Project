<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="./js/version 3.5.js"></script>
    <link rel="stylesheet" href="./css/version 3.5.css">
    <link rel="shortcut icon" href="../images/logo.svg">
    <title>Chatbot</title>
    <style>
        .message {
            margin: 10px 0;
        }

        .outgoing {
            text-align: right;
        }

        .incoming {
            text-align: left;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        html,
        body {
            width: 100%;
            height: 100%;
        }

        .container {
            width: 100%;
            height: 100%;
            position: relative;
            display: grid;
            justify-items: center;
        }

        .container::after {
            content: "GPT 3.5";
            position: absolute;
            color: lightgray;
            font-size: 60px;
            opacity: 0.5;
            top: 45%;
            left: 50%;
            transform: translate(-50%, -50%);
        }

        .chat-card {
            width: 90%;
            background-color: #fff;
            border-radius: 5px;
            position: absolute;
            bottom: 0;
        }

        .chat-header {
            padding: 10px;
            background-color: #f2f2f2;
            display: flex;
            align-items: center;
        }

        .chat-header .h2 {
            font-size: 16px;
            color: #333;
        }

        .body {
            overflow-y: scroll;
            height: 510px;
            display: grid;
            align-items: end;
        }

        .chat-body {
            padding: 20px;
            display: grid;
            justify-items: center;
        }

        .message {
            margin-bottom: 10px;
            padding: 10px;
            border-radius: 5px;
        }

        .incoming {
            background-color: #e1e1e1;
        }

        .outgoing {
            background-color: #f2f2f2;
            text-align: right;
        }

        .message p {
            font-size: 14px;
            color: #333;
            margin: 0;
        }

        .chat-footer {
            padding: 10px;
            background-color: #f2f2f2;
            display: flex;
        }

        .chat-footer input[type="text"] {
            flex-grow: 1;
            padding: 12px 5px;
            border: none;
            border-radius: 3px;
            margin-right: 10px;
        }

        .chat-footer input[type="text"]:focus {
            outline: none;
        }

        .chat-footer button {
            padding: 5px 10px;
            border: none;
            background-color: #4285f4;
            color: #fff;
            font-weight: bold;
            cursor: pointer;
            transition: background-color 0.3s;
        }

        .chat-footer button:hover {
            background-color: #0f9d58;
        }

        @keyframes chatAnimation {
            0% {
                opacity: 0;
                transform: translateY(10px);
            }

            100% {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .chat-card .message {
            animation: chatAnimation 0.3s ease-in-out;
            animation-fill-mode: both;
            animation-delay: 0.1s;
        }

        .chat-card .message:nth-child(even) {
            animation-delay: 0.2s;
            width: 60%;
        }

        .chat-card .message:nth-child(odd) {
            animation-delay: 0.3s;
            width: 60%;
        }
    </style>
</head>

<body>
    <div class="container">
        <div class="chat-card">
            <div class="body" id="scrollableDiv">
                <div class="chat-body">
                    <!-- Messages will be appended here -->
                </div>
            </div>
            <form id="chat-form" method="post">
                <div class="chat-footer" style="padding: 10px;background-color: #f2f2f2;display: flex;">
                    <input id="message" name="message" required placeholder="Type your message here" style="flex-grow: 1;padding: 12px 5px;border: none;border-radius: 3px;margin-right: 10px;outline: none;">
                    <input type="hidden" name="model_reply" id="model_version" value="model1">
                    <button name="send" type="submit" style="padding: 5px 10px;border: none;background-color: #4285f4;color: #fff;font-weight: bold;cursor: pointer;transition: background-color 0.3s;background-color: #0f9d58;">Send</button>
                </div>
            </form>
        </div>
    </div>

    <script>
        document.addEventListener("DOMContentLoaded", function() {
            const form = document.getElementById("chat-form");
            const chatBody = document.querySelector(".chat-body");

            form.addEventListener("submit", function(event) {
                event.preventDefault();

                const formData = new FormData(form);
                const messageText = formData.get("message").trim();

                if (messageText !== "") {
                    // Display the outgoing message immediately
                    const outgoingMessage = document.createElement("div");
                    outgoingMessage.classList.add("message", "outgoing");
                    outgoingMessage.innerHTML = `<p>${messageText}</p>`;
                    chatBody.appendChild(outgoingMessage);
                    chatBody.scrollTop = chatBody.scrollHeight;

                    // Send the message via AJAX
                    fetch(form.action, {
                            method: "POST",
                            body: formData
                        })
                        .then(response => response.text())
                        .then(html => {
                            // Append the incoming message to the chat body
                            chatBody.innerHTML += html;
                            chatBody.scrollTop = chatBody.scrollHeight;
                        })
                        .catch(error => console.error('Error:', error));

                    // Clear the input field
                    form.reset();
                }
            });
        });
    </script>

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
</body>

</html>