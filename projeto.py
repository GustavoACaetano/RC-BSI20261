# IMPORTACOES MININET
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.cli import CLI

# IMPORTACAO SISTEMA
import os

# PARAR MONGODB DO SISTEMA
os.system('service mongodb stop')
os.system('systemctl disable mongodb')
os.system('pkill -f mongod')
os.system('sleep 2')
# precisei fazer isso porque o mongodb do sistema estava sobrepondo o processo do mongodb criado no mininet
# estava causando falhas de conexão e impedindo o acesso da web api ao banco 

# CLASSE PARA ROTEADOR LINUX
class LinuxRouter(Node):
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl -w net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl -w net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()

# CLASSE PARA TOPOLOGIA
class MyTopo(Topo):
    def build(self):
        # SWITCHES
        s4 = self.addSwitch('s4') # Esse é o switch DMZ, utilizar o nome sdmz estava dando erro, então utilizei s4 para representar
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')

        # ROTEADORES
        fw = self.addNode('fw', cls=LinuxRouter)
        r1 = self.addNode('r1', cls=LinuxRouter)
        r2 = self.addNode('r2', cls=LinuxRouter)
        r3 = self.addNode('r3', cls=LinuxRouter)

        # CLIENTE EXTERNO
        ce = self.addHost('ce', ip='172.27.0.10/12', defaultRoute='via 172.27.0.1')

        # CLIENTES INTERNOS
        c1 = self.addHost('c1', ip='192.168.119.10/24', defaultRoute='via 192.168.119.1')
        c2 = self.addHost('c2', ip='192.168.119.11/24', defaultRoute='via 192.168.119.1')
        c3 = self.addHost('c3', ip='192.168.119.12/24', defaultRoute='via 192.168.119.1')
        c4 = self.addHost('c4', ip='192.168.119.13/24', defaultRoute='via 192.168.119.1')
        c5 = self.addHost('c5', ip='192.168.119.14/24', defaultRoute='via 192.168.119.1')

        # SERVIÇOS
        sshServer = self.addHost('sshServer', ip='192.168.8.10/24', defaultRoute='via 192.168.8.1')
        httpServer = self.addHost('httpServer', ip='192.168.8.20/24', defaultRoute='via 192.168.8.1')
        webapi = self.addHost('webapi', ip='192.168.8.30/24', defaultRoute='via 192.168.8.1')

        # DATABASE
        mongoDB = self.addHost('mongoDB', ip='192.168.79.10/24', defaultRoute='via 192.168.79.1')

        # LINKS DMZ
        self.addLink(ce, s4)
        self.addLink(fw, s4)

        # LINKS CLIENTES
        self.addLink(fw, s1)
        self.addLink(r1, s1)
        self.addLink(c1, s1)
        self.addLink(c2, s1)
        self.addLink(c3, s1)
        self.addLink(c4, s1)
        self.addLink(c5, s1)

        # LINKS SERVIÇOS
        self.addLink(r2, s2)
        self.addLink(sshServer, s2)
        self.addLink(httpServer, s2)
        self.addLink(webapi, s2)

        # LINKS DATABASE
        self.addLink(r3, s3)
        self.addLink(mongoDB, s3)

        # LINKS ENTRE ROTEADORES
        self.addLink(r1, r2)
        self.addLink(r1, r3)
        self.addLink(r2, r3)

# INSTANCIAR TOPOLOGIA
topo = MyTopo()

# INICIAR A REDE MININET
net = Mininet(topo=topo)
net.start()

# PEGAR REFERÊNCIAS DO FIREWALL E ROTEADORES
fw = net.get('fw')
r1 = net.get('r1')
r2 = net.get('r2')
r3 = net.get('r3')

# CONFIG FW
fw.cmd('ifconfig fw-eth0 172.27.0.1/12')
fw.cmd('ifconfig fw-eth1 192.168.119.254/24')

# CONFIG R1
r1.cmd('ifconfig r1-eth0 192.168.119.1/24')
r1.cmd('ifconfig r1-eth1 10.3.0.1/16')
r1.cmd('ifconfig r1-eth2 10.5.0.1/16')

# CONFIG R2
r2.cmd('ifconfig r2-eth0 192.168.8.1/24')
r2.cmd('ifconfig r2-eth1 10.3.0.2/16')
r2.cmd('ifconfig r2-eth2 10.10.0.1/16')

# CONFIG R3
r3.cmd('ifconfig r3-eth0 192.168.79.1/24')
r3.cmd('ifconfig r3-eth1 10.5.0.2/16')
r3.cmd('ifconfig r3-eth2 10.10.0.2/16')

# ROTAS R1
r1.cmd('route add -net 192.168.8.0/24 gw 10.3.0.2')
r1.cmd('route add -net 192.168.79.0/24 gw 10.5.0.2')

# ROTAS R2
r2.cmd('route add -net 192.168.119.0/24 gw 10.3.0.1')
r2.cmd('route add -net 192.168.79.0/24 gw 10.10.0.2')

# ROTAS R3
r3.cmd('route add -net 192.168.119.0/24 gw 10.5.0.1')
r3.cmd('route add -net 192.168.8.0/24 gw 10.10.0.1')

# ROTAS FIREWALL
fw.cmd('route add -net 192.168.8.0/24 gw 192.168.119.1')
fw.cmd('route add -net 192.168.79.0/24 gw 192.168.119.1')

# FIREWALL
fw.cmd('iptables -F')
fw.cmd('iptables -t nat -F')
fw.cmd('iptables -P INPUT DROP')
fw.cmd('iptables -P FORWARD DROP')
fw.cmd('iptables -A INPUT -i lo -j ACCEPT')
fw.cmd('iptables -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT')
# LIBERAR HTTP
fw.cmd('iptables -A FORWARD -s 172.27.0.10 -d 192.168.8.20 -p tcp --dport 80 -j ACCEPT')
# LIBERAR SSH
fw.cmd('iptables -A FORWARD -s 172.27.0.10 -d 192.168.8.10 -p tcp --dport 22 -j ACCEPT')
# LIBERAR API
fw.cmd('iptables -A FORWARD -s 172.27.0.10 -d 192.168.8.30 -p tcp --dport 5000 -j ACCEPT')
# LIBERAR MONGODB
fw.cmd('iptables -A FORWARD -s 192.168.8.30 -d 192.168.79.10 -p tcp --dport 27017 -j ACCEPT')
# BLOQUEAR PING DO CLIENTE EXTERNO
fw.cmd('iptables -A FORWARD -s 172.27.0.10 -p icmp -j DROP')
# NAT
fw.cmd('iptables -t nat -A POSTROUTING -o fw-eth1 -j MASQUERADE')

# HTTP SERVER
httpServer = net.get('httpServer')
httpServer.cmd('python3 -m http.server 80 &')

# SSH SERVER
sshServer = net.get('sshServer')
sshServer.cmd('/usr/sbin/sshd &')

# MONGODB
mongoDB = net.get('mongoDB')
mongoDB.cmd('rm -rf /tmp/mongo')
mongoDB.cmd('mkdir -p /tmp/mongo')
mongoDB.cmd('mongod --dbpath /tmp/mongo --bind_ip 0.0.0.0 --port 27018 --fork --logpath /tmp/mongo.log')
mongoDB.cmd('sleep 2')

# WEB API
webapi = net.get('webapi')
webapi.cmd('route add -net 192.168.79.0/24 gw 192.168.8.1')
webapi.cmd('cp api.py .')
webapi.cmd('python3 api.py &')

# ABRE CLI DO MININET
CLI(net)

# ENCERRAR REDE MININET
net.stop()