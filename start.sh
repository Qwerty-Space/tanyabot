#!/bin/bash
# Start tanyabot

tmux new -ds tanyabot "python3 bot.py 2>&1 | tee log.txt"
