#!/usr/bin/bash
source venv/bin/activate  # Activates the WSL venv
export DB_username="yassin"
export HOST="192.168.1.42"
export SPRINGBOOT_PATH="/Users/pc/Desktop/GitHubRepos/GucHub-springboot"
export FINAL_NAME="GucHub.jar"
export REMOTE_PATH="/opt/guchub/backend/"

/mnt/c/users/pc/PycharmProjects/guchub-ops/deploy_backend.py