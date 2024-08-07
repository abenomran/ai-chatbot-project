const chatLog = document.querySelector("#chat-log");
const userInput = document.querySelector("#userInput");
const userInputForm = document.querySelector("#user-input-form");
const sendBtn = document.querySelector("#send-button");

async function sendTest() {
  const response = await fetch("http://127.0.0.1:5000/api/test", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
    mode: "cors",
  });

  let resData = await response.json();
}

async function sendMessage() {
  const userMessage = userInput.value;

  chatLog.innerHTML += `<p class="user-text-bubble rounded-pill px-2 py-1 text-white ml-auto">${userMessage}</p>`;
  userInput.value = "";
  scrollToBottom();

  const response = await fetch("http://127.0.0.1:5000/api/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message: userMessage }),
    mode: "cors",
  });

  chatLog.innerHTML += `<p class="px-2 pt-1 mr-auto"></p>`;
  let lastParagraph = chatLog.querySelector("p:last-child");

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let output = "";

  while (true) {
    const { done, value } = await reader.read();

    if (done) {
      return;
    }

    if (value) {
      const decodedValue = decoder.decode(value, { stream: true });
      output += decodedValue.replace(/\n/g, "<br>");
    } else {
      continue;
    }

    // Dynamically switch class based on the content length
    if (output.length > 200) {
      // Adjust this threshold as needed
      lastParagraph.classList.remove("rounded-pill");
      lastParagraph.classList.add("rounded-lg");
    } else {
      lastParagraph.classList.add("rounded-pill");
      lastParagraph.classList.remove("rounded-lg");
    }

    //lastParagraph.innerHTML += output;
    lastParagraph.innerHTML = `<p class="px-2 pt-1 mr-auto">${output}</p>`;
    scrollToBottom();
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

  //sendTest();
});
