#!/usr/bin/env python3
"""IOC extractor: varre um texto (ou arquivo) e extrai indicadores de
comprometimento comuns — IPs, domínios, hashes (MD5/SHA1/SHA256) e
e-mails — sem depender de nenhuma API externa.

Uso:
    python3 extractor.py caminho/para/relatorio.txt
    python3 extractor.py caminho/para/relatorio.txt --json iocs.json
    echo "texto com 203.0.113.45" | python3 extractor.py -
"""
import argparse
import json
import re
import sys

PATTERNS = {
    "ips": re.compile(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"),
    "dominios": re.compile(
        r"\b(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+"
        r"(?:com|net|org|io|gov|edu|br|ru|cn|info|biz|xyz)\b",
        re.IGNORECASE,
    ),
    "emails": re.compile(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b"),
    "md5": re.compile(r"\b[a-fA-F0-9]{32}\b"),
    "sha1": re.compile(r"\b[a-fA-F0-9]{40}\b"),
    "sha256": re.compile(r"\b[a-fA-F0-9]{64}\b"),
}

# IPs privados (RFC 1918) são quase sempre ruído em relatórios de IOC —
# separamos para facilitar filtrar depois.
IP_PRIVADO_RE = re.compile(
    r"^(10\.|192\.168\.|172\.(1[6-9]|2\d|3[0-1])\.)"
)


def extrair_iocs(texto):
    resultado = {}
    for nome, padrao in PATTERNS.items():
        achados = sorted(set(padrao.findall(texto)))
        resultado[nome] = achados

    resultado["ips_publicos"] = [ip for ip in resultado["ips"] if not IP_PRIVADO_RE.match(ip)]
    resultado["ips_privados"] = [ip for ip in resultado["ips"] if IP_PRIVADO_RE.match(ip)]
    return resultado


def main():
    parser = argparse.ArgumentParser(description="Extrai IOCs (IPs, domínios, hashes, e-mails) de um texto")
    parser.add_argument("arquivo", help="Arquivo de entrada, ou '-' para ler da entrada padrão (stdin)")
    parser.add_argument("--json", help="Se definido, salva o resultado neste arquivo JSON")
    args = parser.parse_args()

    if args.arquivo == "-":
        texto = sys.stdin.read()
    else:
        with open(args.arquivo, "r", encoding="utf-8", errors="ignore") as f:
            texto = f.read()

    iocs = extrair_iocs(texto)

    for categoria, valores in iocs.items():
        print(f"\n{categoria} ({len(valores)}):")
        for v in valores:
            print(f"  {v}")

    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(iocs, f, indent=2, ensure_ascii=False)
        print(f"\nSalvo em {args.json}")


if __name__ == "__main__":
    main()
