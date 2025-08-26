from netmiko import ConnectHandler
from load_devices import inventory

for device in inventory["devices"]:
    # Create a dict only with keys Netmiko needs
    netmiko_device = {
        "device_type": device["device_type"],
        "host": device["hostname"],  # Netmiko expects 'host'
        "username": device["username"],
        "password": device["password"],
    }

    try:
        connection = ConnectHandler(**netmiko_device)
        output = connection.send_command("show ip int brief")
        print(f"--- {device['name']} ---")
        print(output)
        connection.disconnect()
    except Exception as e:
        print(f"Failed to connect to {device['name']}: {e}")
