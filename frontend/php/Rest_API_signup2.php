<?php

// Function to handle API response
function apiResponse($status, $message)
{
    http_response_code($status);
    echo json_encode(array("status" => $status, "message" => $message));
    exit();
}

// Check if the request is made via API
if (isset($_GET['api']) && $_GET['api'] == 'signup') {
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        $name = htmlspecialchars(trim($_POST['name']));
        $email = htmlspecialchars(trim($_POST['email']));
        $password = $_POST['password'];
        $confirm_password = $_POST['confirm_password'];

        // Check if passwords match and password length
        if (strlen($password) < 8) {
            apiResponse(400, "The password must be at least 8 characters");
        } elseif ($password !== $confirm_password) {
            apiResponse(400, "Passwords do not match, please try again");
        } elseif (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
            apiResponse(400, "Invalid email address, please enter a valid one.");
        } else {
            // Check if email already exists in the database
            $stmt = $pdo->prepare("SELECT * FROM users WHERE email=?");
            $stmt->execute([$email]);
            $result = $stmt->fetch(PDO::FETCH_ASSOC);

            if ($result) {
                apiResponse(400, "User already exists, please choose another one.");
            } else {
                // Proceed with inserting new user into the database
                $hashed_password = password_hash($password, PASSWORD_BCRYPT);
                $hashed_confirm_password = password_hash($confirm_password, PASSWORD_BCRYPT); // Hash confirm password
                $stmt = $pdo->prepare("INSERT INTO users (name, email, password, confirm_password) VALUES (?, ?, ?, ?)");
                $stmt->execute([$name, $email, $hashed_password, $hashed_confirm_password]);

                if ($stmt->rowCount() > 0) {
                    // User signed up successfully
                    apiResponse(201, "User signed up successfully");
                } else {
                    apiResponse(500, "Error occurred, please try again later");
                }
            }
        }
    } else {
        apiResponse(405, "Method Not Allowed");
    }
}
