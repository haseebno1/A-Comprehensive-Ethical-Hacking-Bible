# Kali Linux Ethical Hacking Tools

This directory contains guides and configurations for essential ethical hacking tools on Kali Linux.

## Network Tools

### Nmap

Nmap ("Network Mapper") is a free and open-source utility for network discovery and security auditing.

#### Installation
```bash
# Nmap comes pre-installed in Kali Linux
# To ensure you have the latest version:
sudo apt update
sudo apt install nmap -y
```

#### Basic Usage
```bash
# Basic scan
sudo nmap 192.168.1.1

# Scan a network range
sudo nmap 192.168.1.0/24

# Scan with service detection
sudo nmap -sV 192.168.1.1

# Comprehensive scan
sudo nmap -A 192.168.1.1

# Save results to a file
sudo nmap -A 192.168.1.1 -oN scan_results.txt
```

#### Configuration Tips
- Create aliases for common scan types in your `~/.zshrc` or `~/.bashrc`:
  ```bash
  alias nmap-quick="sudo nmap -T4 -F"
  alias nmap-full="sudo nmap -sS -T4 -A -v"
  ```

### Wireshark

Wireshark is a network protocol analyzer that lets you capture and interactively browse the traffic running on a computer network.

#### Installation
```bash
# Wireshark comes pre-installed in Kali Linux
# To ensure you have the latest version:
sudo apt update
sudo apt install wireshark -y
```

#### Basic Usage
- Launch Wireshark from Applications menu or terminal:
  ```bash
  wireshark
  ```
- Select an interface to capture
- Use display filters to focus on specific traffic:
  ```
  http                # Show only HTTP traffic
  ip.addr == 192.168.1.1  # Show traffic to/from specific IP
  tcp.port == 80      # Show traffic on specific port
  ```

#### Configuration Tips
- Configure Wireshark to capture without root:
  ```bash
  sudo usermod -a -G wireshark $USER
  # Log out and log back in for changes to take effect
  ```
- Increase the capture buffer size in Edit > Preferences > Capture

## Web Application Tools

### Burp Suite

Burp Suite is an integrated platform for performing security testing of web applications.

#### Installation
```bash
# Burp Suite Community Edition comes pre-installed in Kali Linux
# Launch from Applications menu or terminal:
burpsuite
```

#### Basic Usage
- Configure your browser to use Burp as a proxy (typically 127.0.0.1:8080)
- Use the Proxy tab to intercept and modify requests
- Use the Spider tab to crawl websites
- Use the Repeater tab to manually modify and resend requests

#### Configuration Tips
- Install the Burp Suite CA certificate in your browser
- Increase Java memory allocation for better performance:
  ```bash
  echo 'export JAVA_TOOL_OPTIONS="-Xmx2g"' >> ~/.zshrc
  ```

### OWASP ZAP

OWASP Zed Attack Proxy (ZAP) is a free security tool that helps find security vulnerabilities in web applications.

#### Installation
```bash
# ZAP comes pre-installed in Kali Linux
# Launch from Applications menu or terminal:
zaproxy
```

#### Basic Usage
- Use the Quick Start tab to scan a website
- Explore the Alerts tab to see identified vulnerabilities
- Use the Spider tool to discover content
- Use the Active Scan feature to automatically test for vulnerabilities

#### Configuration Tips
- Install the ZAP Root CA certificate in your browser
- Configure automatic authentication for testing behind login pages

## Password Tools

### John the Ripper

John the Ripper is a fast password cracker that supports various hash types.

#### Installation
```bash
# John the Ripper comes pre-installed in Kali Linux
# To ensure you have the latest version:
sudo apt update
sudo apt install john -y
```

#### Basic Usage
```bash
# Crack a password file
john passwords.txt

# Use a wordlist
john --wordlist=/usr/share/wordlists/rockyou.txt passwords.txt

# Show cracked passwords
john --show passwords.txt
```

#### Configuration Tips
- Kali Linux comes with pre-installed wordlists in `/usr/share/wordlists/`
- Uncompress rockyou.txt if needed:
  ```bash
  sudo gunzip /usr/share/wordlists/rockyou.txt.gz
  ```
- Create custom rules in `~/.john/john.conf`

### Hashcat

Hashcat is the world's fastest and most advanced password recovery utility.

#### Installation
```bash
# Hashcat comes pre-installed in Kali Linux
# To ensure you have the latest version:
sudo apt update
sudo apt install hashcat -y
```

#### Basic Usage
```bash
# Basic dictionary attack
hashcat -m 0 -a 0 hash.txt /usr/share/wordlists/rockyou.txt

# With rules
hashcat -m 0 -a 0 hash.txt /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule

# Brute force attack
hashcat -m 0 -a 3 hash.txt ?a?a?a?a?a?a
```

#### Configuration Tips
- For GPU acceleration, ensure you have compatible drivers
- Check GPU status with:
  ```bash
  hashcat -I
  ```
- Create custom rules in a .rule file

## Exploitation Frameworks

### Metasploit Framework

Metasploit Framework is a penetration testing platform that enables you to find, exploit, and validate vulnerabilities.

#### Installation
```bash
# Metasploit comes pre-installed in Kali Linux
# To ensure you have the latest version:
sudo apt update
sudo apt install metasploit-framework -y
```

#### Basic Usage
```bash
# Start Metasploit console
msfconsole

# Search for exploits
search apache

# Use an exploit
use exploit/multi/http/apache_mod_cgi_bash_env_exec

# Set options
set RHOSTS 192.168.1.1
set LHOST 192.168.1.2

# Run the exploit
exploit
```

#### Configuration Tips
- Initialize the database:
  ```bash
  sudo msfdb init
  ```
- Create workspaces for different projects:
  ```bash
  workspace -a project_name
  ```
- Update Metasploit regularly:
  ```bash
  apt update && apt install metasploit-framework -y
  ```

## Wireless Tools

### Aircrack-ng

Aircrack-ng is a network software suite consisting of a detector, packet sniffer, WEP and WPA/WPA2-PSK cracker and analysis tool.

#### Installation
```bash
# Aircrack-ng comes pre-installed in Kali Linux
# To ensure you have the latest version:
sudo apt update
sudo apt install aircrack-ng -y
```

#### Basic Usage
```bash
# List wireless interfaces
iwconfig

# Put interface in monitor mode
sudo airmon-ng start wlan0

# Scan for networks
sudo airodump-ng wlan0mon

# Capture traffic
sudo airodump-ng -c [channel] --bssid [BSSID] -w capture wlan0mon

# Crack WPA handshake
sudo aircrack-ng -w /usr/share/wordlists/rockyou.txt capture-01.cap
```

#### Configuration Tips
- Check for processes that might interfere with monitor mode:
  ```bash
  sudo airmon-ng check kill
  ```
- Some wireless adapters work better than others for monitoring; research compatible adapters

## Forensics Tools

### Autopsy

Autopsy is a digital forensics platform and graphical interface to The Sleuth Kit and other digital forensics tools.

#### Installation
```bash
# Install Autopsy
sudo apt update
sudo apt install autopsy -y
```

#### Basic Usage
- Launch Autopsy from Applications menu or terminal:
  ```bash
  autopsy
  ```
- Create a new case
- Add a disk image or local disk
- Use the various analysis modules

#### Configuration Tips
- Increase memory allocation in `autopsy.conf`
- Install additional modules for specialized analysis

### Foremost

Foremost is a console program to recover files based on their headers, footers, and internal data structures.

#### Installation
```bash
# Foremost comes pre-installed in Kali Linux
# To ensure you have the latest version:
sudo apt update
sudo apt install foremost -y
```

#### Basic Usage
```bash
# Recover files from a disk image
foremost -i disk_image.dd -o output_directory

# Recover specific file types
foremost -t jpg,pdf,doc -i disk_image.dd -o output_directory
```

#### Configuration Tips
- Create custom file signatures in `/etc/foremost.conf`

## Virtualization

### VirtualBox

VirtualBox is a free and open-source hosted hypervisor for x86 virtualization.

#### Installation
```bash
# Install VirtualBox
sudo apt update
sudo apt install virtualbox -y
```

#### Basic Usage
- Launch VirtualBox from Applications menu or terminal:
  ```bash
  virtualbox
  ```
- Create a new VM with the "New" button
- Configure CPU, memory, and disk settings
- Install an operating system from an ISO file

#### Configuration Tips
- Create a host-only network for isolated lab environments:
  1. Go to File > Preferences > Network > Host-only Networks > Create
  2. Configure your VMs to use this network
- Enable nested virtualization for running VMs inside VMs:
  ```bash
  VBoxManage modifyvm "VM Name" --nested-hw-virt on
  ```

### QEMU/KVM

QEMU/KVM is a full virtualization solution for Linux.

#### Installation
```bash
# Install QEMU/KVM
sudo apt update
sudo apt install qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils virt-manager -y
```

#### Basic Usage
- Launch Virtual Machine Manager from Applications menu or terminal:
  ```bash
  virt-manager
  ```
- Create a new VM with the "Create a new virtual machine" button
- Configure CPU, memory, and disk settings
- Install an operating system from an ISO file

#### Configuration Tips
- Create an isolated network for your lab:
  1. In virt-manager, go to Edit > Connection Details > Virtual Networks
  2. Create a new network with no external connectivity
- Add your user to the libvirt group:
  ```bash
  sudo usermod -aG libvirt $USER
  ```

## Social Engineering Tools

### Social Engineering Toolkit (SET)

SET is a framework designed for social engineering attacks.

#### Installation
```bash
# SET comes pre-installed in Kali Linux
# Launch from Applications menu or terminal:
sudo setoolkit
```

#### Basic Usage
- Select from the main menu:
  1. Social-Engineering Attacks
  2. Website Attack Vectors
  3. Credential Harvester Attack Method
  4. Site Cloner
- Enter the target URL and your IP address

#### Configuration Tips
- Update SET regularly:
  ```bash
  cd /usr/share/set
  git pull
  ```
- Create custom templates in the `/usr/share/set/src/templates/` directory

## Python Security Tools

### Python Environment Setup

Setting up a dedicated Python environment for security tools.

#### Installation
```bash
# Python comes pre-installed in Kali Linux
# Create a virtual environment
python3 -m venv ~/ethical_hacking_env
source ~/ethical_hacking_env/bin/activate

# Install essential packages
pip install requests scapy pycryptodome python-nmap paramiko beautifulsoup4
```

#### Essential Python Security Packages
- **Requests**: HTTP library for API interactions
- **Scapy**: Packet manipulation
- **PyCryptodome**: Cryptographic functions
- **Python-Nmap**: Nmap scanning from Python
- **Paramiko**: SSH implementation
- **BeautifulSoup4**: Web scraping and parsing

#### Configuration Tips
- Create requirements.txt for your environment:
  ```bash
  pip freeze > requirements.txt
  ```
- Use virtual environments for different projects

## Additional Resources

- [Kali Linux Tools Listing](https://www.kali.org/tools/)
- [Kali Linux Documentation](https://www.kali.org/docs/)
- [Offensive Security Training](https://www.offensive-security.com/courses-and-certifications/)

## Legal Reminder

Always use these tools legally and responsibly, with proper authorization for any testing activities.
