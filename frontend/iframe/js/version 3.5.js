document.addEventListener("DOMContentLoaded", function () {
  const inputField = document.querySelector(".chat-footer input[type='text']");
  const sendButton = document.querySelector(".chat-footer button");
  const chatBody = document.querySelector(".chat-body");
  var div = document.getElementById('scrollableDiv');
  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);
  const language = urlParams.get('lang');
  const vdb = urlParams.get('vdb');
  let link;

  // Log the inputField to ensure it's selected
  console.log("Input Field:", inputField);

  if (language === "EN" && vdb === "on") {
    link = "http://localhost:49664/v2e";
    const responseElement = document.createElement("div");
    responseElement.classList.add("message", "incoming");
    responseElement.innerHTML = `<p>${"Hello, how can I assist you today?"}</p>`;
    chatBody.appendChild(responseElement);
  } else if (language === "AR" && vdb === "on") {
    link = "http://localhost:49664/v2a";
    const responseElement = document.createElement("div");
    responseElement.classList.add("message", "incoming");
    responseElement.innerHTML = `<p>${"مرحباً، كيف يمكنني مساعدتك اليوم؟"}</p>`;
    chatBody.appendChild(responseElement);
  } else if (language === "EN" && vdb === "off") {
    link = "http://localhost:49664/v1e";
    const responseElement = document.createElement("div");
    responseElement.classList.add("message", "incoming");
    responseElement.innerHTML = `<p>${"Hello, how can I assist you today?"}</p>`;
    chatBody.appendChild(responseElement);
  } else if (language === "AR" && vdb === "off") {
    link = "http://localhost:49664/v1a";
    const responseElement = document.createElement("div");
    responseElement.classList.add("message", "incoming");
    responseElement.innerHTML = `<p>${"مرحباً، كيف يمكنني مساعدتك اليوم؟"}</p>`;
    chatBody.appendChild(responseElement);
  }

  console.log(vdb);
  console.log(language);
  console.log(link);

  div.scrollTop = div.scrollHeight;

  // Function to handle sending messages
  function sendMessage(messageText) {
    const messageElement = document.createElement("div");
    messageElement.classList.add("message", "outgoing");
    messageElement.innerHTML = `<p>${messageText}</p>`;
    chatBody.appendChild(messageElement);
    // Scroll to bottom of chat body
    chatBody.scrollTop = chatBody.scrollHeight;

    fetch(link, {
      body: JSON.stringify({ "question": messageText, "chat_history": "", "GPT": "gpt-4" }),
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error(`Server error: ${res.status}`);
        }
        return res.json();
      })
      .then((data) => {
        console.log(data);
        if (data && data.response) {
          generateResponse(data.response);
        } else {
          throw new Error('Invalid response format');
        }
      })
      .catch((err) => {
        console.error("Fetch error:", err);
        alert("Something went wrong. Please try again later.");
      });
  }

  // Function to generate automated response
  function generateResponse(messageText) {
    const responseElement = document.createElement("div");
    responseElement.classList.add("message", "incoming");

    // Split message into lines
    const lines = messageText.split("\n");

    // Build paragraph for each line
    let paragraphContent = "";
    for (const line of lines) {
      paragraphContent += `<p>${line}</p>`;
    }

    responseElement.innerHTML = `${paragraphContent}`;
    chatBody.appendChild(responseElement);
    // Scroll to bottom of chat body
    chatBody.scrollTop = chatBody.scrollHeight;
  }

  // Add a try-catch block for error handling
  try {
    // Event listener for sending message when Enter is pressed
    inputField.addEventListener("keypress", function (event) {
      if (event.key === "Enter") {
        event.preventDefault();
        const messageText = inputField.value.trim();
        if (messageText !== "") {
          sendMessage(messageText);
          inputField.value = "";
        }
      }
    });

    // Event listener for sending message when send button is clicked
    sendButton.addEventListener("click", function () {
      const messageText = inputField.value.trim();
      if (messageText !== "") {
        sendMessage(messageText);
        inputField.value = "";
      }
    });
  } catch (error) {
    console.error("Error adding event listener:", error);
  }
});

function toggleLeftMenu() {
  var leftMenu = document.querySelector(".left");
  leftMenu.classList.toggle("show");
}
