import csv
from netmiko import ConnectHandler
import datetime

TFTP_SERVER_IP = "192.168.100.10"  # Verander dit naar je TFTP-server IP
TFTP_FILENAME = "switch_config_backup"
switch_ip = "192.168.100.100"

# Functie om de CSV-bestanden te lezen
def read_csv(file_path):
    vlan_data = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file, delimiter=';')
        for row in csv_reader:
            vlan_data.append(row)
    return vlan_data

# Functie om de juiste configuratie voor Layer-2 of Layer-3 toe te passen
def configure_vlan(device, vlan_data):
    # Maak verbinding met de switch
    net_connect = ConnectHandler(**device)
    net_connect.enable()  
    net_connect.timeout = 120  

    for vlan in vlan_data:
        vlan_id = vlan['Vlan']
        description = vlan['Description']
        ip_address = vlan['IP Address']
        netmask = vlan['Netmask']
        ports = vlan['Ports']
        
        config = []

        # VLAN (geen IP addressen)
        if not ip_address:
            config.extend([
                f"vlan {vlan_id}",
                f"name {description}",
                "exit"
            ])
            
            # Configureer poorten voor Layer-2 VLAN
            if ports:
                for port in ports.split('-'):
                    config.extend([
                        f"interface range fa0/{port}",
                        "switchport mode access",
                        f"switchport access vlan {vlan_id}",
                        "exit"
                    ])
        
        # Layer-3 VLAN (met IP gegevens)
        elif ip_address and netmask:
            config.extend([
                f"vlan {vlan_id}",
                f"name {description}",
                "exit",
                f"interface vlan {vlan_id}",
                f"ip address {ip_address} {netmask}",
                "no shutdown",
                "exit"
            ])

            # Routing activeren voor Layer-3 switch
            config.append("ip routing")
        
        # Verstuur configuratie naar de switch
        net_connect.send_config_set(config)
        print(config)

        net_connect.send_command("")	
        # Download configuratie via TFTP
        tftp_command = f"copy running-config tftp://{TFTP_SERVER_IP}/{TFTP_FILENAME}_{switch_ip}.cfg"
        tftp_output = net_connect.send_command_timing(tftp_command)
        if "address" in tftp_output.lower():
            tftp_output += net_connect.send_command_timing(TFTP_SERVER_IP)
        if "filename" in tftp_output.lower():
            tftp_output += net_connect.send_command_timing(f"{TFTP_FILENAME}_{switch_ip}.cfg")
        print(tftp_output)

    # Disconnect na configuratie
    net_connect.disconnect()

# Hoofdprogramma
if __name__ == "__main__":
    # SSH connectie-instellingen voor de Cisco switch
    device = {
        'device_type': 'cisco_xe',
        'host': '192.168.100.100',  # Vervang dit met je daadwerkelijke switch IP
        'username': 'user',     # Vervang dit met je daadwerkelijke gebruikersnaam
        'password': '123',     # Vervang dit met je daadwerkelijke wachtwoord
        'secret': '123',       # Vervang dit met je enable wachtwoord indien nodig
    }

    # Lees de CSV
    file_path = 'C:\MCT - IoT Engineer\Infrastructure Automation\Infrastructure-Automation_Opdrachten\Opdracht 2\BST-D-1-242.csv'  # Het pad naar je CSV-bestand
    vlan_data = read_csv(file_path)

    # Configureer de switch met de VLAN gegevens
    configure_vlan(device, vlan_data)

    print("Finished Configuration!")