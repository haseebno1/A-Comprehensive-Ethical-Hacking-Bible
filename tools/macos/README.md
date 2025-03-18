# MacOS Ethical Hacking Tools

This directory contains guides and configurations for essential ethical hacking tools on MacOS.

## Network Tools

### Nmap

Nmap ("Network Mapper") is a free and open-source utility for network discovery and security auditing.

#### Installation
```bash
brew install nmap
```

#### Basic Usage
```bash
# Basic scan
nmap 192.168.1.1

# Scan a network range
nmap 192.168.1.0/24

# Scan with service detection
nmap -sV 192.168.1.1

# Comprehensive scan
nmap -A 192.168.1.1

# Save results to a file
nmap -A 192.168.1.1 -oN scan_results.txt
```

#### Configuration Tips
- Create aliases for common scan types in your `~/.zshrc` or `~/.bash_profile`:
  ```bash
  alias nmap-quick="nmap -T4 -F"
  alias nmap-full="nmap -sS -T4 -A -v"
  ```

### Wireshark

Wireshark is a network protocol analyzer that lets you capture and interactively browse the traffic running on a computer network.

#### Installation
```bash
brew install --cask wireshark
```

#### Basic Usage
- Launch Wireshark from Applications
- Select an interface to capture
- Use display filters to focus on specific traffic:
  ```
  http                # Show only HTTP traffic
  ip.addr == 192.168.1.1  # Show traffic to/from specific IP
  tcp.port == 80      # Show traffic on specific port
  ```

#### Configuration Tips
- Increase the capture buffer size in Preferences > Capture
- Set up profiles for different types of analysis

## Web Application Tools

### Burp Suite

Burp Suite is an integrated platform for performing security testing of web applications.

#### Installation
```bash
brew install --cask burp-suite
```

#### Basic Usage
- Launch Burp Suite from Applications
- Configure your browser to use Burp as a proxy (typically 127.0.0.1:8080)
- Use the Proxy tab to intercept and modify requests
- Use the Scanner tab to automatically identify vulnerabilities

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
brew install --cask owasp-zap
```

#### Basic Usage
- Launch ZAP from Applications
- Use the Quick Start tab to scan a website
- Explore the Alerts tab to see identified vulnerabilities
- Use the Spider tool to discover content

#### Configuration Tips
- Install the ZAP Root CA certificate in your browser
- Configure automatic authentication for testing behind login pages

## Password Tools

### John the Ripper

John the Ripper is a fast password cracker that supports various hash types.

#### Installation
```bash
brew install john-jumbo
```

#### Basic Usage
```bash
# Crack a password file
john passwords.txt

# Use a wordlist
john --wordlist=/path/to/wordlist.txt passwords.txt

# Show cracked passwords
john --show passwords.txt
```

#### Configuration Tips
- Create custom rules in `~/.john/john.conf`
- Download common wordlists:
  ```bash
  curl -L -o wordlist.txt https://github.com/danielmiessler/SecLists/raw/master/Passwords/Common-Credentials/10-million-password-list-top-1000.txt
  ```

### Hashcat

Hashcat is the world's fastest and most advanced password recovery utility.

#### Installation
```bash
brew install hashcat
```

#### Basic Usage
```bash
# Basic dictionary attack
hashcat -m 0 -a 0 hash.txt wordlist.txt

# With rules
hashcat -m 0 -a 0 hash.txt wordlist.txt -r rules/best64.rule

# Brute force attack
hashcat -m 0 -a 3 hash.txt ?a?a?a?a?a?a
```

#### Configuration Tips
- For GPU acceleration, ensure you have compatible drivers
- Create custom rules in a .rule file

## Exploitation Frameworks

### Metasploit Framework

Metasploit Framework is a penetration testing platform that enables you to find, exploit, and validate vulnerabilities.

#### Installation
```bash
brew install metasploit
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
  msfdb init
  ```
- Create workspaces for different projects:
  ```bash
  workspace -a project_name
  ```

## Wireless Tools

### Aircrack-ng

Aircrack-ng is a network software suite consisting of a detector, packet sniffer, WEP and WPA/WPA2-PSK cracker and analysis tool.

#### Installation
```bash
brew install aircrack-ng
```

#### Basic Usage
```bash
# Put interface in monitor mode
sudo airport -z
sudo airport -c[channel] --monitor

# Capture traffic
sudo airodump-ng -c [channel] --bssid [BSSID] -w capture [interface]

# Crack WPA handshake
sudo aircrack-ng -w wordlist.txt capture-01.cap
```

#### Configuration Tips
- MacOS may require additional configuration for wireless monitoring
- External USB wireless adapters often work better for monitoring

## Forensics Tools

### Autopsy

Autopsy is a digital forensics platform and graphical interface to The Sleuth Kit and other digital forensics tools.

#### Installation
```bash
brew install --cask autopsy
```

#### Basic Usage
- Launch Autopsy from Applications
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
brew install foremost
```

#### Basic Usage
```bash
# Recover files from a disk image
foremost -i disk_image.dd -o output_directory

# Recover specific file types
foremost -t jpg,pdf,doc -i disk_image.dd -o output_directory
```

#### Configuration Tips
- Create custom file signatures in `foremost.conf`

## Virtualization

### VirtualBox

VirtualBox is a free and open-source hosted hypervisor for x86 virtualization.

#### Installation
```bash
brew install --cask virtualbox
```

#### Basic Usage
- Launch VirtualBox from Applications
- Create a new VM with the "New" button
- Configure CPU, memory, and disk settings
- Install an operating system from an ISO file

#### Configuration Tips
- Create a host-only network for isolated lab environments:
  1. Go to Preferences > Network > Host-only Networks > Create
  2. Configure your VMs to use this network
- Enable nested virtualization for running VMs inside VMs:
  ```bash
  VBoxManage modifyvm "VM Name" --nested-hw-virt on
  ```

### VMware Fusion

VMware Fusion is a commercial virtualization software for MacOS.

#### Installation
```bash
brew install --cask vmware-fusion
```

#### Basic Usage
- Launch VMware Fusion from Applications
- Create a new VM with the "+" button
- Configure CPU, memory, and disk settings
- Install an operating system from an ISO file

#### Configuration Tips
- Create a custom network for isolated lab environments:
  1. Go to Preferences > Network > Add a custom virtual network
  2. Configure your VMs to use this network
- Enable nested virtualization:
  1. Shut down the VM
  2. Edit the VMX file to add: `vhv.enable = "TRUE"`

## Python Security Tools

### Python Environment Setup

Setting up a dedicated Python environment for security tools.

#### Installation
```bash
# Install Python
brew install python

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

- [MacOS Security Tools List](https://github.com/ashishb/osx-and-ios-security-awesome)
- [Homebrew Security Tools](https://formulae.brew.sh/formula/)
- [Objective-See Tools](https://objective-see.org/tools.html)

## Legal Reminder

Always use these tools legally and responsibly, with proper authorization for any testing activities.
