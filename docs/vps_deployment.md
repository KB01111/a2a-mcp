# VPS Deployment Guide for A2A MCP Server

## Prerequisites

- VPS with at least 1GB RAM (2GB recommended)
- Ubuntu 20.04 LTS or newer
- SSH access to your VPS
- Domain name (optional but recommended)

## Step 1: Set Up Your VPS

### Update System Packages

```bash
sudo apt update
sudo apt upgrade -y
```

### Install Required Packages

```bash
sudo apt install -y git curl wget
```

### Install Docker

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

Log out and log back in for the group changes to take effect.

## Step 2: Deploy MCP Server

### Clone the Repository

```bash
git clone https://github.com/KB01111/a2a-mcp.git
cd a2a-mcp
```

### Build and Run Docker Container

```bash
docker build -t mcp-server .
docker run -d --name mcp-server \
  --restart unless-stopped \
  -p 8080:8080 \
  mcp-server
```

### Verify Deployment

```bash
docker ps
```

You should see your container running.

Test the API endpoint:

```bash
curl http://localhost:8080/health
```

You should receive a response like: `{"status":"healthy"}`

## Step 3: Set Up SSL/TLS with Nginx (Optional but Recommended)

### Install Nginx and Certbot

```bash
sudo apt install -y nginx certbot python3-certbot-nginx
```

### Configure Nginx as a Reverse Proxy

Create a new Nginx configuration file:

```bash
sudo nano /etc/nginx/sites-available/mcp-server
```

Add the following configuration (replace `your-domain.com` with your actual domain):

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket/SSE support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 86400;
    }
}
```

Enable the configuration:

```bash
sudo ln -s /etc/nginx/sites-available/mcp-server /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Obtain SSL Certificate

```bash
sudo certbot --nginx -d your-domain.com
```

Follow the prompts to complete the certificate setup.

## Step 4: Securing Your Deployment

### Set Up Firewall

```bash
sudo apt install -y ufw
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

### Configure Authentication

Edit the `.env` file in the MCP server directory to enable authentication:

```bash
cd ~/a2a-mcp
echo "MCP_AUTH_ENABLED=true" > .env
echo "MCP_JWT_SECRET=$(openssl rand -hex 32)" >> .env
```

Rebuild and restart the container with the environment file:

```bash
docker build -t mcp-server .
docker stop mcp-server
docker rm mcp-server
docker run -d --name mcp-server \
  --restart unless-stopped \
  -p 8080:8080 \
  --env-file .env \
  mcp-server
```

## Step 5: Monitoring and Maintenance

### Monitor Logs

```bash
docker logs -f mcp-server
```

### Update the Server

To update to the latest version:

```bash
cd ~/a2a-mcp
git pull
docker build -t mcp-server .
docker stop mcp-server
docker rm mcp-server
docker run -d --name mcp-server \
  --restart unless-stopped \
  -p 8080:8080 \
  --env-file .env \
  mcp-server
```

## Troubleshooting

### Check Container Status

```bash
docker ps -a
```

### View Container Logs

```bash
docker logs mcp-server
```

### Restart the Container

```bash
docker restart mcp-server
```

### Check Nginx Status

```bash
sudo systemctl status nginx
```

### Check Firewall Status

```bash
sudo ufw status
```