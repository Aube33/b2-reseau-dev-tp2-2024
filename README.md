# TP4 DEV : Socquettes

## I. Simple bs program

## 1. First steps

### 🌞 Commandes...

**Client:**
```
[antoine@client b2-reseau-dev-tp2-2024]$ python bs_client_I1.py 
Le serveur a répondu b'Hi mate !'
[antoine@client b2-reseau-dev-tp2-2024]$ echo $?
0
```

**Serveur:**
```
[antoine@server b2-reseau-dev-tp2-2024]$ sudo firewall-cmd --add-port=13337/tcp --permanent.
[sudo] password for antoine: 
success
[antoine@server b2-reseau-dev-tp2-2024]$ sudo firewall-cmd --reload
success
[antoine@server b2-reseau-dev-tp2-2024]$ sudo firewall-cmd --list-all
public (active)
  target: default
  icmp-block-inversion: no
  interfaces: enp0s3 enp0s8
  sources: 
  services: cockpit dhcpv6-client ssh
  ports: 13337/tcp
  protocols: 
  forward: yes
  masquerade: no
  forward-ports: 
  source-ports: 
  icmp-blocks: 
  rich rules: 
[antoine@server b2-reseau-dev-tp2-2024]$ python bs_server_I1.py 
Données reçues du client : b'Meooooo !'
[antoine@server b2-reseau-dev-tp2-2024]$ 
```

## 2. User friendly