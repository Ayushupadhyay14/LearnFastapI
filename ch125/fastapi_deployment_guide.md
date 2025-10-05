# 🚀 Deploying FastAPI Async App on Hostinger VPS (Ubuntu + Nginx + MySQL + Gunicorn + Uvicorn + Certbot)

This guide outlines the steps to deploy a simple **FastAPI async project** on a Hostinger VPS running Ubuntu, with Nginx as a reverse proxy, MySQL as Database, Gunicorn Process Manager, Uvicorn as an ASGI server, and HTTPS via Certbot (Let's Encrypt).

---

## 📦 1. Install Required Packages

```bash
sudo apt update
sudo apt install nginx
sudo apt install mysql-server
sudo apt install php-fpm php-mysql
sudo apt install python3
sudo apt install python3.12-venv
sudo apt install git
```

---

## 🛢️ 2. Setup MySQL Async Database

Login to MySQL:

```bash
sudo mysql -u root -p
```

Then run these SQL commands:

```bash
CREATE USER 'raj'@'localhost' IDENTIFIED WITH caching_sha2_password BY 'raj123';
CREATE DATABASE resume;
GRANT ALL PRIVILEGES ON resume.* TO 'raj'@'localhost';
```

---

## 🔐 3. Setup SSH Key for GitHub Access

Generate a new SSH deploy key:

```bash
ssh-keygen -f /home/raj/.ssh/ch125_ed25519 -t ed25519 -C "ch125repo"
sudo chown -R raj .ssh
cat ~/.ssh/ch125_ed25519.pub
```

### ➕ Add SSH Key to GitHub

- Go to your GitHub repo → **Settings** → **Deploy Keys** → **Add Deploy Key**
- Paste the public key content

### ➕ Configure Multiple Keys

```bash
cd ~/.ssh
sudo nano config
```

Add:

```ssh
Host ch125_project
    HostName github.com
    User github_username
    IdentityFile ~/.ssh/ch125_ed25519
    IdentitiesOnly yes
```

Test SSH:

```bash
ssh -T git@ch125_project
```

---

## ⬇️ 4. Clone Project and Setup Environment

```bash
git clone git@ch125_project:rajeshrajkr4/ch125.git
cd ~/ch125
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

Create .env File or any file if needed (if any)

Test Gunicorn manually:

```bash
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

Ensure port `8000` is open if testing externally.

---

## 🛢️5. Generate Database Tables (If any)

```bash
alembic revision --autogenerate -m "create table"
alembic upgrade head
```

---

## 🛠️ 6. Create a Systemd Service for Gunicorn

```bash
sudo nano /etc/systemd/system/ch125.service
```

Paste:

```ini
[Unit]
Description=Gunicorn instance to serve ch125 FastAPI App
After=network.target

[Service]
User=raj
Group=www-data
WorkingDirectory=/home/raj/ch125
Environment="PATH=/home/raj/ch125/venv/bin"
ExecStart=/home/raj/ch125/venv/bin/gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 127.0.0.1:8000

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl start ch125
sudo systemctl enable ch125
sudo systemctl status ch125
```

View logs:

```bash
sudo journalctl -u ch125 -f
```

---

## 🌐 7. Configure Nginx as a Reverse Proxy

```bash
sudo nano /etc/nginx/sites-available/ch125
```

Paste the following config:

```nginx
# Redirect www to non-www
server {
    listen 80;
    server_name www.javascriptguru.in;
    return 301 $scheme://javascriptguru.in$request_uri;
}

# Main FastAPI App
server {
    listen 80;
    server_name javascriptguru.in;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the Nginx site:

```bash
sudo ln -s /etc/nginx/sites-available/ch125 /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## 🔄 8. Make Code Change Live

Make Code change in VS Code then Push to Github

On VPS :

```bash
cd ch125
git pull
```

Make Code change live restart service

```bash
sudo systemctl restart ch125.service
```

---

## 🔒 9. Secure with HTTPS using Certbot

Install Certbot:

```bash
sudo apt install certbot python3-certbot-nginx
```

Generate SSL certificates and auto-configure Nginx:

```bash
sudo certbot --nginx -d javascriptguru.in -d www.javascriptguru.in
```

---

## ✅ Deployment Complete

- Visit: `https://javascriptguru.in`
- `www.javascriptguru.in` automatically redirects to the main domain

---
