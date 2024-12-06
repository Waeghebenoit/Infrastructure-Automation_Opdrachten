import csv

def generate_cisco_config(input_csv, output_txt):
    try:
        with open(input_csv, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)

            config_lines = []
            
            for row in csv_reader:
                interface = row.get('interface', '').strip()
                description = row.get('description', '').strip()
                vlan = row.get('vlan', '').strip()
                ipaddress = row.get('ipaddress', '').strip()
                subnetmask = row.get('subnetmask', '').strip()
                defaultgateway = row.get('defaultgateway', '').strip()

                if not interface:
                    continue

                # Interface configuration
                config_lines.append(f"interface {interface}")
                
                if description:
                    config_lines.append(f" description {description}")

                if vlan and vlan != '0':
                    config_lines.append(f" encapsulation dot1Q {vlan}")

                if ipaddress.lower() == 'dhcp':
                    config_lines.append(" ip address dhcp")
                elif ipaddress and subnetmask:
                    config_lines.append(f" ip address {ipaddress} {subnetmask}")

                config_lines.append(" no shutdown")
                config_lines.append("!")

                # Default gateway configuration
                if defaultgateway:
                    config_lines.append(f"ip route 0.0.0.0 0.0.0.0 {defaultgateway}")
                    config_lines.append("!")

            # Write to output file
            with open(output_txt, 'w') as txt_file:
                txt_file.write('\n'.join(config_lines))
                print(f"Configuration file generated: {output_txt}")

    except FileNotFoundError:
        print(f"Error: File '{input_csv}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Test the script
if __name__ == "__main__":
    input_csv = "input.csv"
    output_txt = "output.txt" 
    generate_cisco_config(input_csv, output_txt)