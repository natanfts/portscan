# Mini Port Scanner

Um port scanner simples em Python.

## Uso
py scanner.py -i <IP> [-p porta_inicial-porta_final] [-t timeout] [-o arquivo]

Exemplo:
py scanner.py -i scanme.nmap.org -p 20-80 -t 2 -o resultado.txt

Da raiz do projeto, tambem funciona:
py -m portscanner.scanner -i scanme.nmap.org -p 20-80 -t 2 -o portscanner/results/resultado.txt

portscanner/
│── scanner.py              # Script principal (CLI com argparse + colorama)
│── requirements.txt        # Dependências (colorama, etc.)
│── README.md               # Explicação de uso
│
├── core/                   # Lógica principal
│   ├── __init__.py
│   ├── scanner.py          # Funções de scan (connect_ex, threading)
│   ├── utils.py            # Funções auxiliares (salvar resultados)
│   └── services.py         # Banner grabbing (captura de serviços)
│
├── results/                # Saída dos scans
│   └── resultado_scan.txt
│
└── tests/                  # Testes unitários
    ├── __init__.py
    └── test_scanner.py
