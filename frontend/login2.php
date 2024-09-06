<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login | Dr.Intelligent</title>
    <link rel="stylesheet" href="./css/login2.css">
    <link rel="stylesheet" href="./css/all.min.css">
    <link rel="stylesheet" href="./css/normali.css">
    <link rel="shortcut icon" href="./images/logo.svg">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto+Mono&display=swap" rel="stylesheet">
</head>

<body>
    <div class="container">

        <div class="left">
            <div class="logo-name">
                <a href="./Home2.php"><i class="fa-solid fa-comments" style="color: #4db2fe;"></i></a>
                <h4>Doctor Intelligent</h4>
            </div>
            <div class="text">
                <h5>Nice to see you again</h5>
                <div>
                    <h1>Welcome Back</h1>
                </div>
            </div>
        </div>

        <div class="right">
            <div class="additional">
                <a href="#home"><i class="fa-solid fa-comments" style="color: #4db2fe;"></i></a>
                <h4>Doctor Intelligent</h4>
            </div>
            <div class="right-h">
                <h1>Login Account</h1>
                <h5>Enter your account information below</h5>
            </div>

            <form action="" method="post">
                <div class="form-group">
                    <input type="email" id="email" name="email" placeholder="Enter Email" >
                </div>
                <div class="form-group">
                    <input type="password" id="password" name="password" placeholder="Enter Password" >
                </div>
                <div class="form-group-checkbox">
                    <input type="checkbox" id="keep-signed-in" name="keep-signed-in">
                    <label for="keep-signed-in">Keep me signed in</label>
                </div>
                <?php include_once("./php/login_pro.php");
                if (isset($errors)) {
                    echo '<div class="error">' . $errors . '</div>';
                }
                ?>
                <div class="form-group-forget">
                    <a href="#">Forget password?</a>
                </div>
                <div class="form-group-button">
                    <button type="submit" class="btn">Login</button>
                </div>
                <p>Don't have an account? <a href="./signup2.php">Sign up</a></p>
            </form>

        </div>

    </div>
</body>

</html>