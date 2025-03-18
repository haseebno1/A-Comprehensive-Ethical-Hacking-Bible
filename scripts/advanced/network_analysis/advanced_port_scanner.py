#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Advanced Port Scanner
Author: Abdul Haseeb (@h4x33b)
Version: 1.0.0
Description: A sophisticated port scanner with OS fingerprinting capabilities
             and service detection. This tool combines the power of Nmap-like
             scanning with additional features for comprehensive network reconnaissance.
"""

import argparse
import socket
import sys
import threading
import time
import ipaddress
import random
import os
import json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# ASCII Art Banner
BANNER = """
    _    ____  __     __    _   _  ____  _____  ____    ____   ____    _    _   _ _   _ _____ ____  
   / \\  |  _ \\ \\ \\   / /   / \\ | |/ ___|| ____||  _ \\  |  _ \\ / ___|  / \\  | \\ | | \\ | | ____|  _ \\ 
  / _ \\ | | | | \\ \\ / /   / _ \\| | |    |  _|  | | | | | |_) | |     / _ \\ |  \\| |  \\| |  _| | |_) |
 / ___ \\| |_| |  \\ V /   / ___ \\ | |___ | |___ | |_| | |  __/| |___ / ___ \\| |\\  | |\\  | |___|  _ < 
/_/   \\_\\____/    \\_/   /_/   \\_\\_\\____||_____|____/  |_|    \\____/_/   \\_\\_| \\_|_| \\_|_____|_| \\_\\
                                                                                                    
                                                                By: Abdul Haseeb (@h4x33b)
"""

# Common ports to scan by default
COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080]

# Service signatures for basic service detection
SERVICE_SIGNATURES = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    111: "RPC",
    135: "MSRPC",
    139: "NetBIOS",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    993: "IMAPS",
    995: "POP3S",
    1723: "PPTP",
    3306: "MySQL",
    3389: "RDP",
    5900: "VNC",
    8080: "HTTP-Proxy"
}

# OS detection signatures (simplified)
OS_SIGNATURES = {
    "TTL=64": "Linux/Unix",
    "TTL=128": "Windows",
    "TTL=254": "Cisco/Network Device",
    "TTL=255": "Unix/FreeBSD"
}

class PortScanner:
    def __init__(self, target, ports=None, timeout=1, threads=100, verbose=False, output=None):
        self.target = target
        self.ports = ports if ports else COMMON_PORTS
        self.timeout = timeout
        self.threads = threads
        self.verbose = verbose
        self.output = output
        self.open_ports = []
        self.start_time = None
        self.end_time = None
        self.os_info = "Unknown"
        self.scan_results = {}
        
    def resolve_host(self):
        """Resolve hostname to IP address"""
        try:
            return socket.gethostbyname(self.target)
        except socket.gaierror:
            print(f"[!] Error: Could not resolve hostname {self.target}")
            sys.exit(1)
            
    def is_valid_ip(self, ip):
        """Check if the IP address is valid"""
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False
            
    def scan_port(self, ip, port):
        """Scan a single port"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(self.timeout)
            result = s.connect_ex((ip, port))
            if result == 0:
                service = self.detect_service(ip, port)
                self.open_ports.append((port, service))
                if self.verbose:
                    print(f"[+] Port {port}/tcp open - {service}")
            s.close()
        except Exception as e:
            if self.verbose:
                print(f"[!] Error scanning port {port}: {e}")
                
    def detect_service(self, ip, port):
        """Basic service detection"""
        if port in SERVICE_SIGNATURES:
            service_name = SERVICE_SIGNATURES[port]
            # Try to get banner for more accurate detection
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(self.timeout)
                s.connect((ip, port))
                s.send(b'HELLO\r\n')
                banner = s.recv(1024).decode('utf-8', 'ignore').strip()
                s.close()
                if banner:
                    return f"{service_name} ({banner})"
                return service_name
            except:
                return service_name
        return "Unknown"
        
    def detect_os(self, ip):
        """Simple OS detection using ping TTL values"""
        if not self.is_valid_ip(ip):
            return "Unknown"
            
        try:
            # Use different approach based on platform
            if os.name == 'nt':  # Windows
                ping_cmd = f"ping -n 1 {ip}"
                response = os.popen(ping_cmd).read()
            else:  # Unix/Linux
                ping_cmd = f"ping -c 1 {ip}"
                response = os.popen(ping_cmd).read()
                
            for signature, os_name in OS_SIGNATURES.items():
                if signature in response:
                    return os_name
            return "Unknown"
        except:
            return "Unknown"
            
    def run_scan(self):
        """Run the port scan"""
        ip = self.resolve_host()
        
        print(f"\n[*] Starting scan on {self.target} ({ip})")
        print(f"[*] Scanning {len(self.ports)} ports")
        
        self.start_time = time.time()
        
        # Detect OS
        print("[*] Attempting OS detection...")
        self.os_info = self.detect_os(ip)
        print(f"[+] OS Detection: {self.os_info}")
        
        # Scan ports using thread pool
        print("[*] Starting port scan...")
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            for port in self.ports:
                executor.submit(self.scan_port, ip, port)
                
        self.end_time = time.time()
        scan_duration = self.end_time - self.start_time
        
        # Sort open ports
        self.open_ports.sort(key=lambda x: x[0])
        
        # Prepare results
        self.scan_results = {
            "target": self.target,
            "ip": ip,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "scan_duration": f"{scan_duration:.2f} seconds",
            "os_detection": self.os_info,
            "open_ports": [{"port": port, "service": service} for port, service in self.open_ports]
        }
        
        # Display results
        self.display_results()
        
        # Save results if output is specified
        if self.output:
            self.save_results()
            
    def display_results(self):
        """Display scan results"""
        print("\n" + "="*60)
        print(f"Scan Results for {self.target} ({self.scan_results['ip']})")
        print("="*60)
        print(f"Scan completed in: {self.scan_results['scan_duration']}")
        print(f"OS Detection: {self.scan_results['os_detection']}")
        print(f"Open Ports: {len(self.open_ports)}")
        print("-"*60)
        
        if self.open_ports:
            print("PORT\tSTATE\tSERVICE")
            for port, service in self.open_ports:
                print(f"{port}/tcp\topen\t{service}")
        else:
            print("No open ports found.")
            
        print("="*60)
        
    def save_results(self):
        """Save results to file"""
        try:
            with open(self.output, 'w') as f:
                json.dump(self.scan_results, f, indent=4)
            print(f"[+] Results saved to {self.output}")
        except Exception as e:
            print(f"[!] Error saving results: {e}")

def parse_port_range(port_range):
    """Parse port range string (e.g., '1-1000' or '80,443,8080')"""
    ports = []
    if '-' in port_range:
        start, end = port_range.split('-')
        ports = list(range(int(start), int(end) + 1))
    else:
        ports = [int(port) for port in port_range.split(',')]
    return ports

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Advanced Port Scanner with OS Detection")
    parser.add_argument("target", help="Target IP address or hostname")
    parser.add_argument("-p", "--ports", help="Ports to scan (e.g., '1-1000' or '80,443,8080')")
    parser.add_argument("-t", "--timeout", type=float, default=1, help="Timeout in seconds (default: 1)")
    parser.add_argument("-T", "--threads", type=int, default=100, help="Number of threads (default: 100)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("-o", "--output", help="Output file (JSON format)")
    parser.add_argument("-A", "--all", action="store_true", help="Scan all 65535 ports")
    
    args = parser.parse_args()
    
    print(BANNER)
    
    # Determine ports to scan
    if args.all:
        ports = list(range(1, 65536))
    elif args.ports:
        ports = parse_port_range(args.ports)
    else:
        ports = COMMON_PORTS
        
    # Create scanner and run scan
    scanner = PortScanner(
        target=args.target,
        ports=ports,
        timeout=args.timeout,
        threads=args.threads,
        verbose=args.verbose,
        output=args.output
    )
    
    scanner.run_scan()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user. Exiting...")
        sys.exit(0)
