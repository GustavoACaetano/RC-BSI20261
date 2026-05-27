def configurar_firewall(fw):
    fw.cmd('iptables -F')

    fw.cmd('iptables -t nat -F')

    fw.cmd('iptables -P INPUT DROP')

    fw.cmd('iptables -P FORWARD DROP')

    fw.cmd('iptables -A INPUT -i lo -j ACCEPT')

    fw.cmd('iptables -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT')

    fw.cmd('iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT')

    fw.cmd('iptables -A FORWARD -s 172.27.0.10 -d 192.168.8.20 -p tcp --dport 80 -j ACCEPT')

    fw.cmd('iptables -A FORWARD -s 172.27.0.10 -d 192.168.8.10 -p tcp --dport 22 -j ACCEPT')

    fw.cmd('iptables -A FORWARD -s 172.27.0.10 -d 192.168.8.30 -p tcp --dport 5000 -j ACCEPT')

    fw.cmd('iptables -A FORWARD -s 192.168.8.30 -d 192.168.79.10 -p tcp --dport 27017 -j ACCEPT')

    fw.cmd('iptables -t nat -A POSTROUTING -o fw-eth1 -j MASQUERADE')
