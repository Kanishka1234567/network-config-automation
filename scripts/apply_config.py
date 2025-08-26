from netmiko import ConnectHandler
from load_devices import inventory
import os

for device in inventory["devices"]:
    # Only keep keys Netmiko understands
    netmiko_device = {
        "device_type": device["device_type"],
        "host": device["hostname"],
        "username": device["username"],
        "password": device["password"],
    }

    config_file = f"{device['name']}_config.txt"
    if not os.path.exists(config_file):
        print(f"Config file {config_file} not found. Skipping {device['name']}.")
        continue

    with open(config_file, "r") as f:
        config_lines = f.read().splitlines()

    try:
        connection = ConnectHandler(**netmiko_device)
        print(f"Applying config to {device['name']}...")
        output = connection.send_config_set(config_lines)
        print(output)
        connection.save_config()  # saves configuration to NVRAM
        connection.disconnect()
        print(f"Configuration applied to {device['name']} successfully.\n")
    except Exception as e:
        print(f"Failed to connect or apply config to {device['name']}: {e}")
