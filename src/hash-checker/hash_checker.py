#!/usr/bin/env python3
"""Hash checker: calcula o hash (MD5/SHA1/SHA256) de um arquivo e,
opcionalmente, compara com um hash conhecido (ex.: de threat intel) ou
com uma lista de hashes maliciosos.

Uso:
    python3 hash_checker.py caminho/para/arquivo.exe
    python3 hash_checker.py caminho/para/arquivo.exe --esperado <hash>
    python3 hash_checker.py caminho/para/arquivo.exe --lista hashes_maliciosos.txt
"""
import argparse
import hashlib

CHUNK_SIZE = 65536  # lê o arquivo em blocos de 64 KB, para não estourar
                     # a memória com arquivos grandes


def calcular_hashes(caminho):
    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    sha256 = hashlib.sha256()

    with open(caminho, "rb") as arquivo:
        while True:
            bloco = arquivo.read(CHUNK_SIZE)
            if not bloco:
                break
            md5.update(bloco)
            sha1.update(bloco)
            sha256.update(bloco)

    return {
        "md5": md5.hexdigest(),
        "sha1": sha1.hexdigest(),
        "sha256": sha256.hexdigest(),
    }


def carregar_lista_maliciosos(caminho):
    with open(caminho, "r", encoding="utf-8") as arquivo:
        return {linha.strip().lower() for linha in arquivo if linha.strip()}


def main():
    parser = argparse.ArgumentParser(description="Calcula e verifica hashes de um arquivo")
    parser.add_argument("arquivo", help="Caminho do arquivo a verificar")
    parser.add_argument("--esperado", help="Hash esperado (MD5, SHA1 ou SHA256) para comparar")
    parser.add_argument("--lista", help="Arquivo com uma lista de hashes maliciosos conhecidos (um por linha)")
    args = parser.parse_args()

    hashes = calcular_hashes(args.arquivo)

    print(f"Arquivo: {args.arquivo}")
    for algoritmo, valor in hashes.items():
        print(f"  {algoritmo.upper()}: {valor}")

    if args.esperado:
        esperado = args.esperado.strip().lower()
        bateu = esperado in hashes.values()
        print(f"\nComparação com hash esperado: {'✅ CONFERE' if bateu else '❌ NÃO CONFERE'}")

    if args.lista:
        maliciosos = carregar_lista_maliciosos(args.lista)
        encontrados = [v for v in hashes.values() if v in maliciosos]
        if encontrados:
            print(f"\n⚠️  ALERTA: hash encontrado na lista de maliciosos conhecidos: {encontrados}")
        else:
            print("\nNenhum hash deste arquivo está na lista de maliciosos.")


if __name__ == "__main__":
    main()
