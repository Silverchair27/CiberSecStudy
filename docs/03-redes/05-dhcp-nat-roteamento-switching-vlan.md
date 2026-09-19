# Aula 5 (Módulo 03) — DHCP, NAT, Roteamento, Switching e VLAN

## 1. DHCP — como um dispositivo recebe IP automaticamente

Sem DHCP, alguém precisaria configurar manualmente o IP de **cada**
dispositivo que entra em uma rede — impraticável em qualquer rede além
de um punhado de máquinas. **DHCP** (*Dynamic Host Configuration
Protocol*) automatiza isso: quando um dispositivo entra na rede, ele
"pergunta" por um IP, e um servidor DHCP (geralmente o próprio
roteador, em redes domésticas) responde atribuindo um IP disponível,
junto com outras informações (gateway, servidor DNS a usar).

Processo simplificado (conhecido pela sigla **DORA**):

```
Dispositivo → DISCOVER  → "alguém pode me dar um IP?" (broadcast)
Servidor    → OFFER     → "posso te oferecer 192.168.1.50"
Dispositivo → REQUEST   → "aceito esse IP"
Servidor    → ACK       → "confirmado, é seu por um tempo (lease)"
```

**Por que importa para segurança:** um servidor DHCP **falso**, colocado
por um atacante na rede local, pode responder mais rápido que o
legítimo e distribuir configuração maliciosa — por exemplo, definindo a
si mesmo como gateway/DNS, criando efetivamente um ataque de
**Man-in-the-Middle** parecido em efeito com o ARP Spoofing que vimos na
Aula 2. Isso é chamado de **DHCP Spoofing/Starvation**.

## 2. NAT — como várias máquinas compartilham um IP público

Lembra do problema de esgotamento do IPv4 (Aula 1)? **NAT** (*Network
Address Translation*) é uma das soluções práticas mais usadas: seu
roteador doméstico tem **um único IP público**, mas todos os
dispositivos da sua casa usam IPs **privados** internamente
(`192.168.x.x`). O roteador "traduz" o tráfego de saída, trocando o IP
privado de origem pelo seu próprio IP público — e faz o caminho inverso
quando a resposta volta.

```
[Seu notebook, 192.168.1.10] → NAT (roteador, IP público 203.0.113.5) → Internet
```

Do ponto de vista de um servidor na internet, todo o tráfego da sua casa
parece vir do **mesmo** IP público — o roteador é quem sabe, internamente,
para qual dispositivo devolver cada resposta.

**Por que importa para segurança:** NAT tem, como efeito colateral
(não como objetivo original), uma certa proteção: dispositivos atrás de
NAT não são diretamente alcançáveis pela internet sem uma configuração
explícita de **port forwarding** (redirecionamento de porta) — o que
reduz a superfície de ataque de uma rede doméstica típica. Também
significa que, ao investigar um log de um servidor externo, um único IP
pode representar **muitos** dispositivos diferentes atrás do mesmo NAT
(típico de redes corporativas grandes) — algo a considerar ao atribuir
uma ação a "um" usuário só pelo IP de origem.

## 3. Roteamento — como o tráfego encontra o caminho

**Roteamento** é o processo de decidir por qual caminho o tráfego deve
seguir para chegar ao destino, através de múltiplas redes. Roteadores
mantêm **tabelas de rota** que dizem "para chegar à rede X, envie pelo
caminho Y" — já vimos isso de leve no Módulo 01 (Aula 6) com
`ip route show`.

## 4. Switching — como o tráfego se move dentro da LAN

Enquanto roteadores conectam **redes diferentes**, um **switch** conecta
dispositivos **dentro da mesma LAN**, encaminhando tráfego Ethernet com
base no endereço **MAC** (Aula 1) — ele aprende quais dispositivos estão
em quais portas físicas e envia o tráfego só para onde precisa ir (mais
eficiente que simplesmente "gritar" para todo mundo).

## 5. VLAN — segmentando sem cabos separados

**VLAN** (*Virtual LAN*) permite dividir uma rede física em várias redes
lógicas **isoladas entre si**, mesmo usando o mesmo switch físico e os
mesmos cabos. Por exemplo: VLAN 10 para a rede corporativa, VLAN 20 para
convidados, VLAN 30 para servidores — cada uma isolada, mesmo
compartilhando a mesma infraestrutura física.

**Por que importa para segurança:** VLAN é uma das ferramentas mais
usadas na prática para implementar a **segmentação de rede** que já
mencionamos na Aula 1 (subnetting) — cada VLAN normalmente corresponde a
uma sub-rede diferente. Isso limita diretamente o **movimento lateral**:
mesmo que um atacante comprometa um dispositivo na VLAN de convidados,
ele não alcança diretamente a VLAN de servidores, a menos que exista uma
regra de roteamento/firewall explícita permitindo isso (o que, em um
ambiente bem projetado, normalmente não existe sem necessidade real).

## 6. Conectando tudo — o caminho completo de um pacote

```
1. Dispositivo entra na rede → DHCP atribui IP (Aula 5, seção 1)
2. Dispositivo quer falar com outro NA MESMA LAN → Switch encaminha
   via MAC (dentro da mesma VLAN/sub-rede)
3. Dispositivo quer falar com a INTERNET → Roteador decide o caminho
   (roteamento) → NAT troca o IP privado pelo IP público do roteador
4. Tráfego sai para a internet
```

E do lado defensivo: **VLAN** garante que dispositivos de segmentos
diferentes nem sequer se enxerguem diretamente na camada 2 (switching),
reforçando a segmentação que o **subnetting** já estabelece na camada 3
(roteamento).

## 7. Exercício prático

```bash
ip route show
```

Observe a rota padrão (geralmente marcada como `default via ...`) — é
literalmente o "roteador para o qual eu envio tudo que não sei como
alcançar diretamente", ou seja, seu gateway. Compare com o que
`ip addr show` te mostrou nas aulas anteriores.

## 8. Recapitulando

- DHCP automatiza a atribuição de IP; um servidor DHCP falso pode
  redirecionar tráfego (DHCP Spoofing).
- NAT permite que muitos dispositivos privados compartilhem um único IP
  público — reduz superfície de ataque, mas complica atribuição de ação
  a um IP só (redes grandes atrás de NAT).
- Roteamento move tráfego entre redes diferentes; switching move
  tráfego dentro da mesma LAN, via MAC.
- VLAN segmenta logicamente uma mesma infraestrutura física — a
  principal ferramenta prática de segmentação contra movimento lateral.

## Próxima aula (fecha o Módulo 03)

Firewall, proxy e VPN — os três controles que decidem "o que pode
passar" e "por onde" — junto com HTTP/HTTPS, TLS, cookies, sessões e
APIs, completando o fundamento de redes antes de entrarmos no Módulo 04
(Network Security de verdade).

## Fontes recomendadas

- **RFC 2131 — "Dynamic Host Configuration Protocol"**: especificação
  técnica oficial do DHCP. <https://www.rfc-editor.org/rfc/rfc2131>
- **RFC 3022 — "Traditional IP Network Address Translator (Traditional
  NAT)"**: especificação técnica oficial do NAT.
  <https://www.rfc-editor.org/rfc/rfc3022>
- **IEEE 802.1Q**: padrão técnico oficial que define VLAN (acesso pago;
  a Cisco e outros fabricantes têm boas documentações públicas
  explicando a implementação prática do padrão).
