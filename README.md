# All The Nano Things
after cloning cd into the repo and run the following commands:
```
chmod +x start.sh
chmod +x stop.sh
chmod +x monitor.sh
```
install dedpendencies:
```
pip install -r requirements.txt

```
# Start tracking manually:

```
./start.sh
```
To attach to the tmux session and view the tracking output run:
```
tmux attach -t tracking
```
to change the weights, conf threshold or anything else edit the start.sh file

the start script allows the program to run in the background, so that you can close your ssh session and have the program continue to run. To stop the program run the stop script:
```
./stop.sh
```

# Auto start tracking on pump signal:
 make sure that the GPIO pin is correct in the GPIO_start.py file. By default it is set to 17 (Silkscreen pin number 11 next to GND).
```
./monitor.sh
```
You should familiarize yourself with tmux if you are not already. It is a very useful tool for running programs in the background. [Here](https://www.hamvocke.com/blog/a-quick-and-easy-guide-to-tmux/) is a good guide to get you started.

Here are some useful tmux commands:
Once attached, you'll see the terminal just as it was when you (or the script) started the session.

Some useful tmux commands and shortcuts when you're inside a session:

Ctrl-b followed by d: Detach from the session (this returns you to your original terminal session but keeps the tmux session running in the background).

Ctrl-b followed by c: Create a new window within the tmux session.

Ctrl-b followed by n: Move to the next window within the tmux session.

Ctrl-b followed by p: Move to the previous window within the tmux session.

Ctrl-b followed by &: Kill the current window (you'll be prompted to confirm).

If you forget the session name, or to check if the program is running, you can list all running tmux sessions with:

```
tmux list-sessions

```

If using the gui on the jetson nano, you can view the webcam with mpv:
``` 
mpv /dev/video0
```
To exit mpv press q 