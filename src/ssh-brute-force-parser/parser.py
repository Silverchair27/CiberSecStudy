#!/usr/bin/env python3
"""Parser de log SSH: conta tentativas de login falhadas por IP de origem
e reporta possíveis brute force (threshold configurável).

Uso:
    python3 parser.py caminho/para/auth.log
    python3 parser.py caminho/para/auth.log --threshold 3 --json saida.json
"""
import argparse
import json
import re
from collections import Counter

FAILED_RE = re.compile(
    r"Failed password for (?:invalid user )?(?P<usuario>\S+) from "
    r"(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) port (?P<porta>\d+)"
)
ACCEPTED_RE = re.compile(
    r"Accepted (?:password|publickey) for (?P<usuario>\S+) from "
    r"(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) port (?P<porta>\d+)"
)


def analisar_log(caminho):
    falhas_por_ip = Counter()
    usuarios_tentados_por_ip = {}
    sucessos = []

    with open(caminho, "r", encoding="utf-8", errors="ignore") as arquivo:
        for linha in arquivo:
            m_falha = FAILED_RE.search(linha)
            if m_falha:
                ip = m_falha.group("ip")
                usuario = m_falha.group("usuario")
                falhas_por_ip[ip] += 1
                usuarios_tentados_por_ip.setdefault(ip, set()).add(usuario)
                continue

            m_sucesso = ACCEPTED_RE.search(linha)
            if m_sucesso:
                sucessos.append(
                    {"ip": m_sucesso.group("ip"), "usuario": m_sucesso.group("usuario")}
                )

    return falhas_por_ip, usuarios_tentados_por_ip, sucessos


def montar_relatorio(falhas_por_ip, usuarios_tentados_por_ip, sucessos, threshold):
    suspeitos = []
    for ip, total_falhas in falhas_por_ip.most_common():
        if total_falhas >= threshold:
            suspeitos.append(
                {
                    "ip": ip,
                    "tentativas_falhas": total_falhas,
                    "usuarios_tentados": sorted(usuarios_tentados_por_ip.get(ip, [])),
                    "teve_sucesso_depois": any(s["ip"] == ip for s in sucessos),
                }
            )
    return {
        "threshold": threshold,
        "total_ips_com_falha": len(falhas_por_ip),
        "total_logins_bem_sucedidos": len(sucessos),
        "ips_suspeitos": suspeitos,
    }


def main():
    parser = argparse.ArgumentParser(description="Parser de log SSH para brute force")
    parser.add_argument("log", help="Caminho do arquivo de log (ex.: auth.log)")
    parser.add_argument(
        "--threshold",
        type=int,
        default=5,
        help="Número mínimo de falhas para considerar um IP suspeito (padrão: 5)",
    )
    parser.add_argument("--json", help="Se definido, salva o relatório neste arquivo JSON")
    args = parser.parse_args()

    falhas_por_ip, usuarios_tentados_por_ip, sucessos = analisar_log(args.log)
    relatorio = montar_relatorio(falhas_por_ip, usuarios_tentados_por_ip, sucessos, args.threshold)

    print(f"IPs com falha de login: {relatorio['total_ips_com_falha']}")
    print(f"Logins bem-sucedidos no log: {relatorio['total_logins_bem_sucedidos']}")
    print(f"\nIPs suspeitos (>= {args.threshold} falhas):")
    if not relatorio["ips_suspeitos"]:
        print("  nenhum")
    for item in relatorio["ips_suspeitos"]:
        alerta = " ⚠️  TEVE SUCESSO DEPOIS DAS FALHAS" if item["teve_sucesso_depois"] else ""
        print(
            f"  {item['ip']}: {item['tentativas_falhas']} falhas, "
            f"usuários tentados: {', '.join(item['usuarios_tentados'])}{alerta}"
        )

    if args.json:
        with open(args.json, "w", encoding="utf-8") as arquivo:
            json.dump(relatorio, arquivo, indent=2, ensure_ascii=False)
        print(f"\nRelatório salvo em {args.json}")


if __name__ == "__main__":
    main()
