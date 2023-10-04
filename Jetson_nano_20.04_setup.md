# Jetson Nano Setup
 Setup proceedure to get the Nano running Ubuntu 20.04
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

