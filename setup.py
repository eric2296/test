import subprocess
import requests
import os

url = 'https://github.com/eric2296/test/raw/main/client'
#url='https://www.facebook.com/favicon.ico'

if __name__ == "__main__":
   package_name = "nmap"
   subprocess.run(["sudo", "apt", "install", "-y", package_name], check=True)

""" 
  r = requests.get(url, allow_redirects=True, stream=True)
   with open("client","wb") as f:
      f.write(r.content)
"""
#   subprocess.call(['chmod', '0777', 'client'])
#   os.system('client')
