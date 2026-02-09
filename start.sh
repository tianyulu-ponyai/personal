#!/bin/zsh

cd ~/claude-copilot
CWD=$(pwd)
source venv/bin/activate
nohup litellm --config $CWD/copilot-config.yaml --port 8000 > $CWD/litellm_copilot.log 2>&1 &
cd -