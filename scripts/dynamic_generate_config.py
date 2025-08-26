# scripts/dynamic_generate_config.py


def create_devices():
    devices = []
    num = int(input("How many devices do you want to configure? "))

    for i in range(1, num + 1):
        print(f"\n--- Device {i} Setup ---")
        name = input(f"Enter name for device {i}: ")

        # IP Configuration
        configure_ip = (
            input("Do you want to configure IP address? (y/n): ").lower() == "y"
        )
        if configure_ip:
            ip = input(f"Enter IP address for {name}: ")
        else:
            ip = None

        # SSH Configuration
        configure_ssh = input("Do you want to configure SSH? (y/n): ").lower() == "y"
        username = password = None
        if configure_ssh:
            custom_creds = (
                input(
                    "Do you want to create a custom username/password? (y/n): "
                ).lower()
                == "y"
            )
            if custom_creds:
                username = input("Enter username: ")
                password = input("Enter password: ")
            else:
                username = "admin"
                password = "admin123"

        devices.append(
            {
                "name": name,
                "ip": ip,
                "ssh": configure_ssh,
                "username": username,
                "password": password,
            }
        )

    return devices


def generate_config(devices):
    for device in devices:
        lines = []
        lines.append(f"hostname {device['name']}")
        lines.append("!")

        if device["ip"]:
            lines.append("interface GigabitEthernet0/0")
            lines.append(" description Connected to LAN")
            lines.append(f" ip address {device['ip']} 255.255.255.0")
            lines.append(" no shutdown")
            lines.append("!")

        if device["ssh"]:
            if device["username"] and device["password"]:
                lines.append(
                    f"username {device['username']} privilege 15 secret {device['password']}"
                )
            lines.append("ip domain-name lab.local")
            lines.append("crypto key generate rsa")
            lines.append("line vty 0 4")
            lines.append(" login local")
            lines.append(" transport input ssh")
            lines.append("!")

        lines.append("end")

        filename = f"{device['name']}_config.txt"
        with open(filename, "w") as f:
            f.write("\n".join(lines))
        print(f"✅ Configuration for {device['name']} saved to {filename}")


if __name__ == "__main__":
    devices = create_devices()
    generate_config(devices)
