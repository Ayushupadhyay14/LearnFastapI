# 🚀 FastAPI ReactJS Docker Deployment

This guide explains how to containerize and deploy a FastAPI and ReactJS Project with Docker, MySQL, SQLAlchemy 2.0, Alembic, Nginx reverse proxy, GitHub and HTTPS on a VPS.

---

## 🐳 1. Dockerfile

fastapi/Dockerfile

```bash
# Stage 1: Install deps
FROM python:3.11-slim AS builder
WORKDIR /fastapi
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Final image
FROM python:3.11-slim
WORKDIR /fastapi

COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

```

reactjs/Dockerfile

```bash
# Stage 1: Build the app
FROM node:20-alpine as build

WORKDIR /reactjs
COPY package.json package-lock.json .
RUN npm ci

COPY . .
RUN npm run build

# Stage 2: Serve with nginx
FROM nginx:alpine

COPY --from=build /reactjs/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

```

---

## 🧩 2. docker-compose.yml

ch130/docker-compose.yml

```yaml
services:
  fastapi:
    build:
      context: ./fastapi
    container_name: fastapi
    env_file:
      - ./fastapi/.env
    expose:
      - "8000"
    volumes:
      - ./fastapi:/fastapi
    depends_on:
      - db
    restart: always
    networks:
      - app-network

  db:
    image: mysql:8.0
    container_name: mysql-db
    restart: always
    env_file:
      - ./fastapi/.env
    environment:
      MYSQL_ROOT_PASSWORD: ${DB_PASS}
      MYSQL_DATABASE: ${DB_NAME}
      MYSQL_USER: ${DB_USER}
      MYSQL_PASSWORD: ${DB_PASS}
    volumes:
      - mysql_data:/var/lib/mysql
    networks:
      - app-network

  reactjs:
    build:
      context: ./reactjs
    container_name: reactjs
    env_file:
      - ./reactjs/.env
    restart: always
    expose:
      - "80"
    networks:
      - app-network

  nginx:
    image: nginx:alpine
    container_name: nginx
    ports:
      - "80:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - fastapi
      - reactjs
    restart: always
    networks:
      - app-network

volumes:
  mysql_data:

networks:
  app-network:
    driver: bridge

```

---

## 📜 3. nginx.conf

ch130/nginx/nginx.conf

```nginx
# Reverse proxy for api.javascriptguru.in
server {
    listen 80;
    server_name api.javascriptguru.in;

    location / {
        proxy_pass http://fastapi:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# for javascriptguru.in
server {
    listen 80;
    server_name javascriptguru.in;

    location / {
        proxy_pass http://reactjs:80/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

```

---

## 📦 4. Install Docker on VPS

```bash
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

---

## 🔐 5. Setup SSH Key for GitHub Access

Generate a new SSH deploy key:

```bash
ssh-keygen -f /home/raj/.ssh/fastreact_ed25519 -t ed25519 -C "fastreactrepo"
sudo chown -R raj .ssh
cat ~/.ssh/fastreact_ed25519.pub
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
Host fastreact_project
    HostName github.com
    User github_username
    IdentityFile ~/.ssh/fastreact_ed25519
    IdentitiesOnly yes
```

Test SSH:

```bash
ssh -T git@fastreact_project
```

---

## ⬇️ 6. Clone Project

```bash
git clone git@fastreact_project:rajeshrajkr4/ch130.git
```

Create .env file if needed

---

## 🚀 7. Build Containers

```bash
cd ch130
sudo docker compose up --build -d
```

---

## 🔁 8. Run Alembic Migrations

```bash
cd ch130
sudo docker compose exec fastapi alembic upgrade head
```

Test with Browser:

```bash
http://javascriptguru.in
```

---

## 🔄 9. Make Code Change Live

Make Code change in VS Code then Push to Github

ON VPS:

```bash
cd ch130
git pull
```

Make Code change live rebuild containers adn run alembic

```bash
cd ch130
sudo docker compose down
sudo docker compose up -d
sudo docker compose exec fastapi alembic upgrade head
```

---

## 🛡️ 10 : Secure with HTTPS using Certbot

Prepare docker-compose.yml for certbot:

```bash
services:
  fastapi:
    build:
      context: ./fastapi
    container_name: fastapi
    env_file:
      - ./fastapi/.env
    expose:
      - "8000"
    volumes:
      - ./fastapi:/fastapi
    depends_on:
      - db
    restart: always
    networks:
      - app-network

  db:
    image: mysql:8.0
    container_name: mysql-db
    restart: always
    env_file:
      - ./fastapi/.env
    environment:
      MYSQL_ROOT_PASSWORD: ${DB_PASS}
      MYSQL_DATABASE: ${DB_NAME}
      MYSQL_USER: ${DB_USER}
      MYSQL_PASSWORD: ${DB_PASS}
    volumes:
      - mysql_data:/var/lib/mysql
    networks:
      - app-network

  reactjs:
    build:
      context: ./reactjs
    container_name: reactjs
    env_file:
      - ./reactjs/.env
    restart: always
    expose:
      - "80"
    networks:
      - app-network

  nginx:
    image: nginx:alpine
    container_name: nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf
      - ./certbot/conf:/etc/letsencrypt
      - ./certbot/www:/var/www/certbot
    depends_on:
      - fastapi
      - reactjs
    restart: always
    networks:
      - app-network

  certbot:
    image: certbot/certbot
    container_name: certbot
    volumes: 
      - ./certbot/conf:/etc/letsencrypt
      - ./certbot/www:/var/www/certbot
    networks:
      - app-network

volumes:
  mysql_data:

networks:
  app-network:
    driver: bridge

```

Update nginx.conf to Enable Certbot ACME Challenge in Nginx

```bash
server {
    listen 80;
    server_name javascriptguru.in api.javascriptguru.in;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}

# Reverse proxy for api.javascriptguru.in
server {
    listen 80;
    server_name api.javascriptguru.in;

    location / {
        proxy_pass http://fastapi:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# for javascriptguru.in
server {
    listen 80;
    server_name javascriptguru.in;

    location / {
        proxy_pass http://reactjs:80/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

```

```bash
cd ch130
sudo docker compose down
sudo docker compose up --build -d
```

Run this manually from terminal to generate the cert (First time only)

```bash
sudo docker compose -f /home/raj/ch130/docker-compose.yml run --rm certbot certonly --webroot -w /var/www/certbot --keep-until-expiring --email user@example.com -d javascriptguru.in -d api.javascriptguru.in --agree-tos
```

Update nginx.conf for HTTPS (Final)

```bash
# Redirect HTTP to HTTPS and serve Certbot challenge
server {
    listen 80;
    server_name javascriptguru.in api.javascriptguru.in;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}

# HTTPS for FastAPI (api.javascriptguru.in)
server {
    listen 443 ssl;
    server_name api.javascriptguru.in;

    ssl_certificate /etc/letsencrypt/live/api.javascriptguru.in/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.javascriptguru.in/privkey.pem;

    location / {
        proxy_pass http://fastapi:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# HTTPS for React frontend (javascriptguru.in)
server {
    listen 443 ssl;
    server_name javascriptguru.in;

    ssl_certificate /etc/letsencrypt/live/javascriptguru.in/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/javascriptguru.in/privkey.pem;

    location / {
        proxy_pass http://reactjs:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

```

```bash
cd ch130
sudo docker compose down
sudo docker compose up --build -d
```

Auto-Renew SSL Certifcate & Reload Nginx

Schedule the Script via Cron

```bash
sudo crontab -e
```

Add this line to run it every month at 3 AM with nginx reload and logs:

```bash
0 3 1 * * (docker compose -f /home/raj/ch130/docker-compose.yml run --rm certbot renew --webroot -w /var/www/certbot --non-interactive >> /home/raj/certbot-renew.log 2>&1 && echo "[✔] Renewal succeeded at $(date)" >> /home/raj/certbot-renew-status.log && docker compose -f /home/raj/ch130/docker-compose.yml exec nginx nginx -s reload >> /home/raj/nginx-reload.log 2>&1 || echo "[✖] Renewal failed at $(date)" >> /home/raj/certbot-renew-status.log)
```

OR Add this line without logs

```bash
0 3 1 * * docker compose -f /home/raj/ch130/docker-compose.yml run --rm certbot renew --webroot -w /var/www/certbot --non-interactive && docker compose -f /home/raj/ch130/docker-compose.yml exec nginx nginx -s reload > /dev/null 2>&1
```

Test renewal dry run

```bash
sudo docker compose -f /home/raj/ch130/docker-compose.yml run --rm certbot renew --dry-run --webroot -w /var/www/certbot --non-interactive
```

---

## 📋 11. View Logs and Debug

Run these commands when something doesn't work or to verify everything is healthy:

🔍 See all logs for all services:

```bash
sudo docker compose logs
```

🔍 Tail logs in real-time:

```bash
sudo docker compose logs -f
```

🔍 View logs for specific container:

```bash
sudo docker compose logs web
sudo docker compose logs nginx
```

💡 Use logs for:

* Checking if FastAPI server started
* Debugging 502 Bad Gateway errors
* Monitoring SSL renewal attempts by Certbot
* Inspecting Python exceptions or import errors

---

## ✅ Deployment Complete

- Visit: `https://javascriptguru.in`
- `www.javascriptguru.in` automatically redirects to the main domain
