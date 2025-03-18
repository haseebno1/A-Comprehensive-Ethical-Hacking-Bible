# Beginner Learning Path - Kali Linux

This guide provides a structured learning path for ethical hacking using Kali Linux, taking you from the fundamentals to practical skills.

## Stage 1: Understanding the Basics (2-4 weeks)

### Ethical Hacking Concepts

#### Learning Objectives
- Understand what ethical hacking is and its importance
- Learn the legal and ethical boundaries of security testing
- Differentiate between types of hackers and their motivations
- Familiarize yourself with penetration testing methodologies

#### Resources
- **Reading**: [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- **Video Course**: [Kali Linux for Ethical Hackers](https://www.youtube.com/playlist?list=PLYmlEoSHldN7HJapyiQ8kFLUsk_a7EjCw)
- **Practice**: Create a document outlining the ethical considerations for a hypothetical penetration test

### Networking Fundamentals

#### Learning Objectives
- Understand the TCP/IP model and common protocols
- Learn IP addressing, subnetting, and routing basics
- Master network troubleshooting tools in Kali Linux
- Identify different network devices and their functions

#### Resources
- **Reading**: "TCP/IP Illustrated, Volume 1" by W. Richard Stevens
- **Kali Linux Tools**: 
  ```bash
  # Basic network commands
  ifconfig
  ip addr
  route -n
  ping -c 4 google.com
  traceroute google.com
  
  # Network utilities
  sudo apt install nmap wireshark tcpdump
  ```
- **Practice**: Map your local network using Zenmap (GUI for Nmap)

### Kali Linux Command Line Basics

#### Learning Objectives
- Master essential Bash commands
- Understand file system navigation and permissions
- Learn process management and system monitoring
- Configure terminal for productivity

#### Resources
- **Reading**: "Linux Basics for Hackers" by OccupyTheWeb
- **Kali Linux Commands**:
  ```bash
  # Navigation
  pwd                 # Print working directory
  ls -la              # List all files with details
  cd /path/to/dir     # Change directory
  
  # File operations
  touch file.txt      # Create empty file
  mkdir directory     # Create directory
  cp source target    # Copy files
  mv source target    # Move/rename files
  
  # System information
  top                 # Process viewer
  ps aux              # Process status
  df -h               # Disk usage
  
  # Permissions
  chmod 755 file      # Change file permissions
  chown user:group file # Change file ownership
  ```
- **Practice**: Create a shell script that automates a system reconnaissance task

### Programming Fundamentals

#### Learning Objectives
- Learn basic Python syntax and data structures
- Understand control flow (if/else, loops, functions)
- Master file operations and error handling
- Create simple automation scripts

#### Resources
- **Reading**: "Black Hat Python" by Justin Seitz
- **Kali Linux Setup**:
  ```bash
  # Python is pre-installed on Kali
  # Create a virtual environment
  python3 -m venv ~/ethical_hacking_env
  source ~/ethical_hacking_env/bin/activate
  
  # Install useful packages
  pip install requests scapy pycryptodome
  ```
- **Practice**: Write a Python script that scans your local network for active hosts

## Stage 2: Setting Up Your Environment (1-2 weeks)

### Kali Linux Customization

#### Learning Objectives
- Optimize Kali Linux for ethical hacking
- Configure desktop environment and tools
- Set up persistence for live environments
- Secure your Kali installation

#### Resources
- **Reading**: [Kali Linux Environment Setup Guide](../../docs/kali/environment_setup.md)
- **Essential Configurations**:
  ```bash
  # Update and upgrade
  sudo apt update && sudo apt full-upgrade -y
  
  # Install additional tool categories
  sudo apt install kali-tools-information-gathering kali-tools-vulnerability kali-tools-web -y
  
  # Configure terminal
  sudo apt install zsh -y
  sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
  ```
- **Practice**: Create a custom Kali configuration script that sets up your preferred environment

### Virtualization and Lab Setup

#### Learning Objectives
- Set up virtualization within Kali Linux
- Create and configure vulnerable virtual machines
- Establish isolated networks for testing
- Install target systems for practice

#### Resources
- **Reading**: "Building Virtual Machine Labs" by Tony Robinson
- **Kali Linux Virtualization**:
  ```bash
  # Install virtualization tools
  sudo apt install virtualbox -y
  
  # Or QEMU/KVM
  sudo apt install qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils virt-manager -y
  ```
- **Practice**: Set up a vulnerable VM (like Metasploitable) in an isolated network

## Stage 3: Information Gathering and Reconnaissance (2-3 weeks)

### Passive Reconnaissance

#### Learning Objectives
- Master OSINT (Open Source Intelligence) techniques
- Learn to gather information without direct interaction
- Use Kali Linux tools for passive information gathering
- Document findings effectively

#### Resources
- **Reading**: "Open Source Intelligence Techniques" by Michael Bazzell
- **Kali Linux Tools**:
  ```bash
  # Install and use OSINT tools
  sudo apt install maltego theharvester recon-ng spiderfoot -y
  
  # Basic DNS reconnaissance
  dig any example.com
  host -a example.com
  dnsenum example.com
  ```
- **Practice**: Perform passive reconnaissance on a public company (with permission)

### Active Reconnaissance

#### Learning Objectives
- Learn network scanning techniques
- Master port scanning and service enumeration
- Identify operating systems and applications
- Document network topology

#### Resources
- **Reading**: "Nmap Network Scanning" by Gordon Lyon (Fyodor)
- **Kali Linux Tools**:
  ```bash
  # Basic Nmap scans
  sudo nmap -sS -T4 192.168.1.0/24
  sudo nmap -sV -O target_ip
  sudo nmap -A -T4 target_ip
  
  # Service enumeration
  enum4linux target_ip
  nikto -h target_ip
  ```
- **Practice**: Scan your lab network and document all findings

## Stage 4: Vulnerability Assessment (3-4 weeks)

### Network Vulnerability Scanning

#### Learning Objectives
- Learn to identify network vulnerabilities
- Understand vulnerability scanning tools
- Interpret scan results and prioritize findings
- Generate professional vulnerability reports

#### Resources
- **Reading**: "Mastering Kali Linux for Advanced Penetration Testing" by Vijay Kumar Velu
- **Kali Linux Tools**:
  ```bash
  # OpenVAS setup and usage
  sudo apt install openvas -y
  sudo gvm-setup
  sudo gvm-start
  
  # Access web interface at https://127.0.0.1:9392
  ```
- **Practice**: Perform a vulnerability scan on your test environment and create a report

### Web Application Security

#### Learning Objectives
- Understand the OWASP Top 10 vulnerabilities
- Learn to use web proxies for testing
- Identify common web application flaws
- Understand secure coding practices

#### Resources
- **Reading**: "The Web Application Hacker's Handbook" by Dafydd Stuttard
- **Kali Linux Tools**:
  ```bash
  # Start Burp Suite
  burpsuite
  
  # Or OWASP ZAP
  zaproxy
  
  # Additional web testing tools
  sqlmap -u "http://target/page.php?id=1" --dbs
  wpscan --url http://target --enumerate u
  ```
- **Practice**: Identify vulnerabilities in DVWA (Damn Vulnerable Web Application)

## Next Steps

After completing this beginner learning path, proceed to the [Intermediate Learning Path](intermediate.md) to continue your ethical hacking journey.

## Additional Resources

- [Kali Linux-specific Security Tools](../../tools/kali/README.md)
- [Hands-on Exercises for Beginners](../../exercises/kali/beginner/README.md)
- [Common Ethical Hacking Methodologies](../../common/methodologies/README.md)

## Legal Reminder

Always practice ethical hacking legally and responsibly, with proper authorization for any testing activities.
