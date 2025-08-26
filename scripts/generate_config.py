from jinja2 import Environment, FileSystemLoader
from load_devices import inventory

# Setup Jinja2 environment
env = Environment(loader=FileSystemLoader("templates"))

# Load template
template = env.get_template("config_template.j2")

# Generate config for each device
for device in inventory["devices"]:
    # Add extra variables needed in template
    device["ip_address"] = "192.168.1.10"  # Example, can use real IP from inventory

    config = template.render(device=device)

    # Save generated config to file
    filename = f"{device['name']}_config.txt"
    with open(filename, "w") as f:
        f.write(config)

    print(f"Configuration for {device['name']} saved to {filename}")
