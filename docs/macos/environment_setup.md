# MacOS Environment Setup for Ethical Hacking

This guide will help you set up a comprehensive ethical hacking environment on MacOS.

## Prerequisites

- MacOS 10.15 (Catalina) or newer
- Administrator access to your machine
- At least 8GB RAM (16GB+ recommended)
- At least 50GB free disk space

## Basic Setup

### 1. Install Command Line Tools

First, install Xcode Command Line Tools, which provide essential development utilities:

```bash
xcode-select --install
```

This command will prompt you to install the necessary tools. Click "Install" and wait for the process to complete.

### 2. Set Up Package Manager

Homebrew is the most popular package manager for MacOS, making it easy to install and manage software:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

After installation, add Homebrew to your PATH if prompted, then verify the installation:

```bash
brew doctor
```

## Virtualization Setup

### 1. Install Virtualization Software

Choose one of these options:

**Option 1: VirtualBox (Free)**
```bash
brew install --cask virtualbox
```

**Option 2: VMware Fusion (Commercial)**
```bash
brew install --cask vmware-fusion
```

**Option 3: Parallels Desktop (Commercial)**
```bash
brew install --cask parallels
```

### 2. Download Kali Linux VM

1. Download the Kali Linux VM image from the official website:
   - For VirtualBox: https://www.kali.org/get-kali/#kali-virtual-machines
   - For VMware: https://www.kali.org/get-kali/#kali-virtual-machines

2. Import the VM into your virtualization software
3. Configure with at least 2GB RAM and 20GB disk space
4. Start the VM and update it:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

## Essential Tools Installation

### Network Tools

```bash
brew install nmap masscan netcat socat tcpdump wireshark
```

### Web Application Tools

```bash
brew install --cask owasp-zap burp-suite
brew install nikto sqlmap
```

### Password Tools

```bash
brew install john-jumbo hashcat hydra
```

### Exploitation Frameworks

```bash
brew install metasploit
```

### Wireless Tools

```bash
brew install aircrack-ng kismet
```

### Forensics Tools

```bash
brew install foremost binwalk exiftool
```

### Reverse Engineering

```bash
brew install --cask ghidra
brew install radare2
```

## Python Setup

Python is essential for many ethical hacking tools and scripts:

```bash
brew install python
python3 -m pip install --upgrade pip
```

Create a virtual environment for your ethical hacking projects:

```bash
python3 -m venv ~/ethical_hacking_env
source ~/ethical_hacking_env/bin/activate
```

Install essential Python packages:

```bash
pip install requests scapy pycryptodome python-nmap paramiko beautifulsoup4
```

## Terminal Configuration

Customize your terminal for better productivity:

```bash
# Install Oh My Zsh for a better terminal experience
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# Add useful aliases to your .zshrc or .bash_profile
echo 'alias nmap-quick="nmap -T4 -F"' >> ~/.zshrc
echo 'alias nmap-full="nmap -sS -T4 -A -v"' >> ~/.zshrc
source ~/.zshrc
```

## Creating Isolated Testing Environments

It's crucial to practice ethical hacking in isolated environments to avoid accidental damage or legal issues.

### Setting Up Virtual Networks

1. **Create an Isolated Network in Your Virtualization Software**:
   - In VirtualBox: Go to Preferences > Network > Host-only Networks > Create
   - In VMware Fusion: Go to Preferences > Network > Add a custom virtual network
   - In Parallels: Go to Preferences > Network > Add an isolated network

2. **Configure Your VMs to Use the Isolated Network**:
   - Set network adapter to the host-only or isolated network you created
   - Ensure VMs can communicate with each other but not with the internet

### Setting Up Vulnerable VMs for Practice

Download and set up these vulnerable VMs for practice:

1. **OWASP WebGoat**: https://owasp.org/www-project-webgoat/
2. **Metasploitable**: https://sourceforge.net/projects/metasploitable/
3. **DVWA (Damn Vulnerable Web Application)**: http://www.dvwa.co.uk/

## Verification

To verify your setup is working correctly:

1. Test Nmap:
   ```bash
   nmap -v -A localhost
   ```

2. Test Python environment:
   ```bash
   python3 -c "import requests, scapy, paramiko; print('All modules imported successfully')"
   ```

3. Ensure your virtualization software is running correctly by starting a VM

## Next Steps

Now that your environment is set up, proceed to the [MacOS Beginner Learning Path](../../learning_path/macos/beginner.md) to start your ethical hacking journey.

## Troubleshooting

### Common Issues

1. **Homebrew Installation Fails**:
   - Check your internet connection
   - Try running with sudo: `sudo /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`

2. **VirtualBox Fails to Install**:
   - Ensure System Integrity Protection allows the installation
   - Check Security & Privacy settings to allow Oracle extensions

3. **Tools Not Found After Installation**:
   - Ensure your PATH includes Homebrew: `echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile`
   - Restart your terminal or run: `source ~/.zprofile`

### Getting Help

If you encounter issues not covered here, check:
- Homebrew documentation: https://docs.brew.sh
- Tool-specific documentation
- Stack Overflow for specific error messages
