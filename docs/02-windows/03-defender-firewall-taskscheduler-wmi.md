# Aula 3 (Módulo 02) — Windows Defender, Firewall, Task Scheduler e WMI

## 1. Windows Defender (Microsoft Defender Antivirus)

É o antivírus/antimalware **nativo** do Windows, instalado e ativo por
padrão desde o Windows 10/11 (a menos que outro antivírus o substitua).
Hoje ele é bem mais do que um antivírus clássico baseado em assinatura —
inclui proteção em tempo real, análise comportamental, e integração com
a nuvem da Microsoft para detecção de ameaças novas.

```powershell
Get-MpComputerStatus          # status atual do Defender
Get-MpThreatDetection          # ameaças detectadas recentemente
```

**Por que importa para segurança:** um dos primeiros passos de muitos
atacantes, depois de ganhar acesso inicial, é tentar **desativar ou
enfraquecer** o Defender — seja desligando a proteção em tempo real,
adicionando exclusões (pastas que o Defender passa a ignorar) ou
desativando componentes específicos. Isso é catalogado no MITRE ATT&CK
como **T1562.001 – Impair Defenses: Disable or Modify Tools**. Por isso,
monitorar **mudanças de configuração do Defender** (via Windows Event
Log, que veremos na próxima seção do módulo) é uma detecção de alto
valor — legítimos raramente desativam a proteção em produção, então essa
mudança é um forte indicador.

## 2. Windows Firewall

O firewall nativo do Windows funciona com o mesmo princípio geral que já
vimos no Módulo 01 (Aula 6) para Linux: regras que permitem ou bloqueiam
tráfego, com base em porta, programa, endereço IP, direção
(entrada/saída).

```powershell
Get-NetFirewallProfile             # perfis (Domain, Private, Public) e se estão ativos
Get-NetFirewallRule -Enabled True | Select-Object DisplayName, Direction, Action -First 10
```

**Por que importa para segurança:** assim como o Defender, uma regra de
firewall nova e incomum — especialmente uma que **permite** conexão de
entrada (inbound) para um programa/porta não padrão — é um padrão de
investigação comum. Alguns malwares criam suas próprias regras de
firewall para garantir que sua comunicação de rede não seja bloqueada.

## 3. Task Scheduler (Agendador de Tarefas)

É o equivalente direto do `cron` que vimos no Módulo 01, Aula 3: executa
programas/scripts automaticamente, em um horário definido ou disparado
por um evento (ex.: "ao logar", "ao iniciar o sistema").

```powershell
Get-ScheduledTask | Select-Object TaskName, State -First 15
```

**Por que importa para segurança:** exatamente como o `cron` no Linux,
criar uma tarefa agendada é um dos mecanismos de **persistência** mais
comuns no Windows — sobrevive a reboot, não depende de o usuário estar
logado. Catalogado no MITRE ATT&CK como **T1053.005 – Scheduled
Task/Job: Scheduled Task**. Tarefas com nome genérico/disfarçado
(imitando nomes de tarefas legítimas da Microsoft), apontando para um
executável em pasta incomum (`%TEMP%`, `%APPDATA%`), são um padrão
clássico de detecção.

## 4. WMI (Windows Management Instrumentation)

WMI é uma infraestrutura do Windows para **consultar e gerenciar**
praticamente qualquer aspecto do sistema — processos, serviços,
hardware, configuração de rede — de forma padronizada, inclusive
**remotamente** em outras máquinas da rede.

```powershell
Get-WmiObject Win32_Process | Select-Object Name, ProcessId -First 10
Get-WmiObject Win32_Service | Where-Object {$_.State -eq "Running"} | Select-Object Name -First 10
```

**Por que importa para segurança:** WMI é uma ferramenta administrativa
extremamente poderosa e, por isso, também é amplamente abusada por
atacantes — para: **executar comandos remotamente** em outras máquinas
da rede (uma forma de **movimento lateral**, que vamos aprofundar no
módulo de Active Directory), e para **persistência** avançada através de
**"WMI Event Subscriptions"** (assinaturas de eventos WMI que disparam a
execução de um comando automaticamente quando uma condição acontece —
ex.: toda vez que o sistema iniciar). É catalogado no MITRE ATT&CK como
**T1047 – Windows Management Instrumentation** (execução) e
**T1546.003 – Event Triggered Execution: WMI Event Subscription**
(persistência). É uma técnica considerada "avançada" justamente porque
WMI Event Subscriptions não aparecem como um arquivo comum no disco nem
como uma Run key no Registry — exigem ferramentas específicas para
detectar.

## 5. Conectando tudo

```
Defender    → detecta/bloqueia ameaças; ser DESATIVADO é, em si, um alerta (T1562.001)
Firewall    → controla tráfego de rede; regra nova inesperada é suspeita
Task Scheduler → agenda execução (equivalente ao cron); persistência (T1053.005)
WMI         → gerencia/consulta o sistema, inclusive remotamente; persistência
              avançada (T1546.003) e movimento lateral (T1047)
```

Repare no padrão que se repete módulo após módulo: **toda ferramenta
administrativa legítima e poderosa tende a também ser um vetor de
ataque**. Isso não é coincidência — é a razão pela qual "conhecer bem as
ferramentas normais do sistema" é tão importante para um defensor quanto
conhecer malware em si.

## 6. Exercício prático

```powershell
Get-MpComputerStatus | Select-Object AntivirusEnabled, RealTimeProtectionEnabled
Get-ScheduledTask | Where-Object {$_.State -eq "Ready"} | Select-Object TaskName -First 15
```

Observe se `AntivirusEnabled` e `RealTimeProtectionEnabled` estão como
`True` (esperado em uma máquina saudável). Na lista de tarefas
agendadas, veja se reconhece os nomes — a maioria será de componentes
legítimos do próprio Windows/Microsoft; o exercício mental é começar a
se perguntar "eu reconheço essa tarefa? Ela faz sentido existir?" — que é
exatamente a pergunta que baseline/threat hunting formaliza mais adiante
(Módulo 14).

## 7. Recapitulando

- Defender desativado/enfraquecido = alerta de alta prioridade
  (T1562.001).
- Regra de firewall nova permitindo entrada não padrão = suspeita.
- Task Scheduler = `cron` do Windows; persistência via tarefa agendada
  (T1053.005).
- WMI = ferramenta de gestão poderosa, abusada tanto para execução
  remota/movimento lateral (T1047) quanto persistência avançada via
  Event Subscription (T1546.003).

## Próxima aula

Event Viewer e Windows Event Logs — onde tudo isso (Defender, Firewall,
Task Scheduler, processos, logons) efetivamente **fica registrado**, e
como consultar isso com profundidade.

## Fontes recomendadas

- **Microsoft Learn — "Microsoft Defender Antivirus"**: documentação
  oficial. <https://learn.microsoft.com/defender-endpoint/microsoft-defender-antivirus-windows>
- **MITRE ATT&CK — T1562.001, T1053.005, T1047, T1546.003**: técnicas
  oficiais citadas nesta aula. <https://attack.mitre.org/techniques/T1562/001/>,
  <https://attack.mitre.org/techniques/T1053/005/>,
  <https://attack.mitre.org/techniques/T1047/>,
  <https://attack.mitre.org/techniques/T1546/003/>
- **Microsoft Learn — "WMI Reference"**: documentação técnica oficial de
  WMI. <https://learn.microsoft.com/windows/win32/wmisdk/wmi-reference>
