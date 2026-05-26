def configurar_firewall(fw):
    # Limpa todas as regras do firewall
    fw.cmd('iptables -F')

    # Limpa todas as regras da tabela NAT do firewall
    fw.cmd('iptables -t nat -F')

    # Política padrão da cadeia INPUT como DROP
    # Pacote destinado ao firewall bloqueado por padrão
    fw.cmd('iptables -P INPUT DROP')

    # Política padrão da cadeia FORWARD COMO DROP
    # Pacote passando pelo firewall bloqueado por padrão
    fw.cmd('iptables -P FORWARD DROP')

    # Permite tráfego da interface de loopback
    fw.cmd('iptables -A INPUT -i lo -j ACCEPT')

    # Permite pacotes de resposta de conexões estabelecidas
    fw.cmd('iptables -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT')

    # Permite repostas de conexões estabelecidas destinadas ao firewall
    fw.cmd('iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT')

    # Libera acesso HTTP do cliente externo para o servidor web
    # Porta 80 = HTTP
    fw.cmd('iptables -A FORWARD -s 172.27.0.10 -d 192.168.8.20 -p tcp --dport 80 -j ACCEPT')
    # Libera respostas do servidor HTTP
    fw.cmd('iptables -A FORWARD -p tcp --sport 80 -j ACCEPT')

    # Libera acesso SSH do cliente externo para o servidor SSH
    # Porta 22 = SSH
    fw.cmd('iptables -A FORWARD -s 172.27.0.10 -d 192.168.8.10 -p tcp --dport 22 -j ACCEPT')
    # Libera respostas do servidor SSH
    fw.cmd('iptables -A FORWARD -p tcp --sport 22 -j ACCEPT')

    # Libera acesso a API WEB do cliente externo
    # Porta 5000 = FLASK
    fw.cmd('iptables -A FORWARD -s 172.27.0.10 -d 192.168.8.30 -p tcp --dport 5000 -j ACCEPT')
    # Libera respostas da API WEB
    fw.cmd('iptables -A FORWARD -p tcp --sport 5000 -j ACCEPT')

    # Libera comunicacao entre API WEB e o banco MongoDB
    # Porta 27017 = MONGODB
    fw.cmd('iptables -A FORWARD -s 192.168.8.30 -d 192.168.79.10 -p tcp --dport 27017 -j ACCEPT')
    # Libera respostas do MongoDB
    fw.cmd('iptables -A FORWARD -p tcp --sport 27017 -j ACCEPT')

    # Bloueia pacotes ICMP (PING) vindos do cliente externo
    fw.cmd('iptables -A FORWARD -s 172.27.0.10 -p icmp -j DROP')

    # Aplica NAT (MASQUERADE) nos pacotes saindo pela interface externa
    fw.cmd('iptables -t nat -A POSTROUTING -o fw-eth1 -j MASQUERADE')
