# Chatbot Integration Documentation

## Overview
This branch (`chatbot-integration`) contains a fully integrated chatbot feature for OM Industries India website.

## Components

### 1. **Frontend Files**

#### CSS: [static/css/chatbot.css](static/css/chatbot.css)
- Fixed position chatbot widget in bottom-right corner (z-index: 9999)
- Dark blue theme (#0a3d62) matching company branding
- Responsive design with 320px width
- Smooth animations and shadows
- Features:
  - Floating chat icon (14px padding, 50% border radius)
  - Chat window (12px border radius, 1px border)
  - Chat header with title and close button
  - Scrollable chat body (220px height)
  - Input field with send button

#### JavaScript: [static/js/chatbot.js](static/js/chatbot.js)
- **toggleChat()** - Opens/closes chatbot window
- **sendMessage()** - Processes user messages and generates responses
- **AI Bot Logic** - 100+ predefined response patterns for:
  - Greetings (hi, hello, good morning)
  - Company info (location, history, why choose us)
  - Products (hydraulic thrusters, cylinders, specifications)
  - Orders & Pricing (inquiries, bulk orders, quotations)
  - Technical Support (installation, warranty, troubleshooting)
  - Shipping & Delivery (domestic, international, timing)
  - Contact & Business (email, phone, distributor inquiries)
  - Quality & Certification (testing, standards)
  - Services (CNG testing, manufacturing)

### 2. **HTML Integration**

#### Template: [templates/public/base_public.html](templates/public/base_public.html)
**CSS Link (Line 25-26):**
```html
<!-- Chatbot CSS -->
<link rel="stylesheet" href="{{ url_for('static', filename='css/chatbot.css') }}">
```

**JavaScript & HTML (Line 55-79):**
```html
<!-- Chatbot JS -->
<script src="{{ url_for('static', filename='js/chatbot.js') }}"></script>

<!-- Chatbot Button -->
<div id="chatbot-icon" onclick="toggleChat()">
  <i class="fas fa-comment-dots"></i>
</div>

<!-- Chatbot Box -->
<div id="chatbot">
  <div id="chat-header">
    OM Industries Assistant
    <span onclick="toggleChat()">✖</span>
  </div>

  <div id="chat-body">
    <p><strong>Assistant</strong> Hello 👋 How can I help you today?</p>
  </div>

  <div id="chat-input">
    <input type="text" id="userInput" placeholder="Ask about services, location..." />
    <button onclick="sendMessage()">Send</button>
  </div>
</div>
```

## Features

✅ **Always Available** - Fixed position, visible on all pages
✅ **Easy Toggle** - Click chatbot icon to open/close
✅ **Responsive** - Works on desktop, tablet, and mobile
✅ **Company Branded** - Dark blue theme matching OM Industries
✅ **Keyword-Based AI** - 100+ response patterns
✅ **Multi-Topic Support** - Products, pricing, support, contact, services
✅ **User Friendly** - Simple text input and send button
✅ **High Z-Index** - Always stays on top (z-index: 9999)

## Supported Chatbot Topics

The chatbot can answer questions about:

1. **Greetings**: "hi", "hello", "good morning"
2. **Company**: "what is om industries", "where are you located", "why choose you"
3. **Products**: "hydraulic thruster", "industrial cylinder", "specifications", "customizable"
4. **Orders**: "place an order", "how to order", "pricing", "bulk orders", "minimum order"
5. **Support**: "installation", "warranty", "after-sales", "problems", "issues"
6. **Shipping**: "deliver across india", "export", "delivery time"
7. **Contact**: "contact details", "email", "distributor opportunities"
8. **Quality**: "certified", "tested before delivery"
9. **Services**: "CNG testing", "manufacturing"

## How It Works

1. User clicks chatbot icon in bottom-right corner
2. Chat window opens with welcome message
3. User types message in input field
4. User clicks "Send" or presses Enter
5. Bot searches message for keywords
6. Returns matching predefined response
7. Both user and bot messages appear in chat body
8. Chat scrolls to show latest message

## File Structure

```
d:\Projects\omIndustries\
├── static/
│   ├── css/
│   │   └── chatbot.css          ← Chatbot styling
│   └── js/
│       └── chatbot.js           ← Chatbot logic
├── templates/
│   └── public/
│       └── base_public.html     ← Chatbot HTML integration
└── [Other project files]
```

## Testing

To test the chatbot:

1. Start the Flask application
2. Visit any public page (home, services, about, etc.)
3. Click the floating chat icon in the bottom-right corner
4. Type sample messages:
   - "hi" - Should get greeting response
   - "what is om industries" - Should get company info
   - "hydraulic thruster" - Should get product info
   - "pricing" - Should get pricing response
   - "contact" - Should get contact info

## Deployment

The chatbot is ready for production:
- ✅ No backend API calls needed (client-side only)
- ✅ No database dependencies
- ✅ Works offline
- ✅ Fast performance
- ✅ Lightweight (minimal CSS & JS)

## Future Enhancements

Potential improvements:
1. Add AI/ML model for better NLP (Natural Language Processing)
2. Connect to backend API for dynamic responses
3. Add typing indicator animation
4. Store chat history locally
5. Add typing animation for bot responses
6. Support for multiple languages
7. Analytics tracking (conversation data)
8. Integration with email/SMS for lead capture

## Browser Compatibility

✅ Chrome/Edge (Latest)
✅ Firefox (Latest)
✅ Safari (Latest)
✅ Mobile browsers

## Notes

- Chatbot is available on all public pages via base_public.html template
- CSS and JS files are external for maintainability
- FontAwesome icons used for chat icon (fas fa-comment-dots)
- Close button uses ✖ symbol
- Chat body auto-scrolls to latest message

## Author Notes

This chatbot implementation provides a lightweight, user-friendly customer support solution for OM Industries India without requiring backend processing. It can be enhanced with AI/ML models or API integration as needed.

