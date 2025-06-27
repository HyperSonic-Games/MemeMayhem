Meme Mayhem – Server Setup Guide
================================

Hosting a Server
----------------

To host a Meme Mayhem server, follow these steps:

### Port Forwarding (Required)

Forward **UDP port 54777** on your router to the local IP of your server machine:

1.  Open your router settings (usually `192.168.1.1` or `192.168.0.1` in your browser).
2.  Log in with your admin credentials (check your router’s label or manual).
3.  Find **Port Forwarding** or **Virtual Server** settings.
4.  Add a new rule:
    *   **Protocol:** UDP
    *   **External Port:** 54777
    *   **Internal Port:** 54777
    *   **Internal IP:** Your server’s local IP (e.g., `192.168.1.42`)
5.  Save and apply the settings. Restart the router if needed.

### Find Your Public IP

Your public IP is what other players will use to connect:

*   Visit [WhatIsMyIPAddress](https://whatismyipaddress.com) or search “what is my IP” on Google.
*   Share the public IP with players.

Building From Source
--------------------

To build Meme Mayhem from source:

### On Windows

    Build.bat --prod

### On Linux/macOS

    ./Build.sh --prod

_Use `--docs-only` to build only documentation (Needs Natual Docs installed), or `--no-docs` to skip docs._
