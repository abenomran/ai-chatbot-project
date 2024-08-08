const chatLog = document.querySelector("#chat-log");
const userInput = document.querySelector("#userInput");
const userInputForm = document.querySelector("#user-input-form");
const sendBtn = document.querySelector("#send-button");

async function sendMessage() {
  const userMessage = userInput.value;

  chatLog.innerHTML += `<p>${userMessage}</p>`;
  userInput.value = "";
  scrollToBottom();

  const response = await fetch("/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message: userMessage }),
  });

  chatLog.innerHTML += `<p><strong>Bot: </strong></p>`;
  let lastParagraph = chatLog.querySelector("p:last-child");

  const reader = response.body.getReader();
  let output = "";

  while (true) {
    const { done, value } = await reader.read();
    decodedValue = new TextDecoder().decode(value);
    if (decodedValue === "\n") {
      output += "<br></br>";
    } else {
      output += decodedValue;
    }

    console.log(output);
    //lastParagraph.innerHTML += output;
    lastParagraph.innerHTML = `<p><strong>Bot: </strong>${output}</p>`;
    scrollToBottom();

    if (done) {
      return;
    }
  }
}

// Keeps chat view to latest messages
function scrollToBottom() {
  chatLog.scrollTop = chatLog.scrollHeight;
}

userInputForm.addEventListener("input", function () {
  if (userInput.value === null || userInput.value.trim() === "") {
    sendBtn.setAttribute("disabled", "disabled");
    return;
  } else {
    sendBtn.removeAttribute("disabled");
  }
});

userInputForm.addEventListener("submit", function (e) {
  e.preventDefault();
  sendMessage();
});
