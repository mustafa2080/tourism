# Production Deployment Guide

1. Install production requirements:
```bash
pip install -r requirements.txt
```

2. Set environment variables:
```bash
export DEBUG=False
export SECRET_KEY='your-secure-secret-key'
export ALLOWED_HOSTS='yourdomain.com,www.yourdomain.com'
```

3. Collect static files:
```bash
python manage.py collectstatic --noinput
```

4. Start Gunicorn:
```bash
gunicorn tourism_project.wsgi:application --bind 0.0.0.0:8000
```

5. Configure Nginx as reverse proxy (example config):
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        alias /path/to/your/staticfiles/;
    }

    location /media/ {
        alias /path/to/your/media/;
    }
}
```
