#!/usr/bin/env sh

tmux send-keys "nix develop" C-m
tmux send-keys "nvim main.py" C-m
tmux split-window -h
tmux send-keys "nix develop" C-m


