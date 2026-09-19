# Roadmap — Trilha de Cibersegurança (Zero → Profissional)

Trilha mestre. Marque os checkboxes conforme os tópicos forem
ensinados/praticados. Foco: **Blue Team 70% / Red Team 30%** — o Red Team
sempre a serviço da detecção ("como eu detectaria/investigaria/impediria
isso?").

Legenda: `[ ]` não iniciado · `[~]` em andamento · `[x]` concluído (teoria
+ prática/lab feita).

## 00. Fundamentos de computação — ✅ concluído
- [x] Hardware, CPU, RAM, armazenamento
- [x] Processos, threads, memória, arquivos
- [x] Sistemas operacionais, usuários, grupos, permissões
- [x] Serviços, cliente/servidor, virtualização, containers
- [x] Terminal e processos em background

## 01. Linux para Blue Team — ✅ concluído
- [x] Terminal, Bash, filesystem, permissões, usuários/grupos, sudo
- [x] Processos, serviços, systemd, cron
- [x] SSH
- [x] Logs: syslog, journalctl
- [x] Rede: sockets, conexões, firewall (pacotes/PCAP fica para o Módulo 04)
- [x] Comandos: ps, top, ss, ip, journalctl, grep, awk, sed, find, lsof etc.

## 02. Windows para Blue Team — ✅ concluído
- [x] Arquitetura, processos, serviços, usuários/grupos, Registry
- [x] PowerShell, Defender, Firewall, Task Scheduler, WMI
- [x] Event Viewer e Windows Event Logs (Event IDs essenciais)
- [x] Sysmon, PowerShell logging, process creation, logon events

## 03. Redes — fundamento central
- [x] LAN/WAN, Ethernet, MAC, IP (v4/v6), subnetting, ARP, ICMP
- [x] TCP/UDP, portas, DNS, DHCP, NAT, roteamento, switching, VLAN
- [ ] Firewall, proxy, VPN
- [ ] HTTP/HTTPS, TLS, certificados, cookies, sessões, APIs

## 04. Network Security
- [ ] Firewall, IDS/IPS, NIDS/NIPS, proxy, DNS security
- [ ] NetFlow, Zeek, Suricata, Wireshark
- [ ] Análise de PCAP (exercícios de laboratório)

## 05. Wi-Fi / Wireless Security (AR9271)
- [ ] 802.11, SSID/BSSID, canais, frames (beacon/probe), associação
- [ ] WPA/WPA2/WPA3
- [ ] Setup do adaptador AR9271 (driver, interface, modos)
- [ ] Monitoramento e análise de tráfego wireless (somente em lab próprio)

## 06. Python para Blue Team
- [ ] Fundamentos: variáveis, tipos, condições, loops, funções, arquivos, regex, JSON/CSV
- [ ] Projetos: parser de logs, analisador de IP, IOC extractor, hash checker

## 07. Git e GitHub (portfólio)
- [ ] Repositórios, commits, branches, PRs, issues, documentação

## 08. SOC — Security Operations Center
- [ ] Estrutura (N1/N2/N3), workflow, alert triage, escalation
- [ ] TP vs FP, severidade, priorização, case management, SLA
- [ ] Simulações de alertas (`ALERTA #001`, ...)

## 09. SIEM
- [ ] Coleta → parsing → normalização → enriquecimento → correlação → indexação → alertas
- [ ] Laboratório (Wazuh/Elastic/outro)

## 10. EDR
- [ ] Telemetria, process tree, command line, atividade de arquivo/registry/rede
- [ ] Investigações simuladas (PowerShell suspeito, persistência, C2)

## 11. Sysmon
- [ ] Eventos: process creation, network, file, registry, DNS, image load
- [ ] Exercício + detecção para cada evento relevante

## 12. Threat Intelligence
- [ ] IOC, IOA, TTP, threat actor, campanha, enriquecimento
- [ ] Análise de IP/domínio/URL/hash

## 13. MITRE ATT&CK
- [ ] Tática → Técnica → Procedimento → Evidência → Detecção → Resposta

## 14. Threat Hunting
- [ ] Hipótese, baseline, comportamento anômalo, pivot, timeline
- [ ] Exercícios guiados (sem resposta entregue de imediato)

## 15. Incident Response
- [ ] Preparation → Identification → Triage → Containment → Eradication → Recovery → Lessons Learned
- [ ] Incidentes simulados completos

## 16. Digital Forensics
- [ ] Timeline, filesystem, memória, artefatos Windows/Linux, browser artifacts

## 17. Red Team como apoio ao Blue Team
- [ ] PowerShell ofensivo, credential dumping, persistence — cada um com ataque → evidência → detecção → investigação → mitigação

## 18. Web Security
- [ ] HTTP/HTTPS, auth, sessões, APIs, TLS
- [ ] Vulnerabilidades (OWASP): conceito → lab → evidências → detecção → correção

## 19. Active Directory
- [ ] Domain, DC, OU, GPO, LDAP, Kerberos
- [ ] Ataques comuns em lab: credential attacks, lateral movement, privesc, persistence

## 20. Malware Analysis
- [ ] Fundamentos: trojan, worm, ransomware, loader, C2
- [ ] Static/dynamic analysis, sandbox, strings, hashes (ambiente isolado)

## 21. Detection Engineering
- [ ] Detection logic, correlação, false positives, tuning, alert fatigue
- [ ] Construção de regras: Sigma, KQL, SPL, EQL

---

**Fontes de referência prioritárias** (usar sempre que uma resposta
depender de versão/comportamento atual): MITRE ATT&CK, NIST, CISA, OWASP,
IETF/RFC, CVE/NVD, FIRST/CVSS, Sigma, e a documentação oficial de cada
ferramenta usada em laboratório. Ver detalhes de priorização em
[`../CLAUDE.md`](../CLAUDE.md#fontes-e-precisão).
