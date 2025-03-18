#!/usr/bin/env python3
# network_scanner.py - A simple network scanner for ethical hacking practice
# Compatible with both MacOS and Kali Linux

import argparse
import ipaddress
import socket
import subprocess
import sys
import threading
import time
from datetime import datetime

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
    parser = argparse.ArgumentParser(description='Simple Network Scanner for Ethical Hacking')
    parser.add_argument('-t', '--target', dest='target', help='Target IP address or network (CIDR notation)')
    parser.add_argument('-p', '--ports', dest='ports', default='1-1024', help='Port range to scan (default: 1-1024)')
    parser.add_argument('-T', '--timeout', dest='timeout', type=float, default=1.0, help='Timeout in seconds (default: 1.0)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    return parser.parse_args()

def is_valid_ip(ip):
    """Check if the IP address is valid"""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def is_valid_network(network):
    """Check if the network CIDR is valid"""
    try:
        ipaddress.ip_network(network, strict=False)
        return True
    except ValueError:
        return False

def parse_port_range(port_range):
    """Parse port range string (e.g., '1-1024' or '80,443,8080')"""
    ports = []
    if ',' in port_range:
        # Handle comma-separated ports
        for port in port_range.split(','):
            if '-' in port:
                # Handle ranges within comma-separated list
                start, end = map(int, port.split('-'))
                ports.extend(range(start, end + 1))
            else:
                ports.append(int(port))
    elif '-' in port_range:
        # Handle simple range
        start, end = map(int, port_range.split('-'))
        ports = range(start, end + 1)
    else:
        # Handle single port
        ports = [int(port_range)]
    return ports

def scan_port(ip, port, timeout, verbose):
    """Scan a single port on the target IP"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        if result == 0:
            try:
                service = socket.getservbyport(port)
            except:
                service = "unknown"
            print(f"{Colors.GREEN}[+] {ip}:{port} - Open{Colors.ENDC} ({service})")
            return True
        else:
            if verbose:
                print(f"{Colors.FAIL}[-] {ip}:{port} - Closed{Colors.ENDC}")
            return False
        sock.close()
    except socket.error:
        if verbose:
            print(f"{Colors.WARNING}[!] Could not connect to {ip}:{port}{Colors.ENDC}")
        return False

def scan_host(ip, ports, timeout, verbose):
    """Scan all specified ports on a host"""
    open_ports = 0
    print(f"{Colors.BLUE}[*] Scanning host: {ip}{Colors.ENDC}")
    
    # Try to resolve hostname
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        print(f"{Colors.BLUE}[*] Hostname: {hostname}{Colors.ENDC}")
    except socket.herror:
        hostname = "Unknown"
    
    # Use ping to check if host is up
    try:
        # Different ping command syntax for different platforms
        if sys.platform == "darwin":  # MacOS
            ping_cmd = ["ping", "-c", "1", "-W", "1000", ip]
        else:  # Linux/Kali
            ping_cmd = ["ping", "-c", "1", "-w", "1", ip]
            
        ping_result = subprocess.run(ping_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if ping_result.returncode == 0:
            print(f"{Colors.GREEN}[+] Host is up{Colors.ENDC}")
        else:
            print(f"{Colors.WARNING}[!] Host appears to be down, but continuing scan...{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.WARNING}[!] Error pinging host: {e}{Colors.ENDC}")
    
    # Scan ports using threads for faster scanning
    threads = []
    for port in ports:
        t = threading.Thread(target=scan_port, args=(ip, port, timeout, verbose))
        threads.append(t)
        t.start()
        
        # Limit the number of concurrent threads to avoid overwhelming the system
        if len(threads) >= 100:
            for thread in threads:
                thread.join()
            threads = []
    
    # Wait for remaining threads to complete
    for thread in threads:
        thread.join()
    
    print(f"{Colors.BLUE}[*] Scan completed for {ip}{Colors.ENDC}")

def main():
    """Main function"""
    args = get_arguments()
    
    if not args.target:
        print(f"{Colors.FAIL}[!] Error: Target IP or network is required{Colors.ENDC}")
        sys.exit(1)
    
    # Parse port range
    try:
        ports = parse_port_range(args.ports)
    except ValueError:
        print(f"{Colors.FAIL}[!] Error: Invalid port range{Colors.ENDC}")
        sys.exit(1)
    
    # Print banner
    print(f"{Colors.HEADER}{Colors.BOLD}Simple Network Scanner for Ethical Hacking{Colors.ENDC}")
    print(f"{Colors.HEADER}{'=' * 50}{Colors.ENDC}")
    print(f"{Colors.BLUE}[*] Target: {args.target}{Colors.ENDC}")
    print(f"{Colors.BLUE}[*] Ports: {args.ports}{Colors.ENDC}")
    print(f"{Colors.BLUE}[*] Timeout: {args.timeout} seconds{Colors.ENDC}")
    print(f"{Colors.BLUE}[*] Verbose: {args.verbose}{Colors.ENDC}")
    print(f"{Colors.BLUE}[*] Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}")
    print(f"{Colors.HEADER}{'=' * 50}{Colors.ENDC}")
    
    # Check if target is a single IP or a network
    if is_valid_ip(args.target):
        # Scan single IP
        scan_host(args.target, ports, args.timeout, args.verbose)
    elif is_valid_network(args.target):
        # Scan network
        network = ipaddress.ip_network(args.target, strict=False)
        print(f"{Colors.BLUE}[*] Scanning network: {network}{Colors.ENDC}")
        print(f"{Colors.BLUE}[*] Total hosts to scan: {network.num_addresses}{Colors.ENDC}")
        
        for ip in network.hosts():
            scan_host(str(ip), ports, args.timeout, args.verbose)
    else:
        print(f"{Colors.FAIL}[!] Error: Invalid target IP or network{Colors.ENDC}")
        sys.exit(1)
    
    print(f"{Colors.HEADER}{'=' * 50}{Colors.ENDC}")
    print(f"{Colors.BLUE}[*] End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}Scan Complete{Colors.ENDC}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}[!] Scan interrupted by user{Colors.ENDC}")
        sys.exit(0)
