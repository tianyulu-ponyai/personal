cd ~/claude-copilot
nohup litellm --config copilot-config.yaml --port 8000 > output.log 2>&1 &
cd -