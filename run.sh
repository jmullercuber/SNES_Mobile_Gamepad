# ensure ports are avaliable on server
iptables -I INPUT -p tcp --dport 5000 -j ACCEPT
iptables -I INPUT -p udp --dport 5000 -j ACCEPT

python3 webhook.py
