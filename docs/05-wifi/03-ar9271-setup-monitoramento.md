# Aula 3 (Módulo 05) — Setup do AR9271 e Monitoramento de Tráfego Wireless

[![📄 Baixar PDF desta aula](https://img.shields.io/badge/📄_Baixar-PDF_desta_aula-2b6cb0?style=for-the-badge)](03-ar9271-setup-monitoramento.pdf)

> **Regra importante:** tudo nesta aula só vale em laboratório próprio,
> rede própria ou ambiente explicitamente autorizado — nunca contra
> redes de terceiros. Monitorar tráfego de uma rede sem autorização é
> ilegal, mesmo que tecnicamente simples de fazer.

## 1. Por que o AR9271 é relevante aqui

O **Atheros AR9271** é o chipset de um adaptador Wi-Fi USB comum em
kits de estudo de segurança wireless, porque tem um recurso que a
maioria dos adaptadores Wi-Fi embutidos em notebooks **não tem por
padrão**: suporte robusto a **modo monitor**, necessário para capturar
tráfego Wi-Fi bruto (não só se conectar a uma rede como cliente comum).

## 2. Os três modos de uma interface Wi-Fi

- **Modo Managed (ou Station)**: o modo normal do dia a dia — o
  adaptador se conecta a **um** AP específico como cliente, igual seu
  celular se conectando ao Wi-Fi de casa.
- **Modo Master (AP)**: o adaptador **vira** um ponto de acesso,
  oferecendo rede para outros se conectarem (menos relevante para este
  módulo).
- **Modo Monitor**: o adaptador **não se conecta a nada** — ele fica
  "ouvindo" **todos** os frames 802.11 que passam pelo ar, no canal em
  que está sintonizado, de qualquer rede, sem precisar da senha delas
  (frames de gerenciamento como beacon/probe — Aula 1 — são enviados
  sem criptografia por design, então são visíveis mesmo sem estar
  associado). É o equivalente, no mundo Wi-Fi, ao que fizemos com
  Wireshark em modo promíscuo numa rede com fio (Módulo 04).

**Por que importa para segurança:** modo monitor é o que permite
**observar** o comportamento real da rede — quantos APs existem ao
redor, qual protocolo de segurança cada um anuncia (Aula 2), se há
deauth attacks acontecendo, etc. — sem precisar estar "dentro" de
nenhuma rede específica.

## 3. Verificando se o adaptador foi reconhecido

No Linux, depois de conectar o AR9271:

```bash
lsusb | grep -i atheros
```

Deve aparecer algo como `Atheros Communications, Inc. AR9271 802.11n`.
Se não aparecer nada, o adaptador não foi detectado pelo sistema — verifique
a conexão física antes de seguir.

```bash
dmesg | tail -30
```

Isso mostra as últimas mensagens do kernel — procure por linhas
mencionando `ath9k_htc` (o driver responsável pelo AR9271) confirmando
que o driver carregou e criou uma interface de rede.

## 4. Identificando a interface e o driver

```bash
iw dev
```

Lista as interfaces de rede wireless disponíveis (ex.: `wlan0`,
`wlan1`) e suas capacidades — inclusive quais **modos** cada uma suporta
(`managed`, `monitor`, `AP`, etc.), o que confirma se o adaptador
realmente oferece modo monitor no seu sistema.

```bash
ethtool -i wlan1 2>/dev/null || readlink -f /sys/class/net/wlan1/device/driver
```

Confirma qual driver está associado àquela interface — deve mostrar
`ath9k_htc` para o AR9271. O driver `ath9k_htc` (para o AR9271
especificamente) já vem incluído no kernel Linux das distribuições
modernas — normalmente não é preciso instalar nada manualmente, só
conectar o adaptador.

## 5. Colocando a interface em modo monitor

```bash
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
iw dev wlan1 info
```

O último comando deve mostrar `type monitor` na saída, confirmando a
mudança. (Ferramentas mais completas, como `airmon-ng` do pacote
aircrack-ng, automatizam essa sequência de comandos e também cuidam de
parar processos que podem interferir, como o gerenciador de rede padrão
do sistema — mas entender os comandos "crus" acima ajuda a compreender
o que está de fato acontecendo por baixo.)

## 6. Capturando e monitorando tráfego

Com a interface em modo monitor, o Wireshark (Módulo 04, Aula 2) pode
capturar diretamente dela, igual fizemos com uma interface com fio:

```bash
sudo wireshark -i wlan1 -k
```

Ou, para focar num canal específico primeiro (lembrando da Aula 1 —
monitor precisa estar sintonizado no canal certo):

```bash
sudo iw dev wlan1 set channel 6
```

Dentro do Wireshark, filtros relevantes para começar:

```
wlan.fc.type_subtype == 0x08     # beacon frames
wlan.fc.type_subtype == 0x0c     # deauthentication frames
wlan.ssid == "NomeDaRede"         # frames relacionados a um SSID específico
```

**Por que importa para segurança:** um volume anormalmente alto de
frames de **deauthentication** (subtipo `0x0c`) direcionados a um
cliente específico, vindos repetidamente, é o indicador clássico de um
ataque de deauth (Aula 2) em andamento — seja para capturar um
handshake, seja como negação de serviço simples contra aquele
dispositivo.

## 7. Voltando ao modo normal

Depois de terminar, sempre reverta a interface:

```bash
sudo ip link set wlan1 down
sudo iw dev wlan1 set type managed
sudo ip link set wlan1 up
```

## 8. Conectando tudo (Módulo 05 completo)

```
802.11 (Aula 1): SSID/BSSID/canal/frames — o vocabulário
WPA/WPA2/WPA3 (Aula 2): como a segurança realmente funciona, e onde
   ela é mais fraca (handshake WPA2 capturável)
AR9271 + modo monitor (esta aula): a ferramenta prática para
   OBSERVAR esse tráfego — beacons, probes, deauth — em laboratório
   próprio, encerrando o ciclo ENTENDER → MONITORAR → ANALISAR →
   DETECTAR → DEFENDER
```

## 9. Recapitulando o Módulo 05

- 802.11 = Wi-Fi; SSID (nome, falsificável) vs. BSSID (MAC do AP);
  canal/frequência; beacon (anúncio) e probe (busca ativa) como frames
  centrais.
- WEP/WPA obsoletos; WPA2 (AES) depende de senha forte por causa do
  handshake capturável; WPA3 (SAE) resiste a ataque offline.
- Modo monitor permite observar todo o tráfego 802.11 ao redor sem se
  conectar a nenhuma rede — base de qualquer análise wireless.
- AR9271 + `ath9k_htc` + `iw`/Wireshark é o kit prático para colocar
  tudo isso em prática, sempre em ambiente autorizado.

Módulo 05 concluído. 🎉

## Próximo módulo

**Módulo 06 — Python para Blue Team**: vamos parar de usar só
ferramentas prontas e começar a escrever nossas próprias — parsers de
log, analisadores de IP, extratores de IOC.

## Fontes recomendadas

- **Linux Kernel — documentação do driver `ath9k_htc`**: referência
  oficial do driver usado pelo AR9271.
  <https://wireless.docs.kernel.org/en/latest/en/users/drivers/ath9k_htc.html>
- **`iw` — documentação oficial (kernel.org wireless wiki)**: referência
  completa da ferramenta usada para configurar modo monitor.
  <https://wireless.docs.kernel.org/en/latest/en/users/documentation/iw.html>
- **Wireshark — "Wireless Capture Setup"**: guia oficial de captura em
  modo monitor. <https://wiki.wireshark.org/CaptureSetup/WLAN>
