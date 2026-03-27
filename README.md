# OM Industries

A modern Flask-based web application for industrial products, services, and order management with built-in feedback, contact forms, and admin dashboard.

## Description

OM Industries is a comprehensive business management platform designed for industrial companies to:
- Showcase products and services with detailed descriptions and galleries
- Accept customer orders and manage order fulfillment
- Collect customer feedback and contact inquiries
- Provide an admin dashboard for managing all business operations
- Support multiple database backends (SQLite for local, PostgreSQL for production)

The app features a responsive Bootstrap-based UI with smooth animations, search functionality, and a built-in chatbot widget for customer engagement.

## Features

### Public Features
- **Product & Services Catalog**: Browse industrial products and services by division
- **Service Details**: View comprehensive service information with galleries
- **Search**: Real-time product and service search
- **Order Placement**: Easy-to-use order form with validation
- **Feedback**: Customer rating and feedback submission
- **Contact**: Contact form for inquiries
- **Chatbot**: Embedded AI-powered chat widget for customer support

### Admin Features
- **Dashboard**: Overview of orders, feedback, contacts, and services
- **Order Management**: Create, view, edit, and track orders with status updates
- **Service Management**: Add, edit, and manage services with galleries
- **Feedback Management**: Review and manage customer feedback
- **Contact Management**: Track and manage customer inquiries
- **User Management**: Admin user administration (basic auth)

## Tech Stack

- **Backend**: Python 3.x + Flask
- **Database**: SQLite (local) / PostgreSQL (production)
- **Frontend**: Bootstrap 5, Jinja2 templating
- **Styling**: Custom CSS with animations
- **JavaScript**: jQuery, Font Awesome icons, Slick carousel, AOS
- **Email**: SMTP for contact notifications

## Project Structure

```
omIndustries/
├── app.py                          # Main Flask application
├── products_data.py                # Service/product seed data
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment template
├── Dockerfile                      # Container config
├── runtime.txt                     # Python version
├── Procfile                        # Deployment config
│
├── templates/
│   ├── public/                     # Public-facing pages
│   │   ├── base_public.html        # Base layout with header/footer
│   │   ├── components/
│   │   │   ├── header_public.html  # Fixed navigation header
│   │   │   └── footer_public.html  # Footer with links
│   │   └── pages/
│   │       ├── home.html           # Landing page
│   │       ├── about.html          # About page
│   │       ├── services.html       # Services listing
│   │       ├── service_detail.html # Individual service
│   │       ├── product_detail.html # Product information
│   │       ├── contact.html        # Contact form
│   │       ├── feedback.html       # Feedback form
│   │       └── search_results.html # Search results page
│   │
│   └── admin/                      # Admin dashboard
│       ├── base_admin.html         # Admin layout
│       ├── components/
│       │   ├── header_admin.html   # Admin header
│       │   └── footer_admin.html   # Admin footer
│       └── pages/
│           ├── login.html          # Admin login
│           ├── dashboard.html      # Admin overview
│           ├── orders.html         # Orders list
│           ├── order_add.html      # Add order
│           ├── order_detail.html   # Order detail
│           ├── services.html       # Services management
│           ├── service_edit.html   # Edit service
│           ├── feedback.html       # Feedback list
│           ├── contacts.html       # Contacts list
│           └── users.html          # User management
│
├── static/
│   ├── css/
│   │   ├── bootstrap.min.css       # Bootstrap 5
│   │   ├── style.css               # Custom styles
│   │   └── chatbot.css             # Chatbot widget styles
│   ├── js/
│   │   ├── bootstrap.bundle.min.js # Bootstrap JS
│   │   ├── jquery-3.7.1.min.js     # jQuery
│   │   ├── script.js               # Main JS
│   │   ├── search.js               # Search functionality
│   │   └── chatbot.js              # Chatbot widget
│   └── image/
│       └── products/               # Product images
│
├── __pycache__/                    # Python cache
└── database.db                     # SQLite database (auto-created)
```

## Setup & Installation

### Prerequisites
- Python 3.7+
- pip (Python package manager)
- Git

### Local Setup (SQLite)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd omIndustries
   ```

2. **Create virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create `.env` file** (optional for local SQLite)
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` if needed:
   ```env
   # Default: uses SQLite (database.db)
   # For PostgreSQL, add:
   # DATABASE_URL=postgresql://user:password@host:port/database
   
   SECRET_KEY=your-secret-key-change-this
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   ```

5. **Run the application**
   ```bash
   python app.py
   ```
   
   The app will be available at `http://localhost:5000`

### Database Options

#### Using SQLite (Default - No Configuration Needed)
- Database file `database.db` is auto-created on first run
- Perfect for development and small deployments
- No external service required

#### Using PostgreSQL (Production)

1. **Create a database** (e.g., Supabase - 500MB free)
   - Visit https://supabase.com
   - Create project and get connection string

2. **Install PostgreSQL driver**
   ```bash
   pip install psycopg2-binary
   ```

3. **Set DATABASE_URL in `.env`**
   ```env
   DATABASE_URL=postgresql://user:password@host:port/database
   ```

4. **Run app**
   ```bash
   python app.py
   ```
   - Tables auto-created on startup

## Admin Login

Default credentials (change in production):
- **Username**: `admin`
- **Password**: `your password`

Access admin panel: `http://localhost:5000/admin`

## Pages and Routes

### Public Pages
| Page | Route | Description |
|------|-------|-------------|
| Home | `/` | Landing page with featured services |
| About | `/about` | Company information |
| Services | `/services` | Services listing by division |
| Service Detail | `/service/<slug>` | Detailed service page |
| Product Detail | `/product/<id>` | Product information |
| Search | `/search` | Search results page |
| Contact | `/contact` | Contact form |
| Feedback | `/feedback` | Feedback submission |

### Admin Pages
| Page | Route | Description |
|------|-------|-------------|
| Login | `/admin` | Admin authentication |
| Dashboard | `/admin/dashboard` | Overview and stats |
| Orders | `/admin/orders` | Order management |
| Services | `/admin/services` | Service management |
| Feedback | `/admin/feedback` | Feedback review |
| Contacts | `/admin/contacts` | Contact inquiries |
| Users | `/admin/users` | User management |

## Configuration

### Environment Variables (`.env`)
```env
# Database
DATABASE_URL=postgresql://...  # Optional, uses SQLite if not set

# Security
SECRET_KEY=your-secret-key

# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# App Settings
DEBUG=False
FLASK_ENV=production
```

## API Endpoints

Search is available via JSON endpoint:
```bash
GET /search?q=<query>
```
Returns JSON with matching products/services.

## Deployment

### Railway
1. Push code to GitHub
2. Connect repository to Railway
3. Set `DATABASE_URL` environment variable
4. Deploy automatically

### Heroku
1. Create `Procfile` (included)
2. Set config vars:
   ```bash
   heroku config:set DATABASE_URL=postgresql://...
   heroku config:set SECRET_KEY=your-key
   ```
3. Deploy:
   ```bash
   git push heroku main
   ```

### Docker
```bash
docker build -t omindustries .
docker run -p 5000:5000 omindustries
```

## Features Currently Implemented

- ✅ Product/Service catalog with search
- ✅ Order management system
- ✅ Customer feedback with ratings
- ✅ Contact form with email notifications
- ✅ Admin dashboard with CRUD operations
- ✅ Fixed navigation header
- ✅ Responsive Bootstrap design
- ✅ Chatbot widget integration
- ✅ Database agnostic (SQLite/PostgreSQL)
- ✅ Email notifications via SMTP

## Recommended Improvements

- Add password hashing for admin accounts
- Implement CSRF protection (Flask-WTF)
- Add user roles and permissions
- Create unit tests
- Add pagination for large datasets
- Implement image upload and optimization
- Add Two-Factor Authentication (2FA)
- Set up logging and monitoring
- Add API documentation (Swagger/OpenAPI)

## Troubleshooting

### Database Connection Issues
```bash
# Check psycopg2 is installed for PostgreSQL
pip install psycopg2-binary

# Verify DATABASE_URL format
# postgresql://user:password@host:port/database
```

### Port Already in Use
```bash
# Run on different port
python app.py --port 8000
```

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## File References

- **Technical Spec**: [TECHNICAL_SPEC.md](TECHNICAL_SPEC.md)
- **Setup Guides**: 
  - [SUPABASE_SETUP.md](SUPABASE_SETUP.md)
  - [RAILWAY_DEPLOY.md](RAILWAY_DEPLOY.md)
  - [QUICK_SETUP.md](QUICK_SETUP.md)

## Support

For issues, feature requests, or contributions:
1. Check existing documentation
2. Review troubleshooting section
3. Contact: omindustriesindia2024@gmail.com

## License

[Add your license information here]

## Version History

- **v1.0** - Initial release with full feature set
  - Products/services catalog
  - Order management
  - Feedback system
  - Admin dashboard
  - Fixed header navigation