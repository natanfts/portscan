# Net Scan (Portscan)

Script em Python para localizar portas abertas em um alvo, com menu interativo e barra de progresso.

O dashboard web agora usa a marca Net Scan, com paleta visual cyber (fundo escuro com tons neon verde/ciano) e suporte a logo no cabecalho.

Este e o README principal do projeto. Aqui fica a documentacao geral: instalacao, estrutura, execucao via CLI e dashboard web, testes e funcionamento dos relatorios.

## Aviso de uso

Use apenas em ambientes locais, infraestrutura autorizada por voce ou no alvo de treino scanme.nmap.org.

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

Na raiz do projeto:

```bash
python -m pip install -r portscanner/requirements.txt
```

## Ambiente virtual (.venv)

Criar (se ainda nao existir):

```bash
python -m venv .venv
```

Ativar no PowerShell:

```bash
.\.venv\Scripts\Activate.ps1
```

Se o PowerShell bloquear scripts temporariamente:

```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Desativar:

```bash
deactivate
```

## Execucao

### Via CLI (linha de comando)

Da raiz do projeto:

```bash
python -m portscanner.scanner -i 127.0.0.1
```

De dentro da pasta portscanner:

```bash
python scanner.py -i 127.0.0.1
```

### Via Web Dashboard

Na raiz do projeto:

```bash
python app.py
```

Depois acesse no navegador: `http://127.0.0.1:5000`

### Identidade visual do dashboard

- Nome exibido: Net Scan
- Logo no cabecalho: `static/img/netscan-logo.png`
- Caso a logo nao exista, o titulo continua aparecendo normalmente.

No dashboard web, cada porta recebe um status visual:

- ⚠️ Risco: portas com maior exposicao
- 🌐 Atenção: servicos que exigem revisao
- ✅ OK: exposicao considerada menor

Ao executar via CLI, o programa abre um menu:

1. Scan rapido (portas comuns)
2. Scan completo (1-65535)
3. Scan personalizado (usa o intervalo informado em -p)

Observacao: com `--fast`, o scanner entra direto no modo rapido sem mostrar o menu.

Depois da escolha do tipo de scan, o programa pergunta o formato do relatorio:

1. Salvar em .txt
2. Salvar em .json
3. Mostrar na tela e salvar em ambos

## Parametros do CLI

- -i, --ip: IP ou hostname alvo (obrigatorio)
- -p, --ports: intervalo no formato inicio-fim (exemplo: 20-80)
- --fast: forca scan rapido (portas comuns)

Observacao: no fluxo atual, a escolha do menu define o tipo de scan. O parametro -p e usado no scan personalizado (opcao 3).

## Exemplos

```bash
# inicia e permite escolher no menu
python -m portscanner.scanner -i 127.0.0.1

# scan rapido com --fast
python -m portscanner.scanner -i 127.0.0.1 --fast

# scan personalizado (escolha opcao 3 no menu)
python -m portscanner.scanner -i scanme.nmap.org -p 20-80
```

## Saida

O resultado do scan pode ser salvo em:

```text
results/resultado_scan.txt
results/resultado_scan.json
```

Os relatorios agora incluem:

- data/hora do scan
- alvo escaneado
- tipo de scan
- portas abertas
- total de portas abertas

O projeto tambem mantem um historico de scans em:

```text
results/historico_scans.json
```

Cada entrada do historico armazena data/hora, alvo e lista de portas abertas.

No dashboard web, existe um botao "Limpar historico" para zerar esse registro quando necessario.

## Dependencias

- colorama
- tqdm (opcional; sem ele o scan continua funcionando, apenas sem barra de progresso)
- flask (para dashboard web)

## Testes

Na raiz do projeto:

```bash
python -m unittest discover -s portscanner/tests -v
```

## Saida do CLI

A saída é formatada em tabela com analise de risco para cada porta:

```
=== Relatorio Final ===

Data/Hora: 2026-05-13T19:20:00
Alvo: 127.0.0.1
Tipo de Scan: fast
Total de portas abertas: 3

Porta    Servico      Status   Analise                                                     
------------------------------------------------------------------------------------------
22       SSH          open     SSH aberto -> possivel acesso remoto Linux                   
80       HTTP         open     HTTP aberto -> servidor web detectado                        
3306     MySQL        open     Banco de dados MySQL exposto                                
```

## Erros comuns

- monitor.py nao existe neste projeto; o ponto de entrada e portscanner/scanner.py.
- A opcao -n nao faz parte do CLI.
- Para scan personalizado, use -p no formato inicio-fim (exemplo: -p 1-30).
- Projeto padronizado para usar apenas o ambiente virtual `.venv`.
