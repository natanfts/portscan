 #Banner grabbing para identificar serviços.


import socket

def grab_banner(target_ip, port, timeout=2):
    try:
        sock = socket.socket()
        sock.settimeout(timeout)
        sock.connect((target_ip, port))
        banner = sock.recv(1024).decode(errors="ignore").strip()
        sock.close()
        if banner:
            return banner
        else:
            return "Sem banner identificado"
    except Exception:
        return "Não foi possível capturar banner"
