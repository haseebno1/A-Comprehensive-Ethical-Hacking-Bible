#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
WiFi Analyzer
Author: Abdul Haseeb (@h4x33b)
Version: 1.0.0
Description: A comprehensive WiFi network analyzer that can discover networks,
             capture handshakes, analyze signal strength, and detect potential
             rogue access points. For educational and ethical testing purposes only.
"""

import argparse
import os
import sys
import time
import signal
import subprocess
import re
import json
import csv
from datetime import datetime
from tabulate import tabulate
from threading import Thread
from scapy.all import *

# Suppress Scapy warnings
conf.verb = 0

# ASCII Art Banner
BANNER = """
 __      __.__  ___________.__    _____                .__                         
/  \    /  \__|/   _____/|__|  /  _  \   ____ _____  |  | ___.__.________ _______
\   \/\/   /  |\_____  \ |  | /  /_\  \ /    \\\\__  \ |  |<   |  |\___   // __ \\\\
 \        /|  |/        \|  |/    |    \   |  \/ __ \|  |_\___  | /    /\  ___/
  \__/\  / |__/_______  /|__|\____|__  /___|  (____  /____/ ____||_____ \\\\___  >
       \/             \/             \/     \/     \/     \/          \/    \/ 
                                                                By: Abdul Haseeb (@h4x33b)
"""

# Global variables
networks = {}
clients = {}
hidden_networks = {}
interface = None
monitor_mode = False
channel_hopping = True
capture_handshake = False
target_bssid = None
capture_file = None
handshake_captured = False

def check_root():
    """Check if the script is running as root"""
    if os.geteuid() != 0:
        print("[!] This script must be run as root")
        sys.exit(1)

def check_dependencies():
    """Check if required tools are installed"""
    required_tools = ["airmon-ng", "airodump-ng", "aireplay-ng", "aircrack-ng"]
    missing_tools = []
    
    for tool in required_tools:
        try:
            subprocess.check_output(["which", tool], stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError:
            missing_tools.append(tool)
    
    if missing_tools:
        print("[!] Missing required tools: " + ", ".join(missing_tools))
        print("[!] Please install aircrack-ng suite: sudo apt-get install aircrack-ng")
        sys.exit(1)

def get_interfaces():
    """Get available wireless interfaces"""
    interfaces = []
    try:
        output = subprocess.check_output(["iwconfig"], stderr=subprocess.STDOUT).decode("utf-8")
        pattern = re.compile(r"^([a-zA-Z0-9]+).*IEEE\s+802\.11", re.MULTILINE)
        interfaces = pattern.findall(output)
    except subprocess.CalledProcessError:
        pass
    return interfaces

def enable_monitor_mode(interface):
    """Enable monitor mode on the specified interface"""
    print(f"[*] Enabling monitor mode on {interface}...")
    try:
        # Kill processes that might interfere with monitor mode
        subprocess.run(["airmon-ng", "check", "kill"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Start monitor mode
        output = subprocess.check_output(["airmon-ng", "start", interface]).decode("utf-8")
        
        # Extract the monitor interface name
        monitor_interface = interface
        if "monitor mode enabled on" in output:
            match = re.search(r"monitor mode enabled on (\w+)", output)
            if match:
                monitor_interface = match.group(1)
        elif "monitor mode vif enabled for" in output:
            match = re.search(r"monitor mode vif enabled for \[(\w+)\]", output)
            if match:
                monitor_interface = match.group(1)
        else:
            # Check if interface name changed to interface + mon (common pattern)
            if os.path.exists(f"/sys/class/net/{interface}mon"):
                monitor_interface = f"{interface}mon"
        
        print(f"[+] Monitor mode enabled on {monitor_interface}")
        return monitor_interface, True
    except subprocess.CalledProcessError as e:
        print(f"[!] Failed to enable monitor mode: {e}")
        return interface, False

def disable_monitor_mode(interface):
    """Disable monitor mode on the specified interface"""
    print(f"[*] Disabling monitor mode on {interface}...")
    try:
        subprocess.run(["airmon-ng", "stop", interface], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # Restart network manager
        subprocess.run(["systemctl", "restart", "NetworkManager"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("[+] Monitor mode disabled")
    except subprocess.CalledProcessError as e:
        print(f"[!] Failed to disable monitor mode: {e}")

def channel_hop(interface):
    """Hop between channels to scan all networks"""
    global channel_hopping
    
    while channel_hopping:
        for channel in range(1, 14):
            if not channel_hopping:
                break
            try:
                subprocess.run(["iwconfig", interface, "channel", str(channel)], 
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                time.sleep(0.5)
            except:
                pass

def packet_handler(packet):
    """Handle captured packets"""
    global networks, clients, hidden_networks, handshake_captured, capture_handshake, target_bssid
    
    # Handle Beacon frames - Access Points
    if packet.haslayer(Dot11Beacon):
        bssid = packet[Dot11].addr2
        essid = packet[Dot11Elt].info.decode("utf-8", errors="ignore") if packet[Dot11Elt].info else "Hidden SSID"
        
        try:
            dbm_signal = packet.dBm_AntSignal
        except:
            dbm_signal = -100
            
        stats = packet[Dot11Beacon].network_stats()
        channel = stats.get("channel", 0)
        encryption = stats.get("crypto", "")
        
        if essid == "":
            essid = "Hidden SSID"
            hidden_networks[bssid] = {
                "bssid": bssid,
                "channel": channel,
                "encryption": encryption,
                "signal": dbm_signal,
                "first_seen": datetime.now(),
                "last_seen": datetime.now()
            }
        
        # Update network information
        if bssid not in networks:
            networks[bssid] = {
                "essid": essid,
                "bssid": bssid,
                "channel": channel,
                "encryption": encryption,
                "signal": dbm_signal,
                "beacons": 1,
                "data_packets": 0,
                "first_seen": datetime.now(),
                "last_seen": datetime.now(),
                "clients": []
            }
        else:
            networks[bssid]["essid"] = essid
            networks[bssid]["channel"] = channel
            networks[bssid]["encryption"] = encryption
            networks[bssid]["signal"] = dbm_signal
            networks[bssid]["beacons"] += 1
            networks[bssid]["last_seen"] = datetime.now()
    
    # Handle Probe Responses - Additional AP info
    elif packet.haslayer(Dot11ProbeResp):
        bssid = packet[Dot11].addr2
        essid = packet[Dot11Elt].info.decode("utf-8", errors="ignore") if packet[Dot11Elt].info else "Hidden SSID"
        
        try:
            dbm_signal = packet.dBm_AntSignal
        except:
            dbm_signal = -100
            
        stats = packet[Dot11].network_stats()
        channel = stats.get("channel", 0)
        encryption = stats.get("crypto", "")
        
        # Update network information
        if bssid in networks:
            networks[bssid]["essid"] = essid
            networks[bssid]["channel"] = channel
            networks[bssid]["encryption"] = encryption
            networks[bssid]["signal"] = dbm_signal
            networks[bssid]["last_seen"] = datetime.now()
        
        # Check if this reveals a hidden network
        if bssid in hidden_networks and essid != "Hidden SSID":
            if bssid not in networks:
                networks[bssid] = {
                    "essid": essid,
                    "bssid": bssid,
                    "channel": channel,
                    "encryption": encryption,
                    "signal": dbm_signal,
                    "beacons": 1,
                    "data_packets": 0,
                    "first_seen": hidden_networks[bssid]["first_seen"],
                    "last_seen": datetime.now(),
                    "clients": []
                }
            del hidden_networks[bssid]
    
    # Handle Data frames - Client detection
    elif packet.haslayer(Dot11) and packet.type == 2:  # Data frames
        bssid = None
        client_mac = None
        
        # Extract BSSID and client MAC based on DS Status
        ds = packet.FCfield & 0x3
        if ds == 0:  # Not to/from DS (Ad-hoc)
            bssid = packet[Dot11].addr3
            client_mac = packet[Dot11].addr2
        elif ds == 1:  # To DS
            bssid = packet[Dot11].addr1
            client_mac = packet[Dot11].addr2
        elif ds == 2:  # From DS
            bssid = packet[Dot11].addr2
            client_mac = packet[Dot11].addr1
        
        if bssid and client_mac and bssid in networks:
            # Ignore broadcast/multicast addresses
            if not (client_mac.startswith("01:00:5e") or client_mac.startswith("ff:ff:ff")):
                # Update network data packets count
                networks[bssid]["data_packets"] += 1
                
                # Add client to network if not already there
                if client_mac not in networks[bssid]["clients"]:
                    networks[bssid]["clients"].append(client_mac)
                
                # Update client information
                client_id = f"{bssid}_{client_mac}"
                if client_id not in clients:
                    clients[client_id] = {
                        "bssid": bssid,
                        "client_mac": client_mac,
                        "essid": networks[bssid]["essid"],
                        "first_seen": datetime.now(),
                        "last_seen": datetime.now(),
                        "packets": 1
                    }
                else:
                    clients[client_id]["last_seen"] = datetime.now()
                    clients[client_id]["packets"] += 1
    
    # Handle EAPOL packets for WPA handshake capture
    if capture_handshake and packet.haslayer(EAPOL) and target_bssid:
        bssid = None
        client_mac = None
        
        # Extract BSSID and client MAC
        if packet.addr1 and packet.addr2:
            if packet.addr1 == target_bssid:
                bssid = packet.addr1
                client_mac = packet.addr2
            elif packet.addr2 == target_bssid:
                bssid = packet.addr2
                client_mac = packet.addr1
        
        if bssid == target_bssid:
            print(f"[+] Captured EAPOL packet for {bssid} from client {client_mac}")
            if capture_file:
                wrpcap(capture_file, packet, append=True)
            
            # Check if we have a complete handshake
            if check_handshake(capture_file, target_bssid):
                print(f"[+] WPA handshake captured for {networks[target_bssid]['essid']} ({target_bssid})!")
                handshake_captured = True

def check_handshake(capture_file, bssid):
    """Check if a complete WPA handshake has been captured"""
    if not capture_file or not os.path.exists(capture_file):
        return False
    
    try:
        # Use aircrack-ng to verify the handshake
        cmd = ["aircrack-ng", "-w", "/dev/null", "-b", bssid, capture_file]
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode("utf-8")
        
        return "1 handshake" in output or "Passphrase not in dictionary" in output
    except:
        return False

def deauth_client(interface, bssid, client_mac, count=5):
    """Send deauthentication packets to a client"""
    print(f"[*] Sending {count} deauth packets to {client_mac} from {bssid}")
    try:
        subprocess.run(
            ["aireplay-ng", "--deauth", str(count), "-a", bssid, "-c", client_mac, interface],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception as e:
        print(f"[!] Error sending deauth packets: {e}")

def deauth_network(interface, bssid, count=5):
    """Send deauthentication packets to all clients on a network"""
    print(f"[*] Sending {count} broadcast deauth packets to {bssid}")
    try:
        subprocess.run(
            ["aireplay-ng", "--deauth", str(count), "-a", bssid, interface],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception as e:
        print(f"[!] Error sending deauth packets: {e}")

def detect_rogue_aps():
    """Detect potential rogue access points based on signal strength and SSID similarity"""
    rogue_aps = []
    
    # Group networks by ESSID
    essid_groups = {}
    for bssid, network in networks.items():
        essid = network["essid"]
        if essid not in essid_groups:
            essid_groups[essid] = []
        essid_groups[essid].append(network)
    
    # Check for multiple APs with the same ESSID but different BSSIDs
    for essid, ap_list in essid_groups.items():
        if len(ap_list) > 1 and essid != "Hidden SSID":
            # Sort by signal strength (strongest first)
            ap_list.sort(key=lambda x: x["signal"], reverse=True)
            
            # The strongest signal is likely the legitimate AP
            legitimate_ap = ap_list[0]
            
            # Check other APs with the same ESSID
            for ap in ap_list[1:]:
                # If signal is close to the strongest, it might be legitimate too
                if legitimate_ap["signal"] - ap["signal"] > 15:  # 15 dBm difference
                    rogue_aps.append({
                        "essid": essid,
                        "bssid": ap["bssid"],
                        "channel": ap["channel"],
                        "encryption": ap["encryption"],
                        "signal": ap["signal"],
                        "legitimate_bssid": legitimate_ap["bssid"],
                        "legitimate_signal": legitimate_ap["signal"],
                        "reason": "Signal strength difference"
                    })
    
    # Check for similar ESSIDs (evil twin detection)
    essid_list = list(essid_groups.keys())
    for i, essid1 in enumerate(essid_list):
        if essid1 == "Hidden SSID":
            continue
            
        for essid2 in essid_list[i+1:]:
            if essid2 == "Hidden SSID":
                continue
                
            # Calculate similarity (Levenshtein distance would be better but using simpler approach)
            if essid1.lower() in essid2.lower() or essid2.lower() in essid1.lower():
                # Get the strongest AP for each ESSID
                ap1 = sorted(essid_groups[essid1], key=lambda x: x["signal"], reverse=True)[0]
                ap2 = sorted(essid_groups[essid2], key=lambda x: x["signal"], reverse=True)[0]
                
                # The stronger one is likely legitimate
                if ap1["signal"] > ap2["signal"]:
                    legitimate, rogue = ap1, ap2
                    legitimate_essid, rogue_essid = essid1, essid2
                else:
                    legitimate, rogue = ap2, ap1
                    legitimate_essid, rogue_essid = essid2, essid1
                
                rogue_aps.append({
                    "essid": rogue_essid,
                    "bssid": rogue["bssid"],
                    "channel": rogue["channel"],
                    "encryption": rogue["encryption"],
                    "signal": rogue["signal"],
                    "legitimate_bssid": legitimate["bssid"],
                    "legitimate_essid": legitimate_essid,
                    "legitimate_signal": legitimate["signal"],
                  <response clipped><NOTE>To save on context only part of this file has been shown to you. You should retry this tool after you have searched inside the file with `grep -n` in order to find the line numbers of what you are looking for.</NOTE>