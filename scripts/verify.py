from netmiko import ConnectHandler
from dotenv import load_dotenv
from loguru import logger
from pathlib import Path
import os, yaml, re

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")
NET_USERNAME = os.getenv("NET_USERNAME")
NET_PASSWORD = os.getenv("NET_PASSWORD")


def main():
    inv = yaml.safe_load((ROOT / "devices.yaml").read_text(encoding="utf-8"))
    for dev in inv["devices"]:
        device = {
            "device_type": dev.get("device_type", "cisco_ios"),
            "host": dev["host"],
            "username": NET_USERNAME,
            "password": NET_PASSWORD,
            "port": dev.get("port", 22),
        }
        try:
            with ConnectHandler(**device) as conn:
                out1 = conn.send_command("show vlan brief")
                out2 = conn.send_command("show access-lists")
                ok_vlan_10 = bool(re.search(r"10\s+HR", out1))
                ok_acl = "BLOCK_GUEST" in out2 or "DENY_BAD" in out2
                status = "OK" if (ok_vlan_10 and ok_acl) else "CHECK"
                logger.info(f"{dev['name']} verify: {status}")
        except Exception as e:
            logger.error(f"Verify failed for {dev['name']} ({dev['host']}): {e}")


if __name__ == "__main__":
    main()
