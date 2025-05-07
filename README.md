 Meme Mayhem - Server Setup

Meme Mayhem
===========

How to Set Up a Server
----------------------

To host a Meme Mayhem server, follow the steps below:

### Port Forwarding

Forward **UDP port 54777** on your router to the internal IP address of the machine running the server. This will allow players to connect to your server from the internet. Here's how:

1.  Log in to your router's web interface. Typically, this can be done by typing `192.168.1.1` or `192.168.0.1` into your browser's address bar. You may need the admin username and password for your router (check your router’s manual or the label on the router itself).
2.  Look for a section called "Port Forwarding," "Virtual Server," or something similar.
3.  Add a new port forwarding rule:
    *   **Protocol:** UDP
    *   **External Port:** 54777
    *   **Internal Port:** 54777
    *   **Internal IP:** The local IP address of the server running Meme Mayhem.
4.  Save the settings and restart the router if necessary.

### How to Get Your Public IP Address

Your public IP address is what others will use to connect to your server. To find it, follow these steps:

1.  Visit a site like [WhatIsMyIPAddress](https://whatismyipaddress.com) or search for "What is my IP" on Google.
2.  Note down your public IP address, which will be displayed at the top of the page.
3.  Share this IP address with others so they can connect to your Meme Mayhem server.

Building From Source
--------------------

1.  Open the `__BUILD_SYS__.py` file.
2.  Set the following line based on your build target:
    
        DEV_MODE = True  # Toggle this for dev vs prod
    

### On Windows

Run:

    Build.bat

### On Linux

Run:

    ./Build.sh