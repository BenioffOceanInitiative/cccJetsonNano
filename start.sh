#!/bin/bash

# Check if a tmux session named 'tracking' already exists
tmux has-session -t tracking 2>/dev/null

# $? is a special variable that holds the exit status of the last command executed
if [ $? != 0 ]; then
    # Start a new tmux session in the background without attaching to it
    tmux new-session -d -s tracking "python3 track.py --weights exp3_redo.pt --device 0 --source 0"
    echo "Started track.py in a tmux session named 'tracking'"
else
    echo "A tmux session named 'tracking' is already running. Please stop it first."
fi