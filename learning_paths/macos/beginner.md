# Beginner Learning Path - MacOS

This guide provides a structured learning path for ethical hacking using MacOS, taking you from the fundamentals to practical skills.

## Stage 1: Understanding the Basics (2-4 weeks)

### Ethical Hacking Concepts

#### Learning Objectives
- Understand what ethical hacking is and its importance
- Learn the legal and ethical boundaries of security testing
- Differentiate between types of hackers and their motivations
- Familiarize yourself with penetration testing methodologies

#### Resources
- **Reading**: [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- **Video Course**: [Ethical Hacking Introduction](https://www.youtube.com/playlist?list=PLBf0hzazHTGOEuhPQSnq-Ej8jRyXxfYvl)
- **Practice**: Create a document outlining the ethical considerations for a hypothetical penetration test

### Networking Fundamentals

#### Learning Objectives
- Understand the TCP/IP model and common protocols
- Learn IP addressing, subnetting, and routing basics
- Master network troubleshooting tools on MacOS
- Identify different network devices and their functions

#### Resources
- **Reading**: "TCP/IP Illustrated, Volume 1" by W. Richard Stevens
- **MacOS Tools**: 
  ```bash
  # Install network utilities
  brew install nmap wireshark tcpdump
  
  # Basic network commands
  ifconfig
  netstat -r
  ping google.com
  traceroute google.com
  ```
- **Practice**: Map your home network using the Network Utility app and terminal commands

### MacOS Command Line Basics

#### Learning Objectives
- Master essential Terminal commands
- Understand file system navigation and permissions
- Learn process management and system monitoring
- Configure Terminal for productivity

#### Resources
- **Reading**: "Learning the bash Shell" by Cameron Newham
- **MacOS Terminal Commands**:
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
  ```
- **Practice**: Create a shell script that automates a system maintenance task

### Programming Fundamentals

#### Learning Objectives
- Learn basic Python syntax and data structures
- Understand control flow (if/else, loops, functions)
- Master file operations and error handling
- Create simple automation scripts

#### Resources
- **Reading**: "Automate the Boring Stuff with Python" by Al Sweigart
- **MacOS Setup**:
  ```bash
  # Install Python and pip
  brew install python
  
  # Create a virtual environment
  python3 -m venv ~/ethical_hacking_env
  source ~/ethical_hacking_env/bin/activate
  
  # Install useful packages
  pip install requests scapy pycryptodome
  ```
- **Practice**: Write a Python script that scans your local network for active hosts

## Stage 2: Setting Up Your Environment (1-2 weeks)

### MacOS Security Tools Installation

#### Learning Objectives
- Set up a comprehensive ethical hacking toolkit on MacOS
- Configure tools for optimal performance
- Understand tool dependencies and requirements
- Create isolated testing environments

#### Resources
- **Reading**: [MacOS Environment Setup Guide](../../docs/macos/environment_setup.md)
- **Essential Tools**:
  ```bash
  # Install via Homebrew
  brew install nmap wireshark netcat john-jumbo hydra aircrack-ng
  brew install --cask burp-suite owasp-zap
  ```
- **Practice**: Create a custom installation script that sets up all necessary tools

### Virtualization Setup

#### Learning Objectives
- Set up virtualization software on MacOS
- Create and configure virtual machines
- Establish isolated networks for testing
- Install vulnerable systems for practice

#### Resources
- **Reading**: "Virtualizing Security" by Ken Hess
- **MacOS Virtualization**:
  ```bash
  # Install VirtualBox
  brew install --cask virtualbox
  
  # Or VMware Fusion
  brew install --cask vmware-fusion
  ```
- **Practice**: Set up a Kali Linux VM and a vulnerable VM (like Metasploitable) in an isolated network

## Stage 3: Information Gathering and Reconnaissance (2-3 weeks)

### Passive Reconnaissance

#### Learning Objectives
- Master OSINT (Open Source Intelligence) techniques
- Learn to gather information without direct interaction
- Use MacOS tools for passive information gathering
- Document findings effectively

#### Resources
- **Reading**: "Open Source Intelligence Techniques" by Michael Bazzell
- **MacOS Tools**:
  ```bash
  # Install OSINT tools
  brew install the_harvester recon-ng spiderfoot
  
  # Basic DNS reconnaissance
  dig any example.com
  host -a example.com
  ```
- **Practice**: Perform passive reconnaissance on a public company (with permission)

### Active Reconnaissance

#### Learning Objectives
- Learn network scanning techniques
- Master port scanning and service enumeration
- Identify operating systems and applications
- Document network topology

#### Resources
- **Reading**: "Network Scanning Explained" by Gordon Lyon (Fyodor)
- **MacOS Tools**:
  ```bash
  # Basic Nmap scans
  nmap -sS -T4 192.168.1.0/24
  nmap -sV -O target_ip
  nmap -A -T4 target_ip
  
  # Service enumeration
  brew install enum4linux
  ```
- **Practice**: Scan your home network (with permission) and document all findings

## Stage 4: Vulnerability Assessment (3-4 weeks)

### Network Vulnerability Scanning

#### Learning Objectives
- Learn to identify network vulnerabilities
- Understand vulnerability scanning tools
- Interpret scan results and prioritize findings
- Generate professional vulnerability reports

#### Resources
- **Reading**: "The Art of Network Penetration Testing" by Royce Davis
- **MacOS Tools**:
  ```bash
  # Install OpenVAS
  brew install openvas
  openvas-setup
  
  # Alternative: Use Nessus (commercial)
  # Download from https://www.tenable.com/products/nessus
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
- **MacOS Tools**:
  ```bash
  # Start Burp Suite
  open -a Burp\ Suite
  
  # Or OWASP ZAP
  open -a OWASP\ ZAP
  
  # Install additional tools
  brew install sqlmap nikto wpscan
  ```
- **Practice**: Identify vulnerabilities in DVWA (Damn Vulnerable Web Application)

## Next Steps

After completing this beginner learning path, proceed to the [Intermediate Learning Path](intermediate.md) to continue your ethical hacking journey.

## Additional Resources

- [MacOS-specific Security Tools](../../tools/macos/README.md)
- [Hands-on Exercises for Beginners](../../exercises/macos/beginner/README.md)
- [Common Ethical Hacking Methodologies](../../common/methodologies/README.md)

## Legal Reminder

Always practice ethical hacking legally and responsibly, with proper authorization for any testing activities.
