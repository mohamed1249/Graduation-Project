<?php
session_start();
include("./php/connection/connection.php");
include("./php/Rest_API_signup2.php");

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $name = htmlspecialchars(strip_tags(trim($_POST['name'])));
    $email = htmlspecialchars(strip_tags(trim($_POST['email'])));
    $password = $_POST['password'];
    $confirm_password = $_POST['confirm_password'];

    // Check if all required fields are filled
    if (empty($name) || empty($email) || empty($password) || empty($confirm_password)) {
        $error = "<p style='color:red'>Please complete all required fields.</p>";
    } elseif (strlen($password) < 8) {
        $error = "<p style='color:red'>The password must be at least 8 characters</p>";
    } elseif ($password !== $confirm_password) {
        $error = "<p style='color:red'>Passwords do not match, please try again</p>";
    } elseif (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $error = "<p style='color:red;'>Invalid email address, please enter a valid one.</p>";
    } else {
        // Check if email already exists in the database
        $stmt = $pdo->prepare("SELECT * FROM users WHERE email=?");
        $stmt->execute([$email]);
        $result = $stmt->fetch(PDO::FETCH_ASSOC);

        if ($result) {
            $error = "<p style='color:red;'>User already exists, please choose another one.</p>";
        } else {
            // Proceed with inserting new user into the database
            $hashed_password = password_hash($password, PASSWORD_BCRYPT);
            $hashed_confirm_password = password_hash($confirm_password, PASSWORD_BCRYPT); // Hash confirm password
            $stmt = $pdo->prepare("INSERT INTO users (name, email, password, confirm_password) VALUES (?, ?, ?, ?)");
            $stmt->execute([$name, $email, $hashed_password, $hashed_confirm_password]);

            if ($stmt->rowCount() > 0) {
                // Retrieve the user_id of the newly inserted user
                $user_id = $pdo->lastInsertId();

                // Set session variables
                $_SESSION["loggedin"] = true;
                $_SESSION["name"] = $name;
                $_SESSION["email"] = $email;
                $_SESSION["user_id"] = $user_id;

                // Sanitize cookie name
                $cookie_name = str_replace(' ', '_', $name); // Replace spaces with underscores

                // Set a cookie
                setcookie($cookie_name, md5($email), time() + (86400 * 30), "/"); // " / " => means global cookie

                // Redirect to chat.php or any other page if needed
                header("Location: chat.php");
                exit();
            } else {
                $error = "<p style='color:red'>Error occurred. Please try again later.</p>";
            }
        }
    }
}
