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

  let reply = "Please ask about services, products, pricing, shipping, or contact details.";

// General Greetings
if (message.toLowerCase().includes("hi")) {
  reply = "Hello! Welcome to OM Industries India. How can I assist you today?";
} 
else if (message.toLowerCase().includes("hello")) {
  reply = "Hi there! Are you looking for industrial products?";
} 
else if (message.toLowerCase().includes("good morning")) {
  reply = "Good morning! Welcome to OM Industries. How may we help you?";
}

// About Company
else if (message.toLowerCase().includes("what is om industries")) {
  reply = "OM Industries is a trusted manufacturer and supplier of high-quality industrial equipment and hydraulic products.";
} 
else if (message.toLowerCase().includes("when was om industries established")) {
  reply = "OM Industries has years of experience in manufacturing and supplying industrial solutions.";
} 
else if (message.toLowerCase().includes("where is om industries located") || message.toLowerCase().includes("location")) {
  reply = "We are located in India. Please visit our Contact page for complete address details.";
} 
else if (message.toLowerCase().includes("why should i choose")) {
  reply = "We offer high-quality products, competitive pricing, and reliable customer support.";
}

// Products Related
else if (message.toLowerCase().includes("what products do you manufacture")) {
  reply = "We manufacture hydraulic thrusters, industrial cylinders, and other heavy-duty industrial equipment.";
} 
else if (message.toLowerCase().includes("hydraulic thruster")) {
  reply = "Yes, OM Industries specializes in high-performance hydraulic thrusters.";
} 
else if (message.toLowerCase().includes("industrial cylinder")) {
  reply = "Yes, we manufacture durable and high-quality industrial cylinders.";
} 
else if (message.toLowerCase().includes("product specification")) {
  reply = "Yes, detailed product specifications are available on each product page.";
} 
else if (message.toLowerCase().includes("custom") || message.toLowerCase().includes("customizable")) {
  reply = "Yes, we provide customized solutions based on customer requirements.";
}

// Orders & Pricing
else if (message.toLowerCase().includes("place an order") || message.toLowerCase().includes("how can i order")) {
  reply = "You can place an order by contacting us through the inquiry form or calling our sales team.";
} 
else if (message.toLowerCase().includes("price") || message.toLowerCase().includes("quotation")) {
  reply = "Pricing depends on model and specifications. Please contact us for a quotation.";
} 
else if (message.toLowerCase().includes("bulk")) {
  reply = "Yes, we offer special pricing for bulk orders.";
} 
else if (message.toLowerCase().includes("minimum order")) {
  reply = "Minimum order quantity depends on the product. Please contact our sales team.";
}

// Technical Support
else if (message.toLowerCase().includes("installation")) {
  reply = "Yes, we provide technical guidance for installation.";
} 
else if (message.toLowerCase().includes("after sales") || message.toLowerCase().includes("after-sales")) {
  reply = "Yes, we provide reliable after-sales support.";
} 
else if (message.toLowerCase().includes("warranty")) {
  reply = "Warranty details depend on the product. Please check the product page or contact us.";
} 
else if (message.toLowerCase().includes("issue") || message.toLowerCase().includes("problem")) {
  reply = "Please share your product details and issue description. Our technical team will assist you.";
}

// Shipping & Delivery
else if (message.toLowerCase().includes("deliver across india")) {
  reply = "Yes, we deliver products across India.";
} 
else if (message.toLowerCase().includes("export")) {
  reply = "Yes, we also export to international markets.";
} 
else if (message.toLowerCase().includes("delivery time")) {
  reply = "Delivery time depends on product availability and order size.";
}

// Contact & Business Inquiry
else if (message.toLowerCase().includes("contact")) {
  reply = "You can contact us through phone, email, or by filling out the contact form.";
} 
else if (message.toLowerCase().includes("email address")) {
  reply = "Please check our Contact page for official email details.";
} 
else if (message.toLowerCase().includes("distributor")) {
  reply = "Yes, please contact us with your business details for distributor opportunities.";
}

// Quality & Certification
else if (message.toLowerCase().includes("certified")) {
  reply = "Yes, our products meet industry quality standards.";
} 
else if (message.toLowerCase().includes("test before delivery") || message.toLowerCase().includes("tested")) {
  reply = "Yes, all products are tested before dispatch.";
}

// Services
else if (message.toLowerCase().includes("service")) {
  reply = "We provide CNG hydro plant testing, manufacturing, and customized industrial solutions.";
}

  chatBody.innerHTML += `<p><strong>Bot:</strong> ${reply}</p>`;
  input.value = "";
  chatBody.scrollTop = chatBody.scrollHeight;
}
