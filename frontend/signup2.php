<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sign Up | Dr.Intelligent</title>
    <link rel="stylesheet" href="./css/signup2.css">
    <link rel="stylesheet" href="./css/all.min.css">
    <link rel="stylesheet" href="./css/normali.css">
    <link rel="shortcut icon" href="./images/logo.svg">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto+Mono&display=swap" rel="stylesheet">
</head>

<body>
    <div class="container">

        <div class="right">
            <div class="additional">
                <a href="./Home2.php"><i class="fa-solid fa-comments" style="color: #4db2fe;"></i></a>
                <h4>Doctor Intelligent</h4>
            </div>
            <div class="right-h">
                <h1>Sign up Account</h1>
                <h5>Enter your account information below</h5>
            </div>

            <form action="" method="post">
                <div class="form-group">
                    <input type="text" id="username" name="name" placeholder="Enter Username">
                </div>
                <div class="form-group">
                    <input type="email" id="email" name="email" placeholder="Enter Email">
                </div>
                <div class="form-group">
                    <input type="password" id="password" name="password" placeholder="Enter Password">
                </div>
                <div class="form-group">
                    <input type="password" id="password" name="confirm_password" placeholder="Confirm Password">
                </div>

                <?php include_once("./php/pro_signup2.php");
                if (isset($error)) {
                    echo $error;
                } ?>
                <div class="form-group-button">
                    <button type="submit" class="btn">Sign Up</button>
                </div>
                <p>Already have an account? <a href="./login2.php">Login</a></p>
            </form>

        </div>


        <div class="left">
            <div class="logo-name">
                <a href="./Home2.php"><i class="fa-solid fa-comments" style="color: #4db2fe;"></i></a>
                <h4>Doctor Intelligent</h4>
            </div>
            <div class="text">
                <h5>Nice to see you</h5>
                <div>
                    <h1>Create your account</h1>
                </div>
                <h6>Experience the future of healthcare with Intelligent Doctor. Log in now to access your account and
                    unlock a world of possibilities.</h6>
            </div>
        </div>

    </div>
</body>

</html>