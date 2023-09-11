# Jetson Nano Setup
 Setup proceedure to get the Nano running with YoloV5, Anaconda, and PyTorch
## Required Hardware
 * Jetson Nano BO1 Developer Kit
 * mini SD card (64gb or larger, ultra high speed or video speed class)
 * 5v 4A power supply (barrel jack)
 * micro USB cable
 * Host computer  (Linux is preferable)
 * AC8265 M.2 key E WiFi card (optional)
 * usb keyboard, mouse, and HDMI monitor (for initial setup)
 * USB webcam 
 * Internet connection (for initial setup)

## Initial Setup
1. Download and install [Etcher](https://www.balena.io/etcher/)
2. Download the image from [here](https://ln5.sync.com/dl/f65071870/b5vp32ch-8s23cgn4-b9e4w24q-i2sf9aw2/view/default/13150797710004)
3. Open Balena Etcher and insert the SD card into your computer
4. Select flash from file and select the image you downloaded
5. Select the SD card you inserted
6. Click flash
    [Insert the SD card](https://developer.download.nvidia.com/embedded/images/jetsonOrinNano/getting_started/jetson-orin-nano-dev-kit-sd-slot.jpg) into the Jetson Nano (make sure the power is off)
7. Connect the Jetson Nano to a monitor, keyboard, and mouse
8. Ensure the [J48](https://jetsonhacks.com/2019/04/10/jetson-nano-use-more-power/) jumper is set to the 5v barrel jack power position
9. If you have the AC8265 WiFi card, [install it now](https://www.jetsonhacks.com/2019/04/08/jetson-nano-intel-wifi-and-bluetooth/)
10. or connect the Jetson Nano to the internet via ethernet
11.  Connect the Jetson Nano to the 5v 4A power supply via the barrel jack
12. Follow the on-screen instructions to complete the initial setup
    The default username is jetson and the password is also jetson
# Installing some utilities

we're going to need v4l2-utils for the webcam, and tmux for running the program in the background

```
sudo apt install v4l2-utils
sudo apt install tmux
``` 

## Options for setting up secure ssh
We want to secure the Jetson Nano as much as possible, since this will be running 24/7 and will be exposed to the internet


### 1. **Secure the SSH Server**:
Before exposing the SSH server (Jetson Nano) to the Internet, take the following precautions:

- **Change the default port**: (Not a foolproof measure, but can deter bots that scan default ports.)
    Edit `/etc/ssh/sshd_config` and change `Port 22` to a port of your choice, e.g., `Port 2222`.

- **Use SSH keys for authentication**:
    - On your local computer (client side), generate an SSH key pair:
        ```bash
        ssh-keygen
        ```
    - Copy the public key to the remote computer:
        ```bash
        ssh-copy-id -i ~/.ssh/id_rsa.pub user@remote_host
        ```
    - After copying, edit `/etc/ssh/sshd_config` on the remote computer and disable password authentication:
        ```
        PasswordAuthentication no
        ```

- **Use a firewall**:
    If you are using UFW (Uncomplicated Firewall), allow your custom SSH port:
    ```bash
    sudo ufw allow 2222/tcp
    sudo ufw enable
    ```

- **Limit SSH access to specific IP addresses** (if possible):
    With UFW, you can allow access to the SSH port only from a specific IP:
    ```bash
    sudo ufw allow from your.ip.address.here to any port 2222
    ```

- **Use `fail2ban`**:
    This tool bans IP addresses that have too many failed login attempts:
    ```bash
    sudo apt install fail2ban
    sudo systemctl enable fail2ban
    sudo systemctl start fail2ban
    ```

### 2. **Port Forwarding**:
To access your Linux machine from outside your local network, set up port forwarding on your router to forward your custom SSH port (e.g., 2222) to the Linux machine's internal IP address.

### 3. **Dynamic DNS**:
If your home network doesn't have a static IP, consider using a Dynamic DNS (DDNS) service like DuckDNS, No-IP, or DynDNS. This will provide a hostname that always points to your home's current IP address.

### 4. **Connect**:
Once everything is set up:

```bash
ssh -p 2222 user@remote_host_or_ddns
```

**Important**: Always be cautious when exposing any service to the public internet