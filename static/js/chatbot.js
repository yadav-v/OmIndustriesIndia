// Toggle Chatbot Window
function toggleChatbot() {
  const container = document.getElementById('chatbot-container');
  if (container.style.display === 'none' || container.style.display === '') {
    container.style.display = 'flex';
    document.getElementById('chatbot-input').focus();
  } else {
    container.style.display = 'none';
  }
}

// Handle Enter key
function handleChatKeypress(event) {
  if (event.key === 'Enter') {
    sendChatMessage();
  }
}

// Send Message
function sendChatMessage() {
  const input = document.getElementById('chatbot-input');
  const message = input.value.trim();
  
  if (!message) return;

  // Display user message
  addMessage(message, 'user');
  input.value = '';

  // Get bot response
  const response = getBotResponse(message);
  
  // Display bot response with small delay
  setTimeout(() => {
    addMessage(response, 'bot');
  }, 300);
}

// Add Message to Chat
function addMessage(text, sender) {
  const messagesDiv = document.getElementById('chatbot-messages');
  const messageDiv = document.createElement('div');
  messageDiv.className = `chatbot-message ${sender}-message`;
  
  const p = document.createElement('p');
  p.textContent = text;
  messageDiv.appendChild(p);
  
  messagesDiv.appendChild(messageDiv);
  
  // Scroll to bottom
  messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

// Get Bot Response Based on Keywords
function getBotResponse(message) {
  const msg = message.toLowerCase();
  
  // Greetings
  if (msg.includes('hi') || msg.includes('hello') || msg.includes('hey')) {
    return 'Hello! 👋 Welcome to OM Industries. What can I help you with today?';
  }
  
  // Company Info
  if (msg.includes('who are you') || msg.includes('about om') || msg.includes('who is om')) {
    return 'OM Industries is a trusted manufacturer of high-quality industrial equipment and hydraulic solutions for CNG cylinder testing.';
  }
  
  if (msg.includes('location') || msg.includes('where are you') || msg.includes('address')) {
    return 'We are based in India. Please visit our Contact page for complete address and directions.';
  }
  
  if (msg.includes('established') || msg.includes('founded') || msg.includes('since')) {
    return 'OM Industries has years of experience in manufacturing and supplying industrial solutions.';
  }
  
  // Products
  if (msg.includes('product') || msg.includes('what do you') || msg.includes('manufacture')) {
    return 'We manufacture: CNG Cylinder Testing Equipment, Hydraulic Pumps, Water Jackets, Ultrasonic Rollers, Control Panels, and more industrial equipment.';
  }
  
  if (msg.includes('hydraulic') || msg.includes('pump') || msg.includes('hydro')) {
    return 'Yes! We specialize in high-performance hydraulic equipment and pumps. Check our Services page for detailed specs.';
  }
  
  if (msg.includes('cylinder')) {
    return 'We offer CNG cylinder testing equipment with complete solutions including water jackets, fire stands, and testing plants.';
  }
  
  if (msg.includes('specifications') || msg.includes('specs')) {
    return 'Detailed specifications are available on each product page. Want to know about a specific product?';
  }
  
  if (msg.includes('custom') || msg.includes('customize') || msg.includes('tailor')) {
    return 'Yes! We provide customized solutions based on your requirements. Contact our sales team for details.';
  }
  
  // Pricing & Orders
  if (msg.includes('price') || msg.includes('cost') || msg.includes('rate') || msg.includes('quotation') || msg.includes('quote')) {
    return 'Pricing varies by product and specifications. Please contact us or fill the inquiry form for a customized quotation.';
  }
  
  if (msg.includes('order') || msg.includes('purchase') || msg.includes('buy')) {
    return 'You can place an order by contacting us through the website inquiry form, email, or phone. Our sales team will assist you.';
  }
  
  if (msg.includes('bulk') || msg.includes('wholesale') || msg.includes('distributor')) {
    return 'We offer special pricing for bulk orders. Please contact our sales team for wholesale and distributor inquiries.';
  }
  
  if (msg.includes('minimum') || msg.includes('moq')) {
    return 'Minimum order quantity depends on the product. Contact our sales team for specific MOQ details.';
  }
  
  // Shipping & Delivery
  if (msg.includes('shipping') || msg.includes('delivery') || msg.includes('deliver') || msg.includes('ship')) {
    return 'We deliver across India with reliable shipping options. Delivery time depends on your location and order size.';
  }
  
  if (msg.includes('export') || msg.includes('international')) {
    return 'Yes, we export to international markets. Contact us for export inquiries and documentation.';
  }
  
  // Support & Service
  if (msg.includes('support') || msg.includes('help') || msg.includes('assist')) {
    return 'We provide comprehensive support including installation guidance, technical assistance, and after-sales service. How can we help?';
  }
  
  if (msg.includes('install') || msg.includes('installation') || msg.includes('setup')) {
    return 'We provide technical installation guidance and support. Our team can help you with setup and troubleshooting.';
  }
  
  if (msg.includes('warranty') || msg.includes('guarantee')) {
    return 'Warranty details depend on the product. Check the product page or contact us for specific warranty information.';
  }
  
  if (msg.includes('problem') || msg.includes('issue') || msg.includes('trouble') || msg.includes('broken')) {
    return 'Sorry to hear that! Please describe your issue and product details. Our technical team will assist you right away.';
  }
  
  if (msg.includes('after sales') || msg.includes('after-sales') || msg.includes('maintenance')) {
    return 'We provide reliable after-sales support including maintenance guidance and spare parts availability.';
  }
  
  // Contact
  if (msg.includes('contact') || msg.includes('email') || msg.includes('phone') || msg.includes('call')) {
    return 'You can reach us through our Contact page. We also have email and phone support available during business hours.';
  }
  
  if (msg.includes('email address')) {
    return 'Please check our Contact page for official email addresses. You can also submit an inquiry form.';
  }
  
  if (msg.includes('phone') || msg.includes('mobile')) {
    return 'Our phone numbers are listed on the Contact page. We\'re happy to discuss your requirements!';
  }
  
  // Quality & Certification
  if (msg.includes('certificate') || msg.includes('certified') || msg.includes('iso')) {
    return 'Yes, our products meet industry quality standards and certifications. Contact us for specific compliance details.';
  }
  
  if (msg.includes('test') || msg.includes('tested') || msg.includes('quality')) {
    return 'All products are thoroughly tested before dispatch to ensure quality and reliability.';
  }
  
  // Services
  if (msg.includes('service') || msg.includes('testing') || msg.includes('cng')) {
    return 'We provide CNG hydro plant testing, manufacturing, and complete industrial solutions. What specific service interests you?';
  }
  
  // General fallback responses
  if (msg.length < 3) {
    return 'Could you please provide more details? I\'m here to help with product info, pricing, shipping, or support.';
  }
  
  // Default response
  return 'Great question! I didn\'t quite understand. Could you ask about: Products, Pricing, Shipping, Support, or Contact information?';
}

// Auto-scroll to bottom on page load
document.addEventListener('DOMContentLoaded', function() {
  const messagesDiv = document.getElementById('chatbot-messages');
  if (messagesDiv) {
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
  }
});
