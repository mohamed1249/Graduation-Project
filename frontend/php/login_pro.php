<?php
session_start();
include("./php/connection/connection.php");

$errors = "";
// Check if the form is submitted or API request is made
if ($_SERVER["REQUEST_METHOD"] == "POST" || isset($_GET['api'])) {
    $email = trim($_REQUEST['email']);
    $password = $_REQUEST['password'];

    // Validate email and password (combined check)
    if (empty($email) || empty($password)) {
        $errors = ucwords("<p style='color:red'>Please enter email and password.</p>");
    } else {
        try {
            // Prepared statement to prevent SQL injection
            $stmt = $pdo->prepare("SELECT email, password FROM users WHERE email = ?");
            $stmt->execute([$email]);
            $row = $stmt->fetch(PDO::FETCH_ASSOC);

            if ($row) {
                // Verify password using secure hashing
                if (password_verify($password, $row['password'])) {
                    // Login successful, set session and reset attempt count
                    $_SESSION['user_id'] = $row['id'];
                    $_SESSION['login_attempts'][$email] = 0;
                    session_regenerate_id(true);

                    // Set cookie if keep signed in option is checked
                    if (isset($_POST['keep-signed-in']) && $_POST['keep-signed-in'] == 'on') {
                        setcookie('user_id', $row['id'], time() + (86400 * 30), "/", true, true);
                    }

                    // Check if it's an API request
                    if (isset($_GET['api'])) {
                        echo json_encode(array('success' => true, 'message' => 'Login successful.'));
                        exit();
                    } else {
                        // Redirect if it's a web form submission
                        header("Location: chat.php");
                        exit();
                    }
                } else {
                    $errors = ucwords("<p style='color:red'>Incorrect email or password.</p>");
                }
            } else {
                $errors = ucwords("<p style='color:red'>Incorrect email or password.</p>");
            }
        } catch (PDOException $e) {
            $errors = ucwords("<p style='color:red'>Database error. Please try again later.</p>");
        }
    }
}

if (isset($_GET['api'])) {
    echo json_encode(array('success' => false, 'errors' => $errors));
    exit();
}
