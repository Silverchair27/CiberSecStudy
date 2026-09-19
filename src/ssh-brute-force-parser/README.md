# ssh-brute-force-parser

Parser em Python para logs SSH (`auth.log`/`secure`) que conta
tentativas de login falhadas por IP de origem e sinaliza IPs suspeitos
de brute force — com alerta extra quando um IP com muitas falhas
**também teve sucesso** logo depois (padrão de brute force bem-sucedido).

Acompanha a [Aula 3 do Módulo 06](../../docs/06-python/03-projeto-parser-de-log-ssh.md).

## Uso

```bash
python3 parser.py exemplo_auth.log --threshold 3
python3 parser.py exemplo_auth.log --threshold 3 --json relatorio.json
```

- `--threshold`: número mínimo de falhas para considerar um IP suspeito
  (padrão: 5).
- `--json`: opcional — salva o relatório completo em JSON.

`exemplo_auth.log` é um log de exemplo (dados fictícios) para testar o
script sem precisar de um log real.

## Como funciona

1. Lê o arquivo linha por linha.
2. Usa regex para casar linhas de `Failed password` (falha) e
   `Accepted password`/`Accepted publickey` (sucesso), extraindo IP,
   usuário e porta.
3. Conta falhas por IP com `collections.Counter`.
4. Reporta os IPs que atingiram o threshold, incluindo quais usuários
   foram tentados e se houve sucesso depois das falhas.
