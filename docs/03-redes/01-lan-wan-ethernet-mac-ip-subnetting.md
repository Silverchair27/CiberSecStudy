# Aula 1 (Módulo 03) — LAN, WAN, Ethernet, MAC, IP e Subnetting

[![📄 Baixar PDF desta aula](https://img.shields.io/badge/📄_Baixar-PDF_desta_aula-2b6cb0?style=for-the-badge)](01-lan-wan-ethernet-mac-ip-subnetting.pdf)

## 1. LAN e WAN (visão simples)

- **LAN** (*Local Area Network*): uma rede pequena, geograficamente
  limitada — sua casa, um escritório, um prédio. Os dispositivos se
  comunicam diretamente entre si, sem passar pela internet.
- **WAN** (*Wide Area Network*): uma rede que conecta LANs distantes
  entre si — a própria **internet** é a maior WAN que existe, uma "rede
  de redes".

```
[Seu notebook] ── LAN (rede de casa) ── [Roteador] ── WAN (internet) ── [Servidor do site]
```

**Por que importa para segurança:** essa fronteira entre LAN e WAN é
exatamente onde ficam a maioria dos controles de segurança de perímetro
(firewall, que vamos formalizar mais adiante neste módulo). Saber "isso
é tráfego interno (dentro da LAN) ou está cruzando para a internet
(WAN)?" é uma das primeiras perguntas em qualquer investigação de rede.

## 2. Ethernet e endereço MAC

**Ethernet** é a tecnologia mais comum de rede local com fio (também dá
nome ao formato dos "pacotes" trocados na LAN). Todo dispositivo com
interface de rede (placa de rede, Wi-Fi) tem um identificador único
chamado **endereço MAC** (*Media Access Control*), gravado de fábrica na
própria placa — algo como `00:1A:2B:3C:4D:5E`.

**Por que importa para segurança:** o endereço MAC identifica o
**dispositivo físico** dentro da rede local (diferente do IP, que veremos
a seguir, e que pode mudar). Ataques como **ARP Spoofing** (que veremos
na próxima aula) abusam exatamente da forma como MAC e IP se associam
dentro de uma LAN. Além disso, dispositivos desconhecidos aparecendo na
rede (MAC nunca visto antes) é um sinal clássico de monitoramento de
rede — assunto que retomamos no Módulo 04.

## 3. Endereço IP

Enquanto o MAC identifica um dispositivo **dentro da rede local**, o
**endereço IP** (*Internet Protocol*) identifica um dispositivo de forma
que ele possa ser **roteado** através de redes diferentes — inclusive
pela internet inteira. É o "endereço postal" de cada máquina.

### IPv4

Formato mais comum hoje: quatro números de 0 a 255, separados por ponto:

```
192.168.1.10
```

Cada um desses números é 8 bits (1 byte) — por isso o limite é 255
(2⁸ - 1). No total, IPv4 tem 32 bits, o que dá cerca de 4,3 bilhões de
endereços possíveis — um número que **já se esgotou** frente ao tamanho
da internet atual (um dos motivos por trás do NAT, que veremos adiante,
e da existência do IPv6).

### IPv6

Criado justamente para resolver o esgotamento do IPv4: usa 128 bits,
representado em hexadecimal, como:

```
2001:0db8:85a3:0000:0000:8a2e:0370:7334
```

Ainda é menos usado que IPv4 no dia a dia de investigação (a maioria dos
logs e ferramentas que você vai encontrar no início da carreira ainda
gira em torno de IPv4), mas sua adoção cresce — vale reconhecer o
formato.

### IP público vs. IP privado

- **IP privado**: só é válido dentro de uma rede local — faixas
  reservadas especificamente para isso: `10.0.0.0/8`,
  `172.16.0.0/12`, `192.168.0.0/16` (a notação `/8`, `/12`, `/16` é o
  **prefixo de rede**, que vamos entender já na próxima seção).
- **IP público**: único no mundo inteiro, roteável pela internet.

**Por que importa para segurança:** ver um IP privado (`192.168.x.x`,
`10.x.x.x`) em um log de conexão significa que a comunicação foi
**dentro da rede local**; ver um IP público desconhecido significa
comunicação com a internet — um dado central para decidir se uma conexão
é potencialmente maliciosa (ex.: comunicação com C2, que mencionamos no
Módulo 00, Aula 3).

## 4. Subnetting (dividindo uma rede em sub-redes)

**Subnetting** é o processo de dividir um bloco de endereços IP em
pedaços menores (sub-redes), cada um isolado dos outros por padrão
(a não ser que haja roteamento explícito entre eles). Isso é feito com
uma **máscara de sub-rede** (ou notação CIDR, com `/`).

Exemplo: `192.168.1.0/24` significa que os primeiros 24 bits (os três
primeiros números: `192.168.1`) identificam a **rede**, e os últimos 8
bits (o último número, de `0` a `255`) identificam o **host** dentro
dessa rede — ou seja, essa sub-rede vai de `192.168.1.0` até
`192.168.1.255` (256 endereços, dos quais 254 são utilizáveis por
dispositivos — o primeiro e o último têm usos reservados).

```
192.168.1.0/24
└── 192.168.1.1   até   192.168.1.254   (dispositivos)
    192.168.1.0    = endereço de rede (reservado)
    192.168.1.255  = endereço de broadcast (reservado)
```

Prefixos comuns e seu tamanho:

| Prefixo | Máscara | Hosts utilizáveis (aprox.) |
|---|---|---|
| `/24` | `255.255.255.0` | 254 |
| `/16` | `255.255.0.0` | ~65 mil |
| `/8` | `255.0.0.0` | ~16,7 milhões |

**Por que importa para segurança:** subnetting é a base da
**segmentação de rede** — separar, por exemplo, a rede de convidados da
rede corporativa, ou separar servidores de produção da rede de usuários
comuns. Segmentação bem feita é uma das defesas mais eficazes contra
**movimento lateral** (um atacante que compromete uma máquina não
consegue automaticamente alcançar tudo mais, se as sub-redes forem
isoladas por firewall) — vamos aprofundar isso no Módulo 04 e no módulo
de Active Directory.

## 5. Conectando tudo

```
LAN (rede local)  ──┬── Ethernet + MAC (identifica dispositivo na LAN)
                     └── IP (identifica e roteia, inclusive fora da LAN)
                              │
                     Subnetting (/24, /16...) → divide em sub-redes →
                     base da segmentação de segurança (limita movimento
                     lateral)
                              │
WAN (internet) ── IP público, roteado globalmente
```

## 6. Exercício prático

Se você tiver um terminal (Linux, com o `ip` que já vimos no Módulo 01):

```bash
ip addr show
```

Observe seu próprio IP e o prefixo associado (algo como
`192.168.1.15/24`, aparecendo depois do IP na saída). Pergunte-se: esse
é um IP privado ou público (compare com as faixas reservadas que vimos
na seção 3)? Qual é o prefixo (`/24`? outro?) e o que isso te diz sobre
o tamanho da sua rede local?

## 7. Recapitulando

- LAN = rede local; WAN = rede de longa distância (a internet é a maior
  WAN).
- MAC identifica o dispositivo físico dentro da LAN; IP identifica e
  permite rotear, inclusive fora da LAN.
- IP privado (`10.x`, `172.16-31.x`, `192.168.x`) só existe dentro de
  uma rede local; IP público é único e roteável globalmente.
- Subnetting (`/24`, `/16`...) divide uma rede em sub-redes — base da
  segmentação, uma das defesas mais eficazes contra movimento lateral.

## Próxima aula

ARP e ICMP — como um dispositivo descobre o endereço MAC de outro dentro
da LAN (ARP), e como funciona o `ping` (ICMP) — incluindo o ataque
clássico de **ARP Spoofing** que já mencionamos aqui.

## Fontes recomendadas

- **RFC 791 — "Internet Protocol"**: especificação técnica oficial
  (IETF) do IPv4. <https://www.rfc-editor.org/rfc/rfc791>
- **RFC 8200 — "Internet Protocol, Version 6 (IPv6) Specification"**:
  especificação oficial do IPv6. <https://www.rfc-editor.org/rfc/rfc8200>
- **RFC 1918 — "Address Allocation for Private Internets"**: define
  oficialmente as faixas de IP privado (`10.0.0.0/8`, `172.16.0.0/12`,
  `192.168.0.0/16`). <https://www.rfc-editor.org/rfc/rfc1918>
