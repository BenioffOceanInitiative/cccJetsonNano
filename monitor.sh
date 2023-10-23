#!/bin/bash

# Check if a tmux session named 'tracking' already exists
tmux has-session -t monitor 2>/dev/null

# $? is a special variable that holds the exit status of the last command executed
if [ $? != 0 ]; then
    # Start a new tmux session in the background without attaching to it
    tmux new-session -d -s monitor "python3 GPIO_start.py"
    echo "Started GPIO monitor in a tmux session named 'monitor'"
else
    echo "A tmux session named 'monitor' is already running. Please stop it first."
fi