# 🚀 Deploying React.js Project to VPS with Nginx

This guide walks you through the steps to deploy a production-ready React.js project on a VPS using Nginx.

---

## ✅ Prerequisites

- VPS (Ubuntu preferred)
- Root or sudo access
- Nginx installed
- Git installed
- Domain (e.g., `javascriptguru.in`) pointed to your VPS IP

---

## 📦 1. Install NVM (Node Version Manager)

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
```

Load NVM immediately without restarting the shell:

```bash
\. "$HOME/.nvm/nvm.sh"
```

---

## 📦 2. Install Node.js via NVM

```bash
nvm install 24
```

> Ensures consistent Node.js versioning for your project.

---

## 🔐 3. Setup SSH Key for GitHub Access

Generate a new SSH deploy key:

```bash
ssh-keygen -f /home/raj/.ssh/reactjs_ed25519 -t ed25519 -C "reactjsrepo"
cat /home/raj/.ssh/reactjs_ed25519.pub
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

```
Host reactjs_project
  HostName github.com
  User github_username
  IdentityFile ~/.ssh/reactjs_ed25519
  IdentitiesOnly yes
```

Test SSH:

```bash
ssh -T git@reactjs_project
```

---

## 📥 4. Clone Project and Install Dependencies

```bash
git clone git@reactjs_project:rajeshrajkr4/reactjs.git
cd ~/reactjs
npm install
```

Create .env File or any file if needed (if any)

---

## 🛠️ 5. Generate Production Build

```bash
npm run build
```

This will generate a `dist` folder

---

## 📁 6. Copy Dist Output to Nginx Root Directory

```bash
sudo mkdir -p /var/www/reactjs
sudo rm -rf /var/www/reactjs/*
sudo cp -r dist/* /var/www/reactjs/
```

---

## 🛡️ 7. Set Proper Permissions

```bash
sudo chown -R www-data:www-data /var/www/reactjs
sudo chmod -R 755 /var/www/reactjs
```

---

## 🌐 8. Configure Nginx Site

```bash
sudo nano /etc/nginx/sites-available/reactjs
```

Paste the following:

```nginx
server {
    listen 80;
    server_name www.javascriptguru.in;
    return 301 $scheme://javascriptguru.in$request_uri;
}

server {
    listen 80;
    server_name javascriptguru.in;

    root /var/www/reactjs;
    index index.html;

    location / {
        try_files $uri /index.html;
    }
}
```

Enable the Nginx site:

```bash
sudo ln -s /etc/nginx/sites-available/reactjs /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## 🔄 9. Make Code Change Live

Make Code change in VS Code then Push to Github

On VPS :

```bash
cd reactjs
git pull
npm run build
sudo rm -rf /var/www/reactjs/*
sudo cp -r dist/* /var/www/reactjs/
sudo systemctl reload nginx
```

---

## 🔒 10. Enable HTTPS (SSL with Certbot)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d javascriptguru.in -d www.javascriptguru.in
```

---

## ✅ Done!

Your React.js project is now live on your VPS via Nginx.

---

## (Optional) Create a shell script to make changes live

Create a file react_deploy.sh and save it

```bash
#!/bin/bash

# Define paths
PROJECT_DIR="/home/raj/reactjs"
BUILD_DIR="$PROJECT_DIR/dist"
DEPLOY_DIR="/var/www/reactjs"

echo "🔄 Pulling latest code from Git..."
cd "$PROJECT_DIR" || exit
git pull

echo "🏗️ Building the ReactJS project..."
npm run build

echo "🧹 Cleaning old files in deployment directory..."
sudo rm -rf "$DEPLOY_DIR"/*

echo "📁 Copying new build to deployment directory..."
sudo cp -r "$BUILD_DIR"/* "$DEPLOY_DIR"/

echo "🔁 Reloading Nginx..."
sudo systemctl reload nginx

echo "✅ Deployment complete!"
```

Make it executable then Run it

```bash
chmod +x ~/react_deploy.sh
./react_deploy.sh
```

Done
