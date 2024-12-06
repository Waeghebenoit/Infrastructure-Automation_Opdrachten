import requests
import argparse
import sys

#Command to run the script
#python shelly.py --name "Outlet1" --cloud off

def configure_shelly(ip, plug_name, cloud_enabled):
    try:
        print("Fetching device info...")
        device_info = requests.get(f"http://{ip}/shelly").json()
        print(f"Device MAC: {device_info['mac']}")

        # Set the plug's name
        print("Configuring device name...")
        requests.post(f"http://{ip}/settings", data={"name": plug_name})

        # Ensure switch is off after restart
        print("Setting relay default state to off...")
        requests.post(f"http://{ip}/settings/relay/0", data={"default_state": "off"})

        # Disable LEDs
        print("Disabling LEDs...")
        requests.post(f"http://{ip}/settings", data={"led_status_disable": "true"})

        # Configure MQTT
        print("Configuring MQTT...")
        mqtt_settings = {
            "mqtt_enable": "true",
            "mqtt_server": "172.23.83.254",
            "mqtt_user": "",  # Fill in if needed
            "mqtt_pass": "",  # Fill in if needed
            "mqtt_id": plug_name,
            "mqtt_retain": "false",
            "mqtt_clean_session": "true"
        }
        requests.post(f"http://{ip}/settings", data=mqtt_settings)

        # Disable unused services
        print("Disabling unused services...")
        requests.post(f"http://{ip}/settings", data={"coiot_enable": "false"})
        if not cloud_enabled:
            requests.post(f"http://{ip}/settings", data={"cloud_enabled": "false"})

        # Set max power limit
        print("Setting max power limit to 2200W...")
        requests.post(f"http://{ip}/settings/relay/0", data={"max_power": "2200"})

        # Configure Wi-Fi
        print("Configuring Wi-Fi...")
        wifi_settings = {
            "wifi_sta.ssid": "Howest-IoT",
            "wifi_sta.pass": "LZe5buMyZUcDpLY"  
        }
        requests.post(f"http://{ip}/settings", data=wifi_settings)

        print(f"Shelly Smart Plug '{plug_name}' configured successfully!")
    except requests.RequestException as e:
        print(f"Error configuring device: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Configure Shelly Smart Plug after factory reset.")
    parser.add_argument("--name", required=True, help="Set the name of the smart plug.")
    parser.add_argument("--cloud", choices=["on", "off"], default="off", help="Enable or disable cloud connection (default: off).")

    args = parser.parse_args()
    plug_name = args.name
    cloud_enabled = args.cloud == "on"

    shelly_ip = "192.168.33.1"  # Default IP
    configure_shelly(shelly_ip, plug_name, cloud_enabled)