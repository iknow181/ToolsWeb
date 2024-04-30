#  扫描器
import nmapfun
import nmap
from ipaddress import IPv4Network


def query(user_ip):
    # 使用 nmap 扫描用户主机
    nm = nmap.PortScanner()
    nm.scan(user_ip, arguments='-F -O')

    # 解析扫描结果并获取信息
    result = []
    for host in nm.all_hosts():
        host_info = {"host": host, "ports": [], "os_info": None}
        for proto in nm[host].all_protocols():
            ports = nm[host][proto].keys()
            for port in ports:
                service = nm[host][proto][port]['name']
                host_info["ports"].append({"port": port, "service": service})
        if 'osclass' in nm[host]:
            os_info = nm[host]['osclass']
            host_info["os_info"] = {"osfamily": os_info['osfamily'], "osgen": os_info['osgen']}
        result.append(host_info)
    return result


def get_user_network(user_ip):
    # 假设用户的 IP 地址为 IPv4 格式，例如 '192.168.1.100'
    # 提取出子网前缀，例如 '192.168.1'
    user_subnet_prefix = '.'.join(user_ip.split('.')[:-1])
    # 将子网前缀与子网掩码组合起来，例如 '192.168.1.0/24'
    user_network = user_subnet_prefix + '.0/24'
    return user_network

