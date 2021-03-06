import requests
import random
response =requests.get("https://proxy.webshare.io/api/proxy/list/?page=2", headers={"Authorization":"Token 9f4c211268e13496ee85676c04870479d4a8e676"})
result = response.json()

data =result['results']
select_ip = random.choice(data)
port=select_ip['ports']['socks5']
ip=select_ip['proxy_address']
username=select_ip['username']
password=select_ip['password']

print(port,ip,username,password)