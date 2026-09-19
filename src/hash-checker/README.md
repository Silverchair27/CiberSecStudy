# hash-checker

Calcula MD5, SHA1 e SHA256 de um arquivo (lendo em blocos, para lidar
bem com arquivos grandes) e, opcionalmente, compara com um hash
esperado ou com uma lista de hashes maliciosos conhecidos.

Acompanha a [Aula 4 do Módulo 06](../../docs/06-python/04-projeto-ioc-extractor-hash-checker.md).

## Uso

```bash
python3 hash_checker.py arquivo_exemplo.txt
python3 hash_checker.py arquivo_exemplo.txt --esperado <hash_md5_sha1_ou_sha256>
python3 hash_checker.py arquivo_exemplo.txt --lista hashes_maliciosos.txt
```

`arquivo_exemplo.txt` é um arquivo de teste incluído só para validar o
script sem precisar de uma amostra real.

## Como funciona

Lê o arquivo em blocos de 64 KB (em vez de carregar tudo de uma vez na
memória) e atualiza os três algoritmos de hash simultaneamente. Compara
o resultado (case-insensitive) contra `--esperado` e/ou contra cada
linha de `--lista`.
