<?php
session_start();
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "chatbot";
$conn = mysqli_connect($servername, $username, $password, $dbname);
$sql = "SELECT user_question, model_reply FROM messages";
$result = mysqli_query($conn, $sql);

if (mysqli_num_rows($result) > 0) {
    echo "<div class='container-fluid'>";
    echo "<div class='table-responsive'>";
    echo "<table class='table table-striped table-bordered chat-history-table'>";
    echo "<thead class='thead-light'>";
    echo "<tr>";
    echo "<th>User Question</th>";
    echo "<th>Model Reply</th>";
    echo "</tr>";
    echo "</thead>";
    echo "<tbody>";

    while ($row = mysqli_fetch_array($result)) {
        echo "<tr>";
        echo "<td>" . $row['user_question'] . "</td>";
        echo "<td class='model-reply-container'>";
        echo "<div class='model-reply-content'>" . $row['model_reply'] . "</div>";
        echo "</td>";
        echo "</tr>";
    }

    echo "</tbody>";
    echo "</table>";
    echo "</div>"; // Close table-responsive
    echo "</div>"; // Close container-fluid
} else {
    echo ucwords("<div class='model-reply-container'> no data to show at this time (<a href='../chat.php'>chat here...!</a>)</div>");
}

mysqli_close($conn);
?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chat_history</title>
    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <style>
        /* General styling for the chat history table */
        .chat-history-table {
            width: 100%;
            border-collapse: collapse;
            border-spacing: 0;
            margin-top: 15px;
        }

        /* Styling for table headers */
        .chat-history-table th,
        .chat-history-table td {
            padding: 12px;
            border: 1px solid #ddd;
        }

        .chat-history-table th {
            background-color: #f2f2f2;
            font-weight: bold;
            text-align: center;
        }

        /* Styling for table rows */
        .chat-history-table tr:nth-child(even) {
            background-color: #f9f9f9;
        }

        /* Styling for the model reply container */
        .model-reply-container {
            max-width: 390px;
            overflow-y: auto;
            margin: 0 auto;
            /* Center the container horizontally */
            padding: 8px;
            margin-top: 290px;
            border-radius: 5px;
            background-color: #e9ecef;
        }

        .model-reply-content {
            line-height: 1.5;
            /* Improved readability with increased line height */
        }
    </style>
</head>

<body>
</body>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>

</html>