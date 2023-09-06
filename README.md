# All The Nano Things
after cloning cd into the repo and run the following commands:
```
chmod +x start.sh
chmod +x stop.sh
chmod +x install.sh
```
then run the install script:
```
./install.sh
```
then run the start script:
```
./start.sh
```

to change the weights, conf threshold or anything else edit the start.sh file

the start script allows the program to run in the background, so that you can close your ssh session and have the program continue to run. To stop the program run the stop script:
```
./stop.sh
```
