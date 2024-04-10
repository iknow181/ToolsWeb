from nmap import *

nm = PortScanner()
nm.scan('192.168.142.0/24', '1-500')
for host in nm.all_hosts():
    print('-'*30)
    print(f'Host: {host}')
    print(f'State: {nm[host].state()}')
    print('-'*30)
    for proto in nm[host].all_protocols():
        print(f'Protocol: {proto}')
        lport = sorted(nm[host][proto].keys())
        for port in lport:
            print(f'{port}\tstate: {nm[host][proto][port]["state"]}')