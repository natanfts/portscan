# Analise detalhada de portas e servicos.

RISK_LEVELS = {
    22: {"risk": "Alto", "msg": "SSH aberto → possível acesso remoto Linux"},
    25: {"risk": "Alto", "msg": "SMTP aberto → servidor de email em risco"},
    53: {"risk": "Médio", "msg": "DNS aberto → possível DNS poisoning"},
    80: {"risk": "Médio", "msg": "HTTP aberto → servidor web detectado"},
    110: {"risk": "Alto", "msg": "POP3 aberto → serviço de email exposto"},
    143: {"risk": "Alto", "msg": "IMAP aberto → acesso a emails em risco"},
    443: {"risk": "Baixo", "msg": "HTTPS aberto → comunicação criptografada"},
    3306: {"risk": "Alto", "msg": "Banco de dados MySQL exposto"},
    21: {"risk": "Alto", "msg": "FTP aberto → transferência de arquivos insegura"},
}

RISK_META = {
    "Alto": {"label": "Risco", "icon": "⚠️", "tone": "risk"},
    "Médio": {"label": "Atencao", "icon": "🌐", "tone": "attention"},
    "Baixo": {"label": "OK", "icon": "✅", "tone": "safe"},
}


def analyze_port(port):
    """Retorna analise de risco e recomendacoes para a porta."""
    if port in RISK_LEVELS:
        return RISK_LEVELS[port]["msg"]
    return f"Porta {port}: serviço desconhecido"


def get_port_risk(port):
    """Retorna os metadados visuais de risco da porta."""
    risk = RISK_LEVELS.get(port, {}).get("risk", "Baixo")
    return RISK_META.get(risk, RISK_META["Baixo"])
