# CiberSecStudy

Diário de estudo e portfólio pessoal de cibersegurança, do absoluto zero
até nível profissional, com foco em **Blue Team / SOC / Detection
Engineering / Threat Hunting / Incident Response / Digital Forensics**
(70%), apoiado por fundamentos de **Red Team / Pentest** (30%) usados
apenas para entender o adversário e melhorar a detecção.

> Ataque → Evidência → Detecção → Investigação → Resposta → Correção →
> Prevenção.

## Objetivo

Desenvolver as competências necessárias para atuar como SOC Analyst
(N1/N2), Security Analyst, Blue Team Analyst, Detection Engineer, Threat
Hunter, Incident Responder ou Security Engineer — não apenas aprender a
usar ferramentas, mas a **pensar como um defensor**.

## Como este repositório está organizado

```
docs/          Aulas e teoria, organizadas por módulo (docs/ROADMAP.md = trilha completa)
lab/           Setup de laboratórios (VMs, Sysmon, Active Directory, rede)
src/           Código de projetos maiores
scripts/       Scripts utilitários e de automação
detections/    Regras de detecção (Sigma, KQL, SPL, EQL) documentadas
queries/       Queries de SIEM/EDR reutilizáveis
reports/       Relatórios de incidentes e investigações simuladas
screenshots/   Evidências visuais dos laboratórios
pcaps/         Capturas de tráfego para exercícios de análise
```

Veja [`docs/ROADMAP.md`](docs/ROADMAP.md) para a trilha completa (25
módulos) e o progresso atual.

## Metodologia

Cada tópico segue, sempre que possível, o ciclo:

**Teoria → Exemplo → Demonstração → Ataque simulado → Evidências →
Detecção → Investigação → Resposta → Correção → Projeto**

As instruções completas de como este repositório deve ser ensinado/
conduzido (persona de mentor, regras de fontes, formatos de simulação de
SOC/IR/Threat Hunting) estão em [`CLAUDE.md`](CLAUDE.md).

## Status

🟢 Módulo em andamento: **00 — Fundamentos de Computação** (Aula 3/5
concluída: serviços, cliente/servidor, virtualização e containers)
(ver [`docs/00-fundamentos/`](docs/00-fundamentos/)).
