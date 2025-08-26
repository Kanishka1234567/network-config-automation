from netmiko import ConnectHandler
from load_devices import inventory
import os
import csv

# Commands to verify on each device
commands_to_verify = ["show running-config", "show ip interface brief", "show version"]

# Folder to save reports
os.makedirs("reports", exist_ok=True)

for device in inventory["devices"]:
    # Only pass keys Netmiko recognizes
    netmiko_device = {
        "device_type": device["device_type"],
        "host": device["hostname"],
        "username": device["username"],
        "password": device["password"],
    }

    try:
        connection = ConnectHandler(**netmiko_device)
        print(f"\n--- Verifying {device['name']} ---")

        device_report = ""
        for cmd in commands_to_verify:
            output = connection.send_command(cmd)
            device_report += f"\n--- Command: {cmd} ---\n{output}\n"

        # Save report to a text file
        report_file = f"reports/{device['name']}_report.txt"
        with open(report_file, "w") as f:
            f.write(device_report)
        print(f"Report saved to {report_file}")

        # Optional: Save summary to CSV
        with open("reports/summary.csv", "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([device["name"], device["hostname"], "Verified"])

        connection.disconnect()
    except Exception as e:
        print(f"Failed to verify {device['name']}: {e}")
        with open("reports/summary.csv", "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([device["name"], device["hostname"], f"Failed: {e}"])
