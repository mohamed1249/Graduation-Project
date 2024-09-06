document.addEventListener("DOMContentLoaded", function () {
    // Get references to the buttons and the iframe by ID
    var ver3Button = document.getElementById('ver3Button');
    var ver4Button = document.getElementById('ver4Button');

    var iframe = document.getElementById('versionFrame');

    // Add click event listeners to the buttons
    ver3Button.addEventListener('click', function () {
        // Set the source of the iframe to version 3.5 HTML file
        iframe.src = "./iframe/version%203.5.php";
        const language = document.getElementById("languageSelect").value;
        iframe.src += "?lang=" + language;
        const vdbCheckbox = document.getElementById("VectorDB");
        const vdb = vdbCheckbox.checked ? "on" : "off";

        iframe.src += "&vdb=" + vdb;
    });

    ver4Button.addEventListener('click', function () {
        // Set the source of the iframe to version 4 HTML file
        iframe.src = "./iframe/version%204.php";
        const language = document.getElementById("languageSelect").value;
        iframe.src += "?lang=" + language;
        const vdbCheckbox = document.getElementById("VectorDB");
        const vdb = vdbCheckbox.checked ? "on" : "off";

        iframe.src += "&vdb=" + vdb;


    });
});



