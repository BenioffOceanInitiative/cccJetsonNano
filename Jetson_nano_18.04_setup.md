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
2. Download the [Nvidia Jetpack 4.6](https://developer.nvidia.com/jetpack-sdk-46-archive) image
3. Flash the SD card with the Jetpack 4.6 image using etcher (If the estimated time is more than ~9 minutes, you need a faster SD card. This is a big deal, because the SD card is the bottleneck for the Jetson Nano.  I recommend a 64gb or larger, ultra high speed or video speed class card)
   
4. [Insert the SD card](https://developer.download.nvidia.com/embedded/images/jetsonOrinNano/getting_started/jetson-orin-nano-dev-kit-sd-slot.jpg) into the Jetson Nano (make sure the power is off)
5. Connect the Jetson Nano to a monitor, keyboard, and mouse
6. Ensure the [J48](https://jetsonhacks.com/2019/04/10/jetson-nano-use-more-power/) jumper is set to the 5v barrel jack power position
7. If you have the AC8265 WiFi card, [install it now](https://www.jetsonhacks.com/2019/04/08/jetson-nano-intel-wifi-and-bluetooth/)
8. or connect the Jetson Nano to the internet via ethernet
9.  Connect the Jetson Nano to the 5v 4A power supply via the barrel jack
10. Follow the on-screen instructions to complete the initial setup

## Into Linux Land
You can ssh into the jetson or just use the terminal on the jetson itself.  I prefer to ssh into the jetson from my host computer, since it makes copying commands easier.  To do this, you will need to know the IP address of the jetson.  You can find this by running the following command on the jetson:
```
ifconfig
```
look for the inet address, usually 192.168.x.x.  If you are using a monitor, you can also find the IP address in the network settings.  Once you have the IP address, you can ssh into the jetson from your host computer.  If you are using a linux host, open a terminal window and run the following command:

```
ssh <ip address> -l <username on jetson>
```
you will be prompted for the password for the jetson.

If you are using windows, you will need a program to enable ssh, like [PuTTY](https://www.putty.org/).  Once you have putty installed, open it and enter the IP address of the jetson in the Host Name field.  Make sure the port is set to 22 and the connection type is set to SSH.  Click open and you will be prompted for the username and password for the jetson.

1. If working on the jetson directly, open a terminal window (ctrl+alt+t) 
2. Start by updating the system
```
sudo apt update
sudo apt upgrade
```
3. Install git
```
sudo apt install git
```
4. Optionally, install nano to make editing files easier,
   or you can use vi or vim
    ```
    sudo apt install nano
    ```
## Install Archiconda (conda for ARM)

1. Download the aarch64 installer
   ```
   wget https://github.com/Archiconda/build-tools/releases/download/0.2.3/Archiconda3-0.2.3-Linux-aarch64.sh
   ```
2. Install Archiconda
    ```
    chmod +x Archiconda3-0.2.3-Linux-aarch64.sh
    ./Archiconda3-0.2.3-Linux-aarch64.sh
    ```

3. Follow the terminal instructions to complete the installation
    ```
    Do you accept the license terms? [yes|no]
    [no] >>> yes
    Do you wish the installer to initialize Anaconda3
    by running conda init? [yes|no]
    [no] >>> yes
    ```

4. type the following command to activate conda
    ```
    source ~/.bashrc
    ```
5. Ensure conda is installed
    ```
    conda --version
    ```
## Set up Ultralytics YOLOv5

1. update pip
    ```
    cd ~
    sudo apt update
    sudo apt install -y python3-pip
    pip3 install --upgrade pip
    ```
2. Clone the repo
    ```
    git clone https://github.com/ultralytics/yolov5
    ```
3. Install PyTorch
   ```
    cd ~
    sudo apt-get install -y libopenblas-base libopenmpi-dev
    ```
    ```
    wget https://nvidia.box.com/shared/static/fjtbno0vpo676a25cgvuqc1wty0fkkg6.whl -O torch-1.10.0-cp36-cp36m-linux_aarch64.whl
    ```
    ```
    pip3 install torch-1.10.0-cp36-cp36m-linux_aarch64.whl

   ```
4. Install TorchVision
    ```
    sudo apt install -y libjpeg-dev zlib1g-dev
    ```
    ```
    git clone --branch v0.11.1 https://github.com/pytorch/vision torchvision
    ```
    ```
    cd torchvision

    sudo python3 setup.py install
    ```

5. Modify the requirements.txt file
    ```
    cd yolov5
    sudo nano requirements.txt ## or vi or vim
    ```
6. Comment out the following lines:
    ```
    # torch>=1.7.0
    # torchvision>=0.8.1
    ```
7.  Save and exit the file
8.  Create a conda environment
    ```
    conda create -n yolov5 python=3.9
    ```
9.  Activate the environment
    ```
    conda activate yolov5
    ```
10. Install the following dependency
    ```
    sudo apt install -y libfreetype6-dev
    
    ```

11. Install the requirements
    ```
    pip3 install -r requirements.txt
    ```
12. install onnx
    ```
    pip3 install onnx
    ```
