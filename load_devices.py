import yaml
from dotenv import load_dotenv
import os

# Step 1: Load secrets from .env
load_dotenv()

# Step 2: Load device inventory from devices.yaml
with open("devices.yaml", "r") as f:
    inventory = yaml.safe_load(f)

# Step 3: Replace placeholders with actual secrets
for device in inventory["devices"]:
    device["username"] = os.getenv("NET_USERNAME")
    device["password"] = os.getenv("NET_PASSWORD")
    print(
        f"Device {device['name']} - Host: {device['hostname']} - Username: {device['username']}"
    )
