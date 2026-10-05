#!/bin/bash
# 1. Pull the latest code from your local Forgejo instance
cd /var/www/portfolio
git pull origin main

# 2. Compile the Hugo writeups
echo "[+] Compiling Hugo write-ups..."
cd /var/www/portfolio/writeups-src
hugo --destination /var/www/portfolio/writeups

# 3. Update the server uptime JSON
echo "{\"boot_time\": $(awk '/btime/ {print $2}' /proc/stat)}" >/var/www/portfolio/uptime.json

echo "[+] System live."
