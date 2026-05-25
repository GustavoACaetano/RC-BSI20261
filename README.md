# Projeto Final - Redes de Computadores

**Discente:** Gustavo Alves Caetano

---

# Especificação do Projeto

## Índice

- [Tema](#tema)
- [Objetivo](#objetivo)
- [Estrutura da Topologia](#estrutura-da-topologia)
- [DMZ](#dmz)
- [Redes Internas](#redes-internas)
- [Interligação entre Roteadores](#interligação-entre-roteadores)
- [Endereçamento IP Individual](#endereçamento-ip-individual)
- [Requisitos do Script Python](#requisitos-do-script-python)
- [API Web](#api-web)
- [Regras de Segurança](#regras-de-segurança)
- [Critérios de Avaliação](#critérios-de-avaliação)
- [Observações](#observações)

---

## Tema

**DevOps — Infra virtualizada para aplicações utilizando Mininet**

---

## Objetivo

Desenvolver individualmente uma infraestrutura virtualizada utilizando a ferramenta <a href="https://mininet.org/">Mininet</a> com script em Python, simulando uma rede corporativa contendo:

- DMZ (Zona Desmilitarizada)
- Firewall/NAT
- Rede Interna segmentada
- Serviços de rede
- API Web com CRUD
- Banco de Dados MongoDB

---

## Estrutura da Topologia

### Visão Geral da Infraestrutura

<p align="center">
  <img
    width="688"
    height="298"
    alt="Topologia da Rede"
    src="https://github.com/user-attachments/assets/a7e3455d-f1de-4331-a422-8588557faa92"
  />
</p>

A topologia deverá conter uma DMZ conectada a um Firewall/NAT, responsável por controlar o acesso à rede interna segmentada em diferentes sub-redes.

---

## DMZ

A DMZ representa a área da rede exposta ao público externo.

### Componentes

| Dispositivo | Descrição |
|---|---|
| CE | Cliente Externo utilizado para testar os serviços |
| SDMZ | Switch Layer 2 da DMZ |
| FW | Firewall/NAT responsável pela proteção da rede interna |

### Regras

- O firewall deve possuir:
  - 1 interface conectada à DMZ
  - 1 interface conectada à rede interna
- Apenas o host `CE` pode acessar os serviços expostos da rede interna
- O ping entre `CE` e hosts internos deve ser bloqueado

---

## Redes Internas

A infraestrutura interna deve possuir **3 sub-redes**, cada uma contendo:

- 1 switch
- 1 roteador

---

### 1. Rede de Clientes Internos

#### Hosts obrigatórios

- `c1`
- `c2`
- `c3`
- `c4`
- `c5`

#### Endereço da Rede

```txt
192.168.119.0/24
```

---

### 2. Rede de Serviços

#### Serviços obrigatórios

| Host | Serviço |
|---|---|
| servidorSSH | SSH |
| servidorHTTP | HTTP |
| app | Web API |

#### Endereço da Rede

```txt
192.168.8.0/24
```

---

### 3. Rede de Banco de Dados

#### Banco de Dados

| Host | Banco |
|---|---|
| servidorMongoDB | MongoDB |

#### Endereço da Rede

```txt
192.168.79.0/24
```

---

## Interligação entre Roteadores

Os roteadores devem estar conectados da seguinte forma:

```txt
R1 <-> R2
R1 <-> R3
R2 <-> R3
```

### Redes dos Links

| Link | Rede |
|---|---|
| R1 ↔ R2 | 10.3.0.0/16 |
| R1 ↔ R3 | 10.5.0.0/16 |
| R2 ↔ R3 | 10.10.0.0/16 |

---

## Endereçamento IP Individual

| Segmento | Rede |
|---|---|
| DMZ | 172.27.0.0/12 |
| Rede de Serviços | 192.168.8.0/24 |
| Rede de Banco de Dados | 192.168.79.0/24 |
| Rede Clientes Internos | 192.168.119.0/24 |
| Rede R1-R2 | 10.3.0.0/16 |
| Rede R1-R3 | 10.5.0.0/16 |
| Rede R2-R3 | 10.10.0.0/16 |

---

## Requisitos do Script Python

O script deve obrigatoriamente conter:

```python
class MyTopo(Topo):
```

```python
topo = MyCustomTopo()
```

```python
net = Mininet(topo=topo)
```

```python
net.start()
CLI(net)
net.stop()
```

---

## API Web

### Tecnologia Recomendada

- Python Flask
ou
- FastAPI

---

### Tema da API

#### Registro de Carros

### Estrutura do Registro

```json
{
  "placa": "STR",
  "chassis": "STR",
  "proprietario": "STR",
  "status": "licenciado | com restrição"
}
```

---

### Operações Obrigatórias

A API deve implementar as seguintes operações CRUD:

- GET
- POST
- PUT
- DELETE

---

## Regras de Segurança

O firewall deve:

- Bloquear ping entre `CE` e hosts internos
- Permitir acesso apenas aos serviços autorizados:
  - SSH
  - HTTP
  - API Web
- Bloquear qualquer outro serviço

---

## Critérios de Avaliação

| Critério | Peso |
|---|---|
| Conectividade geral | 20% |
| Implementação da DMZ e Firewall | 10% |
| Restrições de segurança | 30% |
| Funcionamento dos serviços permitidos | 20% |
| Funcionamento da API Web (CRUD) | 20% |

---

## Observações

- Caso o script não execute corretamente, a nota será zero
- O trabalho é individual
- O arquivo deve ser enviado no AVA até a data especificada pelo professor
