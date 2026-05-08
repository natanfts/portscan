# Portscan

Script em Python para localizar portas abertas em um alvo.

## Aviso de uso

Use apenas em ambientes locais, infraestrutura autorizada por voce ou no alvo de treino `scanme.nmap.org`.

## Estrutura do projeto

```text
portscanner/
|-- scanner.py
|-- requirements.txt
|-- README.md
|-- core/
|   |-- __init__.py
|   |-- scanner.py
|   |-- utils.py
|   `-- services.py
|-- results/
|   `-- resultado_scan.txt
`-- tests/
   |-- __init__.py
   `-- test_scanner.py
```

## Instalacao

1. Na raiz do projeto, instale as dependencias:

```bash
py -m pip install -r portscanner/requirements.txt
```

## Execucao

Comando recomendado na raiz do projeto:

```bash
py -m portscanner.scanner -i 127.0.0.1 -p 1-30
```

Voce tambem pode executar de dentro da pasta `portscanner`:

```bash
py scanner.py -i 127.0.0.1 -p 1-30
```

### Parametros

- `-i` ou `--ip`: IP ou hostname alvo (obrigatorio)
- `-p` ou `--ports`: intervalo no formato `inicio-fim` (padrao `1-1024`)
- `-t` ou `--timeout`: timeout em segundos por tentativa (padrao `1`)
- `-o` ou `--output`: arquivo de saida

### Exemplos

```bash
# localhost (scan completo comum)
py -m portscanner.scanner -i 127.0.0.1 -p 1-1024 -t 2

# salvar resultado em arquivo especifico
py -m portscanner.scanner -i 127.0.0.1 -p 1-1024 -t 5 -o portscanner/results/resultado_timeout5.txt

# ambiente de treino
py -m portscanner.scanner -i scanme.nmap.org -p 20-80 -t 2
```

### Erros comuns

- `monitor.py` nao existe neste projeto; o ponto de entrada e `portscanner/scanner.py`.
- A opcao `-n` nao faz parte do CLI.
- Para portas, use `-p` no formato `inicio-fim`, por exemplo `-p 1-30`.
