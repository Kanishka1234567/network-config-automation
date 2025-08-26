from netmiko import ConnectHandler
from dotenv import load_dotenv
from loguru import logger
from pathlib import Path
import os, yaml
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

NET_USERNAME = os.getenv("NET_USERNAME")
NET_PASSWORD = os.getenv("NET_PASSWORD")


def main():
    inv = yaml.safe_load((ROOT / "devices.yaml").read_text(encoding="utf-8"))
    bdir = ROOT / "backups"
    bdir.mkdir(exist_ok=True)

    for dev in inv["devices"]:
        device = {
            "device_type": dev.get("device_type", "cisco_ios"),
            "host": dev["host"],
            "username": NET_USERNAME,
            "password": NET_PASSWORD,
            "port": dev.get("port", 22),
        }
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        fname = bdir / f"{dev['name']}_{dev['host']}_{ts}.cfg"
        try:
            with ConnectHandler(**device) as conn:
                run = conn.send_command("show running-config")
                fname.write_text(run, encoding="utf-8")
                logger.info(f"Backed up {dev['name']} to {fname.name}")
        except Exception as e:
            logger.error(f"Backup failed for {dev['name']} ({dev['host']}): {e}")


if __name__ == "__main__":
    main()
