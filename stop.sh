#!/bin/bash

# Check if a tmux session named 'tracking' exists
tmux has-session -t tracking 2>/dev/null

if [ $? = 0 ]; then
    # Kill the tmux session
    tmux kill-session -t tracking
    echo "Stopped the tmux session named 'tracking' and track.py"
else
    echo "No tmux session named 'tracking' found."
fi
