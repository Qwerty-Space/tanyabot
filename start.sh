#!/bin/bash
# Start tanyabot

tmux new -s tanyabot "python3 bot.py 2>&1 | tee log.txt"
