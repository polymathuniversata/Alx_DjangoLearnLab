# Deployment & HTTPS Configuration Guide

This document explains how to deploy LibraryProject securely with HTTPS enforced.

## 1. Django HTTPS & Secure Headers
- All relevant settings are configured in `settings.py`:
  - `SECURE_SSL_REDIRECT = True`: Redirects all HTTP to HTTPS.
  - `SECURE_HSTS_SECONDS = 31536000`: Enforces HTTPS for 1 year.
  - `SECURE_HSTS_INCLUDE_SUBDOMAINS = True`: Applies HSTS to all subdomains.
  - `SECURE_HSTS_PRELOAD = True`: Allows browser preload.
  - `SESSION_COOKIE_SECURE = True`, `CSRF_COOKIE_SECURE = True`: Secure cookies only over HTTPS.
  - `X_FRAME_OPTIONS`, `SECURE_CONTENT_TYPE_NOSNIFF`, `SECURE_BROWSER_XSS_FILTER`: Secure headers.

## 2. Web Server SSL Setup

### Nginx Example
```
server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$host$request_uri;
}
```

- Use [Let's Encrypt](https://letsencrypt.org/) for free SSL certificates.
- Remember to reload/restart nginx after certificate installation.

### Apache Example
```
<VirtualHost *:443>
    ServerName yourdomain.com
    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/yourdomain.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/yourdomain.com/privkey.pem
    # ...proxy config as above...
</VirtualHost>

<VirtualHost *:80>
    ServerName yourdomain.com
    Redirect permanent / https://yourdomain.com/
</VirtualHost>
```

## 3. Security Review
- All Django settings for HTTPS and secure headers are documented in `settings.py`.
- Web server is configured to enforce HTTPS and redirect all HTTP.
- SSL certificates are required for production deployments.

## 4. Improvements
- Use environment variables for all secrets and sensitive settings.
- Regularly update dependencies and review security advisories.
- Consider automated security scanning and monitoring.

---
For further info, see Django docs: https://docs.djangoproject.com/en/4.2/topics/security/
