# SSL-Tracker

SSL Tracker for internal and external sites.

---

## 🚧 Developer‑Side: Docker Image Build & Push

1. **Login to your private Docker registry**  
   ```bash
   docker login <private_docker_registry>
   ```
   Enter your username and access token when prompted.

2. **Build the Docker image**  
   ```bash
   docker build -t <private_docker_registry>/ssl-tracker:latest .
   ```

3. **Push the image**  
   ```bash
   docker push <private_docker_registry>/ssl-tracker:latest
   ```

---

## 🖥️ Server‑Side Setup

> Prerequisite: Docker and Docker Compose must be installed on the server.

1. **Clone the repo & enter directory**  
   ```bash
   git clone <your_git_repo_url> ssl-tracker
   cd ssl-tracker
   ```

2. **Create your `.env` file**  
   ```bash
   mv example.env .env
   nano .env
   ```
   Populate the following variables in `.env`:
   ```ini
   SMTP_SERVER=your.smtp.server
   SMTP_PORT=587
   SENDER_EMAIL=alerts@yourdomain.com
   SENDER_PASSWORD=your_email_password_or_app_token
   ```

3. **Login to your Docker registry**  
   ```bash
   docker login <private_docker_registry>
   ```

4. **Launch with Docker Compose**  
   ```bash
   docker compose up -d
   ```
   This will pull (if needed) and start the `ssl-tracker` container in detached mode.

---

## ⚙️ Notes

- **Environment Variables**  
  All SMTP credentials and other settings live in the `.env` file—never commit sensitive values to Git.

- **Updating the Image**  
  After making code changes, repeat the **Build & Push** steps on the developer side, then on the server:
  ```bash
  docker compose pull
  docker compose up -d
  ```

- **Logs & Troubleshooting**  
  To view logs:
  ```bash
  docker compose logs -f
  ```
  To restart the container:
  ```bash
  docker compose restart
  ```

