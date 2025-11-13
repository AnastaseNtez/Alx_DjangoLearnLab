Deployment Configuration: Nginx HTTPS Enforcement

This document details the necessary configuration for an Nginx reverse proxy to handle SSL/TLS termination and ensure all traffic is served securely over HTTPS. This complements the SECURE_SSL_REDIRECT settings configured in Django.

Prerequisites

SSL/TLS Certificates: Valid certificates (e.g., fullchain.pem and privkey.pem) must be obtained and installed on the server (e.g., using Certbot/Let's Encrypt).

Gunicorn/uWSGI: The Django application must be running behind an application server, typically listening on localhost:8000.

Nginx Server Block Configuration

Use this configuration template, replacing yourdomain.com and the certificate paths with your actual values.

# 1. HTTP Block (Handles Redirect)
# Listens on standard HTTP port 80.
server {
    listen 80;
    server_name yourdomain.com [www.yourdomain.com](https://www.yourdomain.com);

    # Permanently redirect all HTTP traffic to HTTPS (301 Moved Permanently)
    return 301 https://$host$request_uri;
}

# 2. HTTPS Block (Secure Serving)
# Listens on standard HTTPS port 443.
server {
    listen 443 ssl http2;
    server_name yourdomain.com [www.yourdomain.com](https://www.yourdomain.com);

    # --- SSL Configuration (UPDATE PATHS) ---
    ssl_certificate /etc/letsencrypt/live/[yourdomain.com/fullchain.pem](https://yourdomain.com/fullchain.pem);
    ssl_certificate_key /etc/letsencrypt/live/[yourdomain.com/privkey.pem](https://yourdomain.com/privkey.pem);

    # Optional: Reinforce HSTS header (Django also handles this, but Nginx is faster)
    # add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

    # --- Proxying to Django (Gunicorn/uWSGI) ---
    location / {
        proxy_pass http://localhost:8000; # Target application server
        
        # Essential headers for Django to correctly identify the secure connection:
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme; # Tells Django the request was 'https'
        proxy_set_header Host $host;
    }

    # --- Static and Media Files ---
    # Serve static assets directly via Nginx for performance
    location /static/ {
        alias /path/to/your/LibraryProject/static/;
    }
}


Post-Configuration Steps

Verify the Nginx configuration: sudo nginx -t

Reload Nginx: sudo systemctl reload nginx