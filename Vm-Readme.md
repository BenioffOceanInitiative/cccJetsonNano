# Setting up the VM for remote access to the Jetson Nano

I chose an Ubuntu instance, due to it's popularity and ease of use, but this should work on any Linux server.

We are going to create a machine that is capable of maintaing an SSH connection, powerful enough to act as a bridge for a VNC server on the nano, and the video stream from the Nano to the client.

First we navigate to the Google cloud console and create a new VM instance. I chose the default e2 instance with 2 vCPUs and 4GB of memory. 
![image](readme_images/1.png)


I selected Ubuntu 20.04 LTS image with 10gb storage.

![image](readme_images/2.png)

Once the instance is created, we need to assign a static ip address

Navigate to VPC network > External IP addresses
And select reserve static address

Assign the static ip to the instance we just created

![image](readme_images/3.png)

SSH should be allowed by default on the machine, so no new firewall rules are needed.

Now, in order to be able to connect the nano to the VM over ssh, we need a keypair. On the Nano, or wherever you will be connecting from, run:

```
ssh-keygen -t rsa -f ~/.ssh/<keyname> -C <new username> -b 2048
```

This will create a new keypair in the ~/.ssh directory. The public key will be named <keyname>.pub and the private key will be named <keyname>

Set proper permissions on the private key:

```
chmod 400 ~/.ssh/<keyname>
```

we need to copy the pulic key to the VM. 
On your local machine, run:

```
cat ~/.ssh/<keyname>.pub
```
copy the output of this command to your clipboard.

In the cloud console, navigate to Compute Engine > VM Instances and click on the instance we just created.
Click edit at the top, and scroll down to SSH keys. Click add item and paste the public key into the box. Click save at the bottom.

![image](readme_images/4.png)

Sometimes, it is necessary to restart the VM for the changes to take effect.

Now we can ssh into the VM from our local machine:

```
ssh -i ~/.ssh/<keyname> <username>@<public ip>
```

Refer to the [Jetson Nano Setup](Jetson_nanO_20.04_setup.md) for instructions on how to set up the Nano to connect to the VM.



# Setting up a Reverse SSH Tunnel

To allow remote access to the Jetson Nano, we will set up a reverse ssh tunnel. This will allow us to connect to the Jetson Nano from anywhere in the world through our VM.


 On the Nano, install autossh. autossh will automatically restart the ssh connection if it is interrupted.
```
sudo apt install autossh
```

 Now we can use autossh to set up the reverse tunnel in a tmux session named ssh
``` 
tmux new-session -s -d ssh "autossh -N -R 10022:localhost:22 -i sail.pem <server user>@<server public ip>"
```
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
``````
# Create a Service that runs the tunnel on startup with Systemd

1. **Write The Bash Script**


```bash
touch /autossh.sh
```

In the file add the following content:

```bash

#!/bin/bash

# Check if a tmux session named 'ssh' already exists
tmux has-session -t ssh 2>/dev/null

# $? is a special variable that holds the exit status of the last command executed
if [ $? != 0 ]; then
    # Start a new tmux session in the background without attaching to it
    tmux new-session -d -s ssh "autossh -N -R 10022:localhost:22 -i <keyfile> <server user>@<server public ip>"
    
else
    echo "A tmux session named 'ssh' is already running"
fi
```

Save and close the file.

2. **Make the script executable**

```bash
chmod +x /autossh.sh
```


**Using systemd**

Create a new service file under `/etc/systemd/system/`, let's name it `autossh.service`:

```bash
sudo nano /etc/systemd/system/autossh.service
```

b. Add the following content:

```ini
[Unit]
Description= Reverse autossh tunnel

[Service]
ExecStart=/home/jetson/autossh.sh
User=jetson
Group=jetson

[Install]
WantedBy=multi-user.target
```

c. Save and close the file.

d. Enable the service to run at startup:

```bash
sudo systemctl enable myscript.service
```

e. To test the service without rebooting, you can start it manually:

```bash
sudo systemctl start myscript.service
```

Now, the ssh tunnel will run on every system startup.


# Setting up Mosquitto MQTT Broker
Next, we're going to install mosquitto on the VM. Mosquitto is an MQTT broker that will allow us to send messages between the Nano and the client. This is for any sensor data we want to send to the client, and in the future, possibly ,for sending commands from the client to the Nano.

ssh into the VM and run:

```
sudo apt-add-repository ppa:mosquitto-dev/mosquitto-ppa
sudo apt-get update
sudo apt-get install mosquitto
sudo apt-get install mosquitto-clients
```
Mosquitto should now be installed. We need to create a config file to allow outside connections and to set password authentication. 

```
cd /etc/mosquitto/conf.d
sudo nano mosquitto.conf
```

Paste the following into the file:

```
allow_anonymous false
password_file /etc/mosquitto/passwd
listener 1883
listener 8080
protocol websockets
```
```

Save and exit the file.

Next, we need to create a password file. Run:

```
```
sudo nano /etc/mosquitto/passwd.txt
```

Add a username and password to the file in this format, one per line. You can add multiple users and passwords, and multiple clients can use the same credentials. This will be used to authenticate the connection between the Nano and the VM. It will need to be included in any client that connects to the broker.



```
username:password
```

Save and exit the file.

Now we need to encrypt the password file. Run:

```
mosquitto_passwd -U passwd.txt
```
if you open the file again, you will see that the password is now encrypted.

Mosquitto is already configured as a systemd service, so to start it simply run

```
sudo service mosquitto start
```

To check the status of the service, run

```
sudo service mosquitto status
```
to stop the service, run

```
sudo service mosquitto stop
```

Once started, it will run on startup and run in the background.