# Aula 1 (Módulo 05) — 802.11, SSID, BSSID, canais e frames

[![📄 Baixar PDF desta aula](https://img.shields.io/badge/📄_Baixar-PDF_desta_aula-2b6cb0?style=for-the-badge)](01-80211-ssid-bssid-canais-frames.pdf)

## 1. O que é 802.11 (visão simples)

**802.11** é o nome técnico (padrão do IEEE) para o que todo mundo chama
de "Wi-Fi". Assim como Ethernet (Módulo 03, Aula 1) é o padrão para rede
local **com fio**, 802.11 é o padrão para rede local **sem fio**. Os
conceitos de LAN, IP, TCP/UDP etc. que já vimos continuam valendo
exatamente iguais — o que muda é só a camada mais baixa: em vez de um
cabo, os dados viajam por **ondas de rádio**.

## 2. SSID e BSSID — dois "nomes" diferentes

- **SSID** (*Service Set Identifier*): o **nome da rede** que aparece
  quando você procura Wi-Fi no seu celular/notebook (ex.: "Casa_Nicolas",
  "Starbucks_WiFi"). É só um texto — pode ser duplicado por qualquer
  pessoa em qualquer lugar.
- **BSSID** (*Basic Service Set Identifier*): o **endereço MAC do
  roteador/ponto de acesso** (Access Point, ou **AP**) que está
  transmitindo aquele SSID. Diferente do SSID, o BSSID é único (é um
  endereço MAC, lembra da Aula 1 do Módulo 03?).

**Por que importa para segurança:** como o SSID é só um texto livre,
qualquer atacante pode criar um Access Point próprio usando o **mesmo
nome** de uma rede legítima (ex.: "Starbucks_WiFi" falso, ao lado do
verdadeiro) para enganar vítimas a se conectarem nele — chamado de
**Evil Twin** / Rogue Access Point. O BSSID (MAC do AP verdadeiro) é uma
forma de diferenciar o AP legítimo do falso, já que o MAC é bem mais
difícil de "parecer igual" por acaso (embora um atacante sofisticado
consiga clonar até o MAC — chamado de *MAC spoofing*, o que atrasa mas
não impede totalmente a detecção).

## 3. Canais e frequência

Wi-Fi opera em faixas de frequência específicas — principalmente
**2.4 GHz** (alcance maior, mais sujeita a interferência de outros
aparelhos) e **5 GHz** (mais rápida, alcance menor, menos interferência;
o 802.11ax/Wi-Fi 6E também usa 6 GHz). Cada faixa é dividida em
**canais** — sub-faixas específicas que um AP escolhe para transmitir,
para não conflitar tanto com APs vizinhos usando a mesma frequência
exata.

**Por que importa para segurança:** para **monitorar** tráfego Wi-Fi
(o que faremos nas próximas aulas com o adaptador AR9271), é preciso que
o adaptador esteja "ouvindo" no **mesmo canal** que a rede alvo está
usando — se você está no canal errado, simplesmente não vê nada daquela
rede. Ferramentas de scanning Wi-Fi (que veremos adiante) frequentemente
"pulam" entre canais (*channel hopping*) para conseguir uma visão geral
de tudo que existe ao redor.

## 4. Frames — a unidade básica de comunicação Wi-Fi

Assim como vimos "pacote" em redes com fio, no Wi-Fi a unidade básica se
chama **frame**. Os tipos mais relevantes para segurança:

### Beacon frame

O Access Point envia esses frames **constantemente** (várias vezes por
segundo), anunciando: "existo, meu SSID é tal, meu BSSID é tal, minhas
capacidades de segurança são tais (WPA2? WPA3?)". É assim que seu
celular consegue listar as redes disponíveis sem você precisar digitar
nada — ele só está "escutando" beacons.

### Probe request / probe response

- **Probe request**: um dispositivo (ex.: seu celular) pergunta
  ativamente "existe alguma rede com o nome X por aqui?" — muitas vezes
  perguntando por redes que ele **já conheceu antes** (ex.: a rede da
  sua casa), mesmo estando longe dela.
- **Probe response**: um AP que reconhece aquele SSID responde "sim, sou
  eu, aqui estão meus detalhes".

**Por que importa para segurança:** probe requests revelam, historicamente,
uma lista de redes que aquele dispositivo já se conectou antes — o que
já foi usado (e ainda é discutido) como uma forma de **rastrear
dispositivos/pessoas** mesmo sem estarem conectados a nada (só o
celular "perguntando" por redes conhecidas já vaza informação). Por
isso, sistemas operacionais modernos (Android, iOS) reduziram bastante
esse comportamento e passaram a usar **MAC aleatório** ao fazer essas
buscas — outro motivo pelo qual "MAC" sozinho, hoje em dia, é uma
identidade menos confiável do que costumava ser.

### Associação e autenticação

Depois que um dispositivo decide se conectar a um AP, acontece uma
sequência de frames de **autenticação** e **associação** — é aqui que
entra a segurança de verdade da rede (senha, criptografia), que
formalizamos na próxima aula (WPA/WPA2/WPA3).

## 5. Conectando com o que já vimos

```
802.11 = "Ethernet sem fio" — mesmos conceitos de LAN/IP/TCP por cima
SSID   = nome da rede (texto livre, pode ser falsificado — Evil Twin)
BSSID  = MAC do AP (mais confiável, mas ainda pode ser clonado)
Canal  = sub-faixa de frequência; monitoramento precisa "ouvir" no canal certo
Frames = beacon (anúncio constante), probe (pergunta ativa),
         autenticação/associação (conexão de fato)
```

## 6. Exercício prático (sem equipamento especial)

No seu celular ou notebook, abra a lista de redes Wi-Fi disponíveis.
Observe:

1. Quantas redes você vê, e se algum SSID se repete (dois APs anunciando
   o mesmo nome — pode ser legítimo, como um mesh de vários APs da mesma
   casa/empresa, ou pode ser suspeito, dependendo do contexto).
2. No Android/algumas ferramentas de notebook, é possível ver detalhes
   como o BSSID e o canal de cada rede — se seu dispositivo mostrar isso,
   compare o BSSID de duas redes com o mesmo SSID (se houver).

## 7. Recapitulando

- 802.11 é o Wi-Fi — mesma pilha de redes já estudada, só a camada mais
  baixa muda (rádio em vez de cabo).
- SSID = nome (falsificável); BSSID = MAC do AP (mais confiável, mas
  clonável).
- Canal define a frequência específica; monitoramento precisa estar no
  canal certo.
- Beacon = anúncio constante do AP; probe request/response = dispositivo
  perguntando ativamente por redes (historicamente um vazamento de
  privacidade, mitigado por MAC aleatório nos SOs modernos).

## Próxima aula

WPA, WPA2 e WPA3 — como a segurança de uma rede Wi-Fi realmente
funciona, e por que WEP e até WPA/WPA2 (em certas configurações) são
considerados fracos hoje em dia.

## Fontes recomendadas

- **IEEE 802.11 (visão geral oficial do padrão)**: o padrão completo é
  pago, mas o IEEE mantém uma página de visão geral pública.
  <https://www.ieee802.org/11/>
- **Wi-Fi Alliance — "Discover Wi-Fi"**: explicações oficiais sobre
  gerações do Wi-Fi (802.11n/ac/ax) e frequências.
  <https://www.wi-fi.org/discover-wi-fi>
