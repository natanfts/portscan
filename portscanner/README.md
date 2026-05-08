# Mini Port Scanner

Port scanner simples em Python com CLI.

## Uso rapido

Dentro da pasta `portscanner`:

```bash
py scanner.py -i <IP_OU_HOST> [-p inicio-fim] [-t timeout] [-o arquivo]
```

Da raiz do projeto:

```bash
py -m portscanner.scanner -i <IP_OU_HOST> [-p inicio-fim] [-t timeout] [-o arquivo]
```

## Parametros

- `-i`, `--ip`: alvo do scan (obrigatorio)
- `-p`, `--ports`: intervalo no formato `inicio-fim` (padrao `1-1024`)
- `-t`, `--timeout`: timeout em segundos (padrao `1`)
- `-o`, `--output`: caminho do arquivo de saida

## Exemplos

```bash
# localhost, portas 1-30
py -m portscanner.scanner -i 127.0.0.1 -p 1-30

# localhost com timeout maior e arquivo de saida
py -m portscanner.scanner -i 127.0.0.1 -p 1-1024 -t 5 -o portscanner/results/resultado_timeout5.txt

# alvo de treino controlado
py -m portscanner.scanner -i scanme.nmap.org -p 20-80 -t 2
```

## Observacoes

- O entrypoint do projeto e `scanner.py` (ou `py -m portscanner.scanner` na raiz).
- A opcao `-n` nao e reconhecida neste CLI.
- Para escanear portas, use sempre `-p` no formato `inicio-fim`.
