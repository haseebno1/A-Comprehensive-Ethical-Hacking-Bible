#!/usr/bin/env python3
# mac_changer.py - A script to change MAC address for network interfaces
# Platform-specific for MacOS

import argparse
import re
import subprocess
import sys
import random
import time

# Define colors for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def get_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='MAC Address Changer for MacOS')
    parser.add_argument('-i', '--interface', dest='interface', help='Interface to change MAC address')
    parser.add_argument('-m', '--mac', dest='new_mac', help='New MAC address (random if not specified)')
    parser.add_argument('-r', '--random', action='store_true', help='Generate a random MAC address')
    parser.add_argument('-l', '--list', action='store_true', help='List available interfaces')
    return parser.parse_args()

def list_interfaces():
    """List available network interfaces"""
    print(f"{Colors.HEADER}Available Network Interfaces:{Colors.ENDC}")
    
    try:
        # Get network interfaces using networksetup -listallhardwareports
        result = subprocess.run(["networksetup", "-listallhardwareports"], 
                               capture_output=True, text=True, check=True)
        
        # Parse the output to extract interface names and MAC addresses
        output = result.stdout
        hardware_ports = re.findall(r"Hardware Port: (.*?)\nDevice: (.*?)\nEthernet Address: (.*?)(?:\n|$)", 
                                   output, re.DOTALL)
        
        if hardware_ports:
            for port, device, mac in hardware_ports:
                if mac.strip():  # Only show interfaces with MAC addresses
                    print(f"{Colors.GREEN}Interface: {Colors.BOLD}{device}{Colors.ENDC}")
                    print(f"  Hardware Port: {port}")
                    print(f"  Current MAC: {mac}")
        else:
            print(f"{Colors.WARNING}No interfaces with MAC addresses found.{Colors.ENDC}")
            
    except subprocess.CalledProcessError as e:
        print(f"{Colors.FAIL}Error listing interfaces: {e}{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print(f"{Colors.FAIL}Unexpected error: {e}{Colors.ENDC}")
        sys.exit(1)

def get_current_mac(interface):
    """Get current MAC address of the interface"""
    try:
        # Use ifconfig to get the current MAC address
        ifconfig_result = subprocess.run(["ifconfig", interface], 
                                        capture_output=True, text=True, check=True)
        
        # Extract MAC address using regex
        mac_address_search = re.search(r"ether\s+([0-9a-fA-F:]{17})", ifconfig_result.stdout)
        
        if mac_address_search:
            return mac_address_search.group(1)
        else:
            print(f"{Colors.FAIL}Could not read MAC address for {interface}{Colors.ENDC}")
            return None
            
    except subprocess.CalledProcessError:
        print(f"{Colors.FAIL}Interface {interface} not found{Colors.ENDC}")
        return None

def generate_random_mac():
    """Generate a random MAC address"""
    # First byte must have the second least significant bit set to 0 (locally administered)
    # and the least significant bit set to 0 (unicast)
    first_byte = random.randint(0, 255) & 0xFC | 0x02
    
    # Generate the rest of the MAC address
    mac_parts = [first_byte] + [random.randint(0, 255) for _ in range(5)]
    
    # Format the MAC address
    return ':'.join([f"{part:02x}" for part in mac_parts])

def change_mac(interface, new_mac):
    """Change MAC address of the interface"""
    print(f"{Colors.BLUE}[*] Changing MAC address for {interface} to {new_mac}{Colors.ENDC}")
    
    try:
        # Disable the interface
        print(f"{Colors.BLUE}[*] Disabling {interface}...{Colors.ENDC}")
        subprocess.run(["sudo", "ifconfig", interface, "down"], check=True)
        
        # Change the MAC address
        print(f"{Colors.BLUE}[*] Setting new MAC address...{Colors.ENDC}")
        subprocess.run(["sudo", "ifconfig", interface, "ether", new_mac], check=True)
        
        # Enable the interface
        print(f"{Colors.BLUE}[*] Enabling {interface}...{Colors.ENDC}")
        subprocess.run(["sudo", "ifconfig", interface, "up"], check=True)
        
        # Wait for the interface to come up
        time.sleep(1)
        
        # Verify the change
        current_mac = get_current_mac(interface)
        if current_mac == new_mac:
            print(f"{Colors.GREEN}[+] MAC address was successfully changed to {current_mac}{Colors.ENDC}")
            return True
        else:
            print(f"{Colors.FAIL}[-] Failed to change MAC address{Colors.ENDC}")
            if current_mac:
                print(f"{Colors.FAIL}[-] Current MAC: {current_mac}{Colors.ENDC}")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"{Colors.FAIL}[-] Error changing MAC address: {e}{Colors.ENDC}")
        print(f"{Colors.WARNING}[!] This script requires sudo privileges{Colors.ENDC}")
        return False

def main():
    """Main function"""
    args = get_arguments()
    
    # Print banner
    print(f"{Colors.HEADER}{Colors.BOLD}MAC Address Changer for MacOS{Colors.ENDC}")
    print(f"{Colors.HEADER}{'=' * 50}{Colors.ENDC}")
    
    # List interfaces if requested
    if args.list:
        list_interfaces()
        sys.exit(0)
    
    # Check if interface is specified
    if not args.interface:
        print(f"{Colors.FAIL}[!] Error: Interface is required{Colors.ENDC}")
        print(f"{Colors.WARNING}[!] Use -l or --list to see available interfaces{Colors.ENDC}")
        sys.exit(1)
    
    # Get current MAC address
    current_mac = get_current_mac(args.interface)
    if current_mac:
        print(f"{Colors.BLUE}[*] Current MAC address: {current_mac}{Colors.ENDC}")
    else:
        print(f"{Colors.FAIL}[!] Could not get current MAC address. Exiting.{Colors.ENDC}")
        sys.exit(1)
    
    # Determine new MAC address
    if args.random or not args.new_mac:
        new_mac = generate_random_mac()
        print(f"{Colors.BLUE}[*] Generated random MAC address: {new_mac}{Colors.ENDC}")
    else:
        # Validate the provided MAC address
        if not re.match(r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$", args.new_mac):
            print(f"{Colors.FAIL}[!] Invalid MAC address format. Use format like 00:11:22:33:44:55{Colors.ENDC}")
            sys.exit(1)
        new_mac = args.new_mac
    
    # Change MAC address
    change_mac(args.interface, new_mac)
    
    print(f"{Colors.HEADER}{'=' * 50}{Colors.ENDC}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}[!] Operation interrupted by user{Colors.ENDC}")
        sys.exit(0)
