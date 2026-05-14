# Banner grabbing para identificar serviços.

COMMON_SERVICES = {
    22: "SSH",
    80: "HTTP",
    443: "HTTPS",
    3306: "MySQL",
    21: "FTP",
    25: "SMTP",
    110: "POP3",
    143: "IMAP",
    53: "DNS",

}


def identify_service(port):
    return COMMON_SERVICES.get(port, "Desconhecido")
