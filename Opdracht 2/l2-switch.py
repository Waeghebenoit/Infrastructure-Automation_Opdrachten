import csv
import time
import logging
from netmiko import ConnectHandler

# Enable logging for debugging
logging.basicConfig(filename='netmiko_debug.log', level=logging.DEBUG)

csv_file = "./Opdracht 2/BST-D-1-242.csv"

# Define the device parameters
switch = {
    "device_type": "cisco_ios",  # For Cisco devices
    "host": "192.168.100.100",   # Replace with your switch IP address
    "username": "user",          # Replace with your username
    "password": "123",           # Replace with your login password
    "secret": "123",             # Replace with your enable password (the second Password prompt)
    "timeout": 120               # Increase the timeout duration
}

# Connect to the switch
net_connect = ConnectHandler(**switch)

# Get config and execute commands
with open(csv_file, mode='r') as file:
    csv_reader = csv.DictReader(file,delimiter=';')
    
    for row_num, row in enumerate(csv_reader, start=1):
        # Clean headers and values
        row = {key.strip(): value.strip() for key, value in row.items()}
        commands = ['conf t', 'vtp mode transparent', 'end', 'wr mem']
        net_connect.enable()
        output = net_connect.send_config_set(commands)
        
        ip_address = row.get("IP Address", "")  # Safely get "IP Address"
        
        if not ip_address:  # Check if the value is empty or missing
            commands = [
                        "conf t",
                        f"vlan {row['Vlan']}",
                        f"name {row['Description']}",
                        f"interface range FastEthernet 0/{row['Ports']}",
                        "switchport mode access",
                        f"switchport access vlan {row['Vlan']}",
                        "no shut",
                        "end",
                        "wr mem"
                        ]

        else:
            commands = [
                        f"vlan {row['Vlan']}",
                        f"name {row['Description']}",
                        f"int vlan{row['Vlan']}",
                        f"desc {row['Description']}",
                        f"ip address {row['IP Address']} {row['Netmask']}",
                        "no shut",
                        "end","wr mem"
                        ]
        #net_connect.enable()
        output = net_connect.send_config_set(commands)
        print(output)
        commands = []



# Download config using tftp
commands = ["end","copy running-config tftp",
            "192.168.100.101",
            ""
            ]   

output = net_connect.send_config_set(commands)
print(output)

# Disconnect from the switch
net_connect.disconnect()

