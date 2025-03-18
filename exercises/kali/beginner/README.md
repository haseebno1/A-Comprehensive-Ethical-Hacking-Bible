# Beginner Exercises - Kali Linux

This directory contains hands-on exercises for beginners learning ethical hacking on Kali Linux. Each exercise is designed to reinforce concepts from the beginner learning path.

## Exercise 1: Reconnaissance and Information Gathering

### Objective
Practice passive reconnaissance techniques to gather information about a target website.

### Prerequisites
- Completed Stage 1 of the Beginner Learning Path
- Kali Linux with basic tools installed

### Tools Needed
- Web browser
- Terminal
- Whois, dig, and other DNS tools (pre-installed in Kali)
- TheHarvester, Recon-ng

### Instructions

1. Choose a legitimate website (e.g., a university or company website)
2. Gather the following information:
   - Domain registration details (registrar, dates, contact info)
   - IP address ranges
   - Name servers
   - Mail servers
   - Subdomains
   - Technologies used on the website

#### Kali Linux Commands
```bash
# Whois lookup
whois example.com

# DNS lookup
dig example.com ANY
dig MX example.com
dig NS example.com

# Find subdomains
dnsenum example.com
amass enum -d example.com

# Email harvesting
theHarvester -d example.com -b all

# Web technologies identification
whatweb example.com
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
- Kali Linux with Nmap installed (pre-installed)

### Tools Needed
- Nmap
- Terminal
- Zenmap (optional GUI for Nmap)

### Instructions

1. Set up a target VM or use your local network (with permission)
2. Perform the following scans:
   - Basic port scan
   - Service detection scan
   - OS detection scan
   - Comprehensive scan

#### Kali Linux Commands
```bash
# Basic port scan
sudo nmap 192.168.1.1

# Service detection
sudo nmap -sV 192.168.1.1

# OS detection
sudo nmap -O 192.168.1.1

# Comprehensive scan
sudo nmap -A 192.168.1.1

# Save results to a file
sudo nmap -A 192.168.1.1 -oN scan_results.txt

# Using Zenmap (GUI)
sudo zenmap
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
- Kali Linux with virtualization software installed

### Tools Needed
- VirtualBox or QEMU/KVM
- Terminal

### Instructions

1. Install virtualization software (if not already installed)
   ```bash
   # Install VirtualBox
   sudo apt update
   sudo apt install virtualbox -y
   
   # Or install QEMU/KVM
   sudo apt install qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils virt-manager -y
   ```

2. Create an isolated network
   ```bash
   # For VirtualBox
   # Create a host-only network through the GUI or:
   VBoxManage hostonlyif create
   VBoxManage hostonlyif ipconfig vboxnet0 --ip 192.168.56.1
   
   # For QEMU/KVM (using virt-manager GUI is easier)
   sudo virsh net-define isolated-network.xml
   sudo virsh net-start isolated
   sudo virsh net-autostart isolated
   ```

3. Download and set up vulnerable VMs
   ```bash
   # Download Metasploitable
   wget https://sourceforge.net/projects/metasploitable/files/Metasploitable2/metasploitable-linux-2.0.0.zip
   unzip metasploitable-linux-2.0.0.zip
   
   # Import into virtualization software
   # For VirtualBox, use the GUI to import the .vmdk file
   # For QEMU/KVM, use virt-manager to create a new VM using the existing disk
   ```

4. Configure network settings for isolation
   ```bash
   # Verify network isolation
   # All VMs should be able to communicate with each other but not with the internet
   # Test with ping between VMs
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
- Kali Linux with password cracking tools installed (pre-installed)

### Tools Needed
- John the Ripper
- Hashcat
- Terminal

### Instructions

1. Create sample password hash files
   ```bash
   # Create a sample password file
   echo "user:$(openssl passwd -crypt password123)" > passwords.txt
   
   # Or use unshadow to combine /etc/passwd and /etc/shadow (on a test system)
   sudo unshadow /etc/passwd /etc/shadow > combined_passwords.txt
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
   # Kali has pre-installed wordlists
   ls /usr/share/wordlists/
   
   # Use rockyou wordlist (may need to be unzipped first)
   sudo gunzip /usr/share/wordlists/rockyou.txt.gz
   john --wordlist=/usr/share/wordlists/rockyou.txt passwords.txt
   
   # Use rules
   john --wordlist=/usr/share/wordlists/rockyou.txt --rules passwords.txt
   ```

4. Try Hashcat for GPU-accelerated cracking (if you have a compatible GPU)
   ```bash
   # Basic usage
   hashcat -m 0 -a 0 hash.txt /usr/share/wordlists/rockyou.txt
   
   # With rules
   hashcat -m 0 -a 0 hash.txt /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule
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
- Kali Linux with web testing tools installed (pre-installed)
- Vulnerable web application (DVWA, WebGoat) set up in your lab

### Tools Needed
- OWASP ZAP or Burp Suite
- Web browser
- Terminal

### Instructions

1. Start the vulnerable web application in your lab environment
   ```bash
   # If using Docker for DVWA
   sudo docker run --rm -it -p 80:80 vulnerables/web-dvwa
   
   # If using Docker for WebGoat
   sudo docker run --rm -it -p 8080:8080 -p 9090:9090 webgoat/webgoat
   ```

2. Configure your proxy tool
   ```bash
   # Start OWASP ZAP
   zaproxy
   
   # Or Burp Suite
   burpsuite
   ```

3. Identify and explore the following vulnerabilities:
   - SQL Injection
   ```bash
   # Manual testing
   # In a login form, try: ' OR 1=1 --
   
   # Using sqlmap
   sqlmap -u "http://target-ip/dvwa/vulnerabilities/sqli/?id=1&Submit=Submit" --cookie="security=low; PHPSESSID=your_session_id" --dbs
   ```
   
   - Cross-Site Scripting (XSS)
   ```bash
   # Test with basic payload
   # In a search or comment field, try: <script>alert('XSS')</script>
   ```
   
   - Insecure Direct Object References
   ```bash
   # Try changing IDs in URLs
   # Example: change profile.php?id=123 to profile.php?id=124
   ```
   
   - Cross-Site Request Forgery (CSRF)
   ```bash
   # Create a simple HTML form that submits to the target application
   ```

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
