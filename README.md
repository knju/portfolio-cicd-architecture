# Self-Hosted CI/CD Infrastructure Architecture

A custom, automated deployment pipeline engineered to host and compile a static portfolio. This architecture bridges a containerized Git forge with a host-level execution environment, enabling zero-downtime automated builds via Git webhooks.

## System Architecture

The pipeline securely routes traffic from the public web through a reverse proxy, into an isolated container network, and safely back out to the host operating system to execute the build scripts.

`Git Push` ➔ `Nginx (Host)` ➔ `Forgejo (Podman)` ➔ `Webhook (10.89.0.1)` ➔ `Python Listener (Host)` ➔ `Hugo Build` ➔ `Live Site`

## Tech Stack
* **OS:** Ubuntu Server (Testing Environment: Arch Linux / KVM)
* **Reverse Proxy:** Nginx
* **Containerization:** Podman
* **Git Forge:** Forgejo (Gitea fork)
* **Automation:** Python 3 (HTTP Server) & Bash
* **Static Site Generator:** Hugo

## Key Engineering Challenges Solved

### 1. Cross-Boundary Container-to-Host Communication
To maintain isolation, the Git forge runs inside a rootless Podman container. Triggering the host-level Hugo compiler required bridging the Podman virtual network (`10.89.0.1`) back to the host operating system. The Python webhook listener was bound to `0.0.0.0` to explicitly accept payloads originating from the containerized interface while blocking public access via UFW firewall rules.

### 2. SSRF (Server-Side Request Forgery) Mitigation
Modern Git forges block outbound webhooks to internal IP addresses by default to prevent network scanning. Rather than disabling this security feature globally with a wildcard (`*`), the `app.ini` security policy was surgically modified. The `ALLOWED_HOST_LIST` was configured to explicitly whitelist only the Podman gateway IP (`10.89.0.1`), preserving SSRF protection for the rest of the server infrastructure.

### 3. Infrastructure as Code (IaC) Portability
The entire environment configuration—including proxy routing, container orchestration, and deployment logic—is version-controlled in this repository. This allows the complete infrastructure to be deployed to a fresh Hetzner VPS in minutes without manual reconfiguration or disk imaging.

## Repository Structure

```text
/
├── etc/nginx/sites-available/
│   └── portfolio.conf       # Nginx reverse proxy routing (Port 80/443 & 3000)
└── opt/
    ├── deploy/
    │   ├── deploy.sh        # Bash execution script (Git pull & Hugo compile)
    │   └── listener.py      # Python HTTP daemon listening for Forgejo webhooks
    └── forgejo/
        └── compose.yaml     # Podman container orchestration and volume mapping
