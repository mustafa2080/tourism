# Tourism Project 🌍

A comprehensive Django-based tourism website with multi-language support, booking system, payment integration, and modern UI.

## Features ✨

- **Multi-language Support**: Arabic, English, French, German
- **Tour Management**: Browse and book tours with detailed information
- **User Authentication**: Registration, login with social auth support
- **Booking System**: Complete booking workflow with payment integration
- **PayPal Integration**: Secure payment processing
- **Blog System**: Travel blog with categories and comments
- **Review System**: User reviews and ratings for tours
- **Admin Dashboard**: Comprehensive admin interface with analytics
- **Responsive Design**: Mobile-first design with Tailwind CSS
- **API Support**: RESTful API for mobile apps and integrations

## Tech Stack 🛠️

- **Backend**: Django 5.2, Django REST Framework
- **Frontend**: Tailwind CSS, Alpine.js, HTML5
- **Database**: SQLite (development), PostgreSQL (production)
- **Payment**: PayPal API
- **Deployment**: Railway
- **Authentication**: Django Allauth
- **Internationalization**: Django Model Translation

## Quick Start 🚀

### Prerequisites
- Python 3.12+
- Node.js 18+
- npm 9+

### Local Development

1. **Clone the repository**
```bash
git clone <repository-url>
cd tourism_project2
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
npm install
```

4. **Build CSS**
```bash
npm run build
```

5. **Run migrations**
```bash
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Run development server**
```bash
python manage.py runserver
```

Visit `http://localhost:8000` to see the application.

### Environment Variables

The project uses environment variables for configuration. These are loaded from a `.env` file in development. In production (e.g., on Render), these are set as environment variables.

#### Critical Environment Variables

- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to `True` in development, `False` in production
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DATABASE_URL`: Database connection string

#### Payment Integration

- `PAYPAL_MODE`: Either `sandbox` or `live`
- `PAYPAL_CLIENT_ID`: Your PayPal client ID
- `PAYPAL_SECRET`: Your PayPal secret key

#### Social Authentication

- `GOOGLE_CLIENT_ID`: Your Google OAuth client ID
- `GOOGLE_CLIENT_SECRET`: Your Google OAuth client secret

## Deployment to Render

This project is configured for deployment on Render.com.

1. Push your code to GitHub (make sure `.env` is in `.gitignore`).

2. Create a new Web Service on Render:
   - Connect your GitHub repository
   - Select "Python" as the environment
   - Set the build command to `./build.sh`
   - Set the start command to `gunicorn tourism_project.wsgi:application`

3. Add environment variables in the Render dashboard:
   - All the variables from your `.env` file (except development-specific ones)
   - Set `RENDER=true` to enable Render-specific settings

4. Deploy the service.

## Security Notes

- Never commit `.env` files or any files containing secrets to version control.
- Use environment variables for all sensitive information.
- In production, always use HTTPS and set appropriate security headers.
