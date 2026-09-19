# ioc-extractor

Extrai indicadores de comprometimento (IOCs) comuns de qualquer texto —
IPs (separando público vs. privado), domínios, e-mails, e hashes
MD5/SHA1/SHA256 — usando só regex, sem depender de nenhuma API externa.

Acompanha a [Aula 4 do Módulo 06](../../docs/06-python/04-projeto-ioc-extractor-hash-checker.md).

## Uso

```bash
python3 extractor.py exemplo_relatorio.txt
python3 extractor.py exemplo_relatorio.txt --json iocs.json
echo "conexão suspeita para 203.0.113.45" | python3 extractor.py -
```

`exemplo_relatorio.txt` é um relatório de incidente fictício, usado só
para testar o script.
