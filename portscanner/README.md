# Mini Port Scanner

Port scanner em Python com CLI, menu interativo e barra de progresso.

Este README e uma referencia rapida do pacote `portscanner` e do uso do CLI. Para a documentacao completa do projeto, incluindo estrutura geral e dashboard web, consulte o README da raiz do repositorio.

## Uso rapido

Dentro da pasta portscanner:

```bash
py scanner.py -i <IP_OU_HOST> [-p inicio-fim] [--fast]
```

Da raiz do projeto:

```bash
py -m portscanner.scanner -i <IP_OU_HOST> [-p inicio-fim] [--fast]
```

Com `--fast`, o scan rapido inicia direto (sem passar pelo menu).

Depois da escolha do tipo de scan, o programa pergunta o formato do relatorio:

1. Salvar em .txt
2. Salvar em .json
3. Mostrar na tela e salvar em ambos

## Ambiente virtual (.venv)

Na raiz do projeto:

```bash
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Se precisar liberar scripts no PowerShell temporariamente:

```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## Menu de execucao

Ao iniciar, o programa mostra:

1. Scan rapido (portas comuns)
2. Scan completo (1-65535)
3. Scan personalizado (usa o intervalo passado em -p)

## Parametros

- -i, --ip: alvo do scan (obrigatorio)
- -p, --ports: intervalo no formato inicio-fim (exemplo: 20-80)
- --fast: ativa scan rapido (portas comuns)

## Exemplos

```bash
# menu interativo
py -m portscanner.scanner -i 127.0.0.1

# scan rapido
py -m portscanner.scanner -i 127.0.0.1 --fast

# scan personalizado (selecione opcao 3 no menu)
py -m portscanner.scanner -i scanme.nmap.org -p 20-80
```

## Saida

Resultados gravados por padrao em:

```text
results/resultado_scan.txt
results/resultado_scan.json
results/historico_scans.json
```

Cada relatorio inclui data/hora do scan, alvo escaneado, tipo de scan, portas abertas e total de portas abertas.

O dashboard web tambem mostra um historico de scans com data/hora, alvo e portas abertas, alem de status visuais por risco:

- ⚠️ Risco
- 🌐 Atencao
- ✅ OK

Ha um botao "Limpar historico" no dashboard para remover todos os registros salvos.

## Dependencias

- colorama
- tqdm

## Testes

```bash
python -m unittest discover -s portscanner/tests -v
```

## Observacoes

- O entrypoint do projeto e scanner.py (ou py -m portscanner.scanner na raiz).
- A opcao -n nao e reconhecida neste CLI.
- Para scan personalizado, use -p no formato inicio-fim.
