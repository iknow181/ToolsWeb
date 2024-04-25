#  扫描器
import nmapfun
import nmap


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
