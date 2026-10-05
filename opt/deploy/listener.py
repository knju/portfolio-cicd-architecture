import subprocess
import urllib.request
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

DISCORD_WEBHOOK = "<WEBHOOK>"

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Route 1: CI/CD Deployment from Forgejo
        if self.path == '/deploy':
            print("[*] Webhook received. Initiating deployment...")
            subprocess.Popen(['bash', '/opt/deploy/deploy.sh'])
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Deployment triggered.\n")

        # Route 2: Contact Form from Frontend
        elif self.path == '/api/contact':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                # Forward the exact JSON payload to Discord
                req = urllib.request.Request(
                    DISCORD_WEBHOOK, 
                    data=post_data, 
                    headers={'Content-Type': 'application/json', 'User-Agent': 'Knju-Server'}
                )
                urllib.request.urlopen(req)
                
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Message sent securely.\n")
            except Exception as e:
                print(f"[!] Discord API Error: {e}")
                self.send_response(500)
                self.end_headers()

if __name__ == '__main__':
    print("[+] Knju Backend active on port 8000")
    HTTPServer(('0.0.0.0', 8000), WebhookHandler).serve_forever()
