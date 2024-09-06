<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="./css/chat.css">
  <link rel="stylesheet" href="./css/all.min.css">
  <link rel="stylesheet" href="./css/normali.css">
  <link rel="shortcut icon" href="./images/logo.svg">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />


  <title>Chat | Dr.Intelligent</title>
</head>

<body>
  <div class="container">
    <div class="left">
      <div class="new-chat">
        <button type="menu">
          <i class="fa-solid fa-comments"></i>
          <h3>New Chat</h3>
        </button>
      </div>
      <div class="history">
        <a href="./php/select_chathistory.php"><span class="material-symbols-outlined">
            history
          </span> History</a>
      </div>
    </div>
    <div class="right">
      <div class="header">
        <a href="./Home2.php">Dr.Intelligent</a>
        <div class="versions">


          <select id="languageSelect">
            <option value="EN" id="EN">English</option>
            <option value="AR" id="AR">عربي</option>
          </select>
          <label for="VectorDB">VectorDB</label>
          <input type="checkbox" id="VectorDB" name="VectorDB" value="true">
          <button class="ver3.5" id="ver3Button">GPT 3.5</button>
          <button class="ver4" id="ver4Button">GPT 4</button>
          <a href="./php/select_chathistory.php"><span class="material-symbols-outlined">
              history
            </span> History</a>
        </div>
      </div>

      <iframe id="versionFrame" frameborder="0" height="100%"></iframe>
    </div>
  </div>

  <script src="./js/chat.js">
  </script>
</body>

</html>