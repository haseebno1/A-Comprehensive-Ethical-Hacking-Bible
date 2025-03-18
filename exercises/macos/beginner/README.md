# Beginner Exercises - MacOS

This directory contains hands-on exercises for beginners learning ethical hacking on MacOS. Each exercise is designed to reinforce concepts from the beginner learning path.

## Exercise 1: Reconnaissance and Information Gathering

### Objective
Practice passive reconnaissance techniques to gather information about a target website.

### Prerequisites
- Completed Stage 1 of the Beginner Learning Path
- MacOS with basic tools installed

### Tools Needed
- Web browser
- Terminal
- Whois lookup tool
- DNS lookup tools

### Instructions

1. Choose a legitimate website (e.g., a university or company website)
2. Gather the following information:
   - Domain registration details (registrar, dates, contact info)
   - IP address ranges
   - Name servers
   - Mail servers
   - Subdomains
   - Technologies used on the website

#### MacOS Commands
```bash
# Install necessary tools
brew install whois bind dnsrecon

# Whois lookup
whois example.com

# DNS lookup
dig example.com ANY
dig MX example.com
dig NS example.com

# Find subdomains (requires dnsrecon)
dnsrecon -d example.com -D /usr/share/wordlists/subdomains.txt -t brt
```

### Deliverables
Create a report documenting:
1. The information gathered
2. The methods and tools used
3. Potential security implications of the information found
4. Recommendations for the target to improve their security posture

### Learning Outcome
You'll understand how much information is publicly available about organizations and how this information can be used in the initial stages of security testing.

## Exercise 2: Network Scanning

### Objective
Learn to scan networks and identify open ports and services.

### Prerequisites
- Completed Stage 1 of the Beginner Learning Path
- MacOS with Nmap installed

### Tools Needed
- Nmap
- Terminal

### Instructions

1. Set up a target VM or use your local network (with permission)
2. Perform the following scans:
   - Basic port scan
   - Service detection scan
   - OS detection scan
   - Comprehensive scan

#### MacOS Commands
```bash
# Install Nmap if not already installed
brew install nmap

# Basic port scan
nmap 192.168.1.1

# Service detection
nmap -sV 192.168.1.1

# OS detection
nmap -O 192.168.1.1

# Comprehensive scan
nmap -A 192.168.1.1

# Save results to a file
nmap -A 192.168.1.1 -oN scan_results.txt
```

### Deliverables
Create a report documenting:
1. The scan results for each type of scan
2. Differences between scan types
3. Potential vulnerabilities identified
4. Recommendations for securing the scanned systems

### Learning Outcome
You'll learn how to discover hosts, open ports, and services on a network, which is essential for identifying potential entry points.

## Exercise 3: Setting Up a Virtual Lab Environment

### Objective
Create a secure, isolated environment for ethical hacking practice.

### Prerequisites
- Completed Stage 2 of the Beginner Learning Path
- MacOS with virtualization software installed

### Tools Needed
- VirtualBox, VMware Fusion, or Parallels Desktop
- Terminal

### Instructions

1. Install virtualization software
   ```bash
   # Using Homebrew to install VirtualBox
   brew install --cask virtualbox
   
   # Or install VMware Fusion or Parallels Desktop from their websites
   ```

2. Create an isolated network
   - In VirtualBox: Create a Host-Only Network in Preferences
   - In VMware Fusion: Configure Custom Network
   - In Parallels: Set up Isolated Network

3. Download and set up vulnerable VMs
   - OWASP WebGoat: https://owasp.org/www-project-webgoat/
   - Metasploitable: https://sourceforge.net/projects/metasploitable/
   - DVWA: http://www.dvwa.co.uk/

4. Configure network settings for isolation
   ```bash
   # Check your host-only network settings
   ifconfig
   
   # Ensure VMs are configured to use the host-only network
   # This is done in the VM settings
   ```

### Deliverables
Document your lab setup including:
1. Network diagram showing the isolated environment
2. List of installed VMs with their purposes
3. Network configuration details
4. Verification that the lab is properly isolated

### Learning Outcome
You'll learn how to create a safe, isolated environment for practicing ethical hacking techniques without risking damage to production systems or legal issues.

## Exercise 4: Basic Password Cracking

### Objective
Understand password cracking techniques and tools.

### Prerequisites
- Completed Stage 3 of the Beginner Learning Path
- MacOS with password cracking tools installed

### Tools Needed
- John the Ripper
- Hashcat
- Terminal

### Instructions

1. Create sample password hash files
   ```bash
   # Install John the Ripper
   brew install john-jumbo
   
   # Create a sample password file
   echo "user:$(openssl passwd -crypt password123)" > passwords.txt
   ```

2. Use John the Ripper to crack the passwords
   ```bash
   # Basic cracking
   john passwords.txt
   
   # Show cracked passwords
   john --show passwords.txt
   ```

3. Experiment with different wordlists and rules
   ```bash
   # Download a wordlist
   curl -L -o wordlist.txt https://github.com/danielmiessler/SecLists/raw/master/Passwords/Common-Credentials/10-million-password-list-top-1000.txt
   
   # Use a wordlist
   john --wordlist=wordlist.txt passwords.txt
   
   # Use rules
   john --wordlist=wordlist.txt --rules passwords.txt
   ```

4. Try Hashcat for GPU-accelerated cracking (if you have a compatible GPU)
   ```bash
   # Install Hashcat
   brew install hashcat
   
   # Basic usage
   hashcat -m 0 -a 0 hash.txt wordlist.txt
   ```

### Deliverables
Create a report documenting:
1. The different cracking methods used
2. Effectiveness of different wordlists and rules
3. Performance comparison between tools
4. Recommendations for creating strong passwords that resist these attacks

### Learning Outcome
You'll understand how password cracking works and why strong, unique passwords are essential for security.

## Exercise 5: Web Application Vulnerability Assessment

### Objective
Identify and understand common web vulnerabilities.

### Prerequisites
- Completed Stage 4 of the Beginner Learning Path
- MacOS with web testing tools installed
- Vulnerable web application (DVWA, WebGoat) set up in your lab

### Tools Needed
- OWASP ZAP or Burp Suite
- Web browser
- Terminal

### Instructions

1. Start the vulnerable web application in your lab environment

2. Configure your proxy tool
   ```bash
   # Install OWASP ZAP
   brew install --cask owasp-zap
   
   # Or Burp Suite
   brew install --cask burp-suite
   ```

3. Identify and explore the following vulnerabilities:
   - SQL Injection
   - Cross-Site Scripting (XSS)
   - Insecure Direct Object References
   - Cross-Site Request Forgery (CSRF)

4. Document each vulnerability with:
   - Description of the vulnerability
   - How you identified it
   - Potential impact
   - Remediation steps

### Deliverables
Create a comprehensive report including:
1. Detailed findings for each vulnerability
2. Screenshots demonstrating the vulnerabilities
3. Explanation of the underlying security flaws
4. Recommended fixes for each issue

### Learning Outcome
You'll gain practical experience identifying and understanding common web vulnerabilities, which is essential for web application security testing.

## Next Steps

After completing these exercises, consider moving on to the [Intermediate Exercises](../intermediate/) to continue developing your skills.

## Legal Reminder

Always practice ethical hacking legally and responsibly, with proper authorization for any testing activities. These exercises should only be performed in your controlled lab environment or on systems you have explicit permission to test.
