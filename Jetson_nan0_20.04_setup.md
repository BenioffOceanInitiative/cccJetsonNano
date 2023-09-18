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

# Setting up a Reverse SSH Tunnel

To allow remote access to the Jetson Nano, we will set up a reverse ssh tunnel. This will allow us to connect to the Jetson Nano from anywhere in the world, as long as it has an internet connection.
I set up a minimal vm on aws lightsail to act as the server. You can use any server you want, as long as it has a public IP address and you can ssh into it.
By default the lightsail instance uses keys instead of passwords for ssh. If you are using a server that uses passwords, you will need to change the ssh commands below to include the password.

 On the Nano, install autossh. autossh will automatically restart the ssh connection if it is interrupted.
```
sudo apt install autossh
```
I configured the VM with a static IP address also.
Since Im using keys, I need to copy the Server public key to the Nano so that it can authenticate the connection.
   I named it sail.pem and copied it to the home directory on the Nano
   In order to use the key, I need to change the permissions on it
``` 
chmod 400 sail.pem
```
 Now we can use autossh to set up the reverse tunnel in a tmux session named ssh
``` 
tmux new-session -s -d ssh "autossh -N -R 10022:localhost:22 -i sail.pem <server user>@<server public ip>"
```
   * -f tells autossh to run in the background
   * -N tells autossh not to run any commands on the server
   * -R tells autossh to set up a reverse tunnel
   * 10022 is the port on the server that will be forwarded to port 22 on the Nano
   * localhost is the address on the server that will be forwarded to the Nano
   * 22 is the port on the Nano that will be forwarded to the server
   * -i tells autossh to use the key file
   * sail.pem is the key file
   
 Now that the tunnel is set up, we can ssh into the Nano from the server
```
ssh -p 10022 jetson@localhost
```
   * -p tells ssh to use port 10022
   * jetson is the username on the Nano
   * localhost is the address on the server that is forwarded to the Nano

And thats it! Now you can ssh into the Nano from anywhere in the world, as long as it has an internet connection. The ssh command will need to be run from the server on every session.

To kill the autossh process, run:
```
pkill autossh
