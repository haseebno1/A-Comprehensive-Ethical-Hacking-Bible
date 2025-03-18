# Kali Linux Environment Setup

This guide will help you set up and optimize your Kali Linux environment for ethical hacking.

## Prerequisites

- A computer capable of running Kali Linux (4GB+ RAM, 20GB+ storage)
- Basic familiarity with Linux commands
- USB drive (8GB+) if installing as a standalone OS

## Installation Options

### Option 1: Full Installation

1. **Download Kali Linux ISO**:
   - Visit the official Kali Linux download page: https://www.kali.org/get-kali/
   - Choose the appropriate image (64-bit recommended)

2. **Create Bootable USB**:
   - On MacOS:
     ```bash
     diskutil list
     diskutil unmountDisk /dev/diskX
     sudo dd if=kali-linux-2025.X-installer-amd64.iso of=/dev/diskX bs=1m
     ```
   - Replace `diskX` with your USB drive identifier

3. **Install Kali Linux**:
   - Boot from the USB drive
   - Follow the installation wizard
   - Choose "Guided - use entire disk" for simplicity
   - Select the desktop environment (Xfce is lightweight, GNOME is feature-rich)

### Option 2: Virtual Machine

1. **Download Kali Linux VM Image**:
   - Visit: https://www.kali.org/get-kali/#kali-virtual-machines
   - Download the image for your virtualization software (VMware, VirtualBox)

2. **Import the VM**:
   - Open your virtualization software
   - Import the downloaded VM image
   - Allocate at least 2GB RAM and 2 CPU cores

### Option 3: WSL (Windows Subsystem for Linux)

For Windows users who want to run Kali alongside Windows:

```powershell
# Enable WSL
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# Install Kali from Microsoft Store or:
wsl --install -d kali-linux
```

## Post-Installation Setup

### 1. Update and Upgrade

First, update your system to ensure you have the latest packages:

```bash
sudo apt update
sudo apt full-upgrade -y
```

### 2. Install Kali Linux Metapackages

Kali organizes tools into metapackages by category:

```bash
# Install all Kali tools (large download, 15GB+)
sudo apt install kali-linux-default -y

# Or install specific categories
sudo apt install kali-tools-information-gathering -y
sudo apt install kali-tools-vulnerability -y
sudo apt install kali-tools-web -y
sudo apt install kali-tools-database -y
sudo apt install kali-tools-passwords -y
sudo apt install kali-tools-wireless -y
sudo apt install kali-tools-reverse-engineering -y
sudo apt install kali-tools-exploitation -y
```

### 3. Configure Your Shell

Enhance your terminal experience:

```bash
# Install ZSH and Oh-My-ZSH
sudo apt install zsh -y
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# Add useful aliases
echo 'alias update="sudo apt update && sudo apt upgrade -y"' >> ~/.zshrc
echo 'alias nmap-quick="nmap -T4 -F"' >> ~/.zshrc
echo 'alias nmap-full="nmap -sS -T4 -A -v"' >> ~/.zshrc
source ~/.zshrc
```

### 4. Set Up Python Environment

Python is essential for many ethical hacking tools:

```bash
# Install pip and virtualenv
sudo apt install python3-pip python3-venv -y

# Create a virtual environment
python3 -m venv ~/ethical_hacking_env
source ~/ethical_hacking_env/bin/activate

# Install essential packages
pip install requests scapy pycryptodome python-nmap paramiko beautifulsoup4
```

### 5. Configure Network Settings

#### Enable Wireless Monitoring Mode

For wireless network testing:

```bash
# Check wireless interface name
iwconfig

# Enable monitor mode
sudo airmon-ng start wlan0  # Replace wlan0 with your interface name
```

#### Configure VPN for Anonymous Testing

```bash
# Install OpenVPN
sudo apt install openvpn -y

# Configure your VPN (example with .ovpn file)
sudo openvpn --config /path/to/your/vpn/config.ovpn
```

## Setting Up Isolated Lab Environments

### 1. Create a Virtual Network

If using VirtualBox:

1. Go to File > Preferences > Network
2. Add a Host-Only Network
3. Configure your vulnerable VMs to use this network

### 2. Set Up Vulnerable VMs for Practice

Download and set up these vulnerable VMs:

1. **Metasploitable**: https://sourceforge.net/projects/metasploitable/
2. **DVWA**: http://www.dvwa.co.uk/
3. **OWASP BWA**: https://sourceforge.net/projects/owaspbwa/

### 3. Docker for Containerized Labs

```bash
# Install Docker
sudo apt install docker.io docker-compose -y
sudo systemctl enable docker --now
sudo usermod -aG docker $USER

# Pull vulnerable application containers
docker pull webgoat/webgoat
docker pull vulnerables/web-dvwa

# Create a Docker network for isolation
docker network create --subnet=172.18.0.0/16 hacknet

# Run containers on the isolated network
docker run --network hacknet --ip 172.18.0.2 -p 8080:8080 -p 9090:9090 webgoat/webgoat
```

## Optimizing Kali Performance

### 1. Reduce Resource Usage

For systems with limited resources:

```bash
# Install a lightweight desktop environment
sudo apt install xfce4 -y

# Disable unnecessary services
sudo systemctl disable bluetooth.service
sudo systemctl disable cups.service
```

### 2. SSD Optimization

If using an SSD:

```bash
# Add TRIM support
sudo systemctl enable fstrim.timer
```

### 3. RAM Optimization

```bash
# Adjust swappiness (lower value = less swap usage)
echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

## Security Hardening

Even though Kali is a security tool, it should be secured:

```bash
# Change default credentials
passwd

# Update SSH configuration
sudo nano /etc/ssh/sshd_config
# Set: PermitRootLogin no
# Set: PasswordAuthentication no
sudo systemctl restart ssh

# Install and configure UFW firewall
sudo apt install ufw -y
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw enable
```

## Verification

To verify your setup is working correctly:

1. Test Nmap:
   ```bash
   nmap -v -A localhost
   ```

2. Test Metasploit:
   ```bash
   msfconsole
   ```

3. Test Python environment:
   ```bash
   python3 -c "import requests, scapy, paramiko; print('All modules imported successfully')"
   ```

## Troubleshooting

### Common Issues

1. **Wireless Adapter Not Working**:
   ```bash
   sudo apt install linux-headers-$(uname -r) -y
   sudo apt install realtek-rtl88xxau-dkms -y  # For common Realtek chipsets
   ```

2. **Display Resolution Issues**:
   - Install guest additions if in VM
   - For VirtualBox: Devices > Insert Guest Additions CD image

3. **Tool Not Found After Installation**:
   ```bash
   which tool_name
   sudo updatedb
   locate tool_name
   ```

### Getting Help

If you encounter issues not covered here:
- Official Kali documentation: https://www.kali.org/docs/
- Kali forums: https://forums.kali.org/
- Kali Linux subreddit: https://www.reddit.com/r/Kali_Linux_Essentials/

## Next Steps

Now that your Kali Linux environment is set up, proceed to the [Kali Linux Beginner Learning Path](../../learning_path/kali/beginner.md) to start your ethical hacking journey.
