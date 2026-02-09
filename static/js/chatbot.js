function toggleChat() {
  const bot = document.getElementById("chatbot");
  bot.style.display = (bot.style.display === "none" || bot.style.display === "")
    ? "block"
    : "none";
}

function sendMessage() {
  const input = document.getElementById("userInput");
  const message = input.value.trim();
  const chatBody = document.getElementById("chat-body");

  if (message === "") return;

  chatBody.innerHTML += `<p><strong>You:</strong> ${message}</p>`;

  let reply = "Please ask about services, location, or contact details.";

  if (message.toLowerCase().includes("service")) {
    reply = "We provide CNG hydro plant testing, manufacturing, and customized industrial solutions.";
  } else if (message.toLowerCase().includes("location")) {
    reply = "OM Industries India is located in Vikhroli, Mumbai.";
  } else if (message.toLowerCase().includes("contact")) {
    reply = "Contact details are available on our Contact page.";
  } else if (message.toLowerCase().includes("manufacture")) {
    reply = "Yes, we manufacture products based on customer requirements.";
  }

  chatBody.innerHTML += `<p><strong>Bot:</strong> ${reply}</p>`;
  input.value = "";
  chatBody.scrollTop = chatBody.scrollHeight;
}
