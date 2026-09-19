# Aula 4 (Módulo 02) — Event Viewer e Windows Event Logs

[![📄 Baixar PDF desta aula](https://img.shields.io/badge/📄_Baixar-PDF_desta_aula-2b6cb0?style=for-the-badge)](04-event-viewer-event-ids.pdf)

## 1. O que é o Event Viewer (visão simples)

Assim como o Linux registra eventos em `/var/log` ou via `journalctl`
(Módulo 01, Aula 5), o Windows registra praticamente tudo relevante em
um sistema chamado **Windows Event Log**. O **Event Viewer** (`eventvwr.msc`)
é o programa gráfico para visualizar esses registros; o PowerShell
oferece o mesmo acesso via linha de comando.

Os três logs principais:

| Log | Conteúdo |
|---|---|
| **Application** | eventos gerados por aplicativos instalados |
| **System** | eventos do próprio sistema operacional (drivers, serviços, hardware) |
| **Security** | **o mais importante para Blue Team** — logon, logoff, uso de privilégio, alterações de política de auditoria, gerenciamento de contas |

## 2. Event ID — a "chave" de cada tipo de evento

Cada evento tem um número chamado **Event ID**, que identifica **o tipo**
de evento (independente dos detalhes específicos daquela ocorrência).
Pense nisso como um "código de categoria" padronizado pela própria
Microsoft — saber os IDs mais importantes de cor é uma das habilidades
mais valiosas (e mais cobradas em entrevista) de um SOC Analyst.

### Os Event IDs essenciais do log Security

| Event ID | Significado | Por que importa |
|---|---|---|
| **4624** | Logon bem-sucedido | Confirma quem logou, quando, de onde, e **como** (ver "Logon Type" abaixo) |
| **4625** | Falha de logon | Base de detecção de brute force — muitas 4625 seguidas do mesmo usuário/IP |
| **4672** | Logon com privilégios especiais (admin) | Confirma que uma conta administrativa foi usada — merece atenção redobrada |
| **4688** | Criação de novo processo | Equivalente ao que vimos com `ps`/árvore de processos no Linux — mostra processo, PID, e (se auditado) a command line completa |
| **4697** | Instalação de um novo serviço | Persistência via serviço (T1543, já visto no Módulo 00) |
| **4698** | Criação de tarefa agendada | Persistência via Task Scheduler (T1053.005, aula anterior) |
| **4720** | Criação de novo usuário local | Pode indicar uma conta criada por um atacante para persistência |
| **4732** | Usuário adicionado a um grupo local | Ex.: adicionado ao grupo `Administrators` — escalada de privilégio/persistência |

## 3. Logon Type — o detalhe que faz toda a diferença no 4624/4625

O Event ID 4624 (e 4625) sempre vem acompanhado de um campo **Logon
Type**, que diz **como** aquele logon aconteceu:

| Logon Type | Significado |
|---|---|
| **2** | Interativo — alguém logou fisicamente no teclado da máquina |
| **3** | Rede — acesso a um compartilhamento de arquivo/pasta pela rede |
| **4** | Batch — geralmente uma tarefa agendada |
| **5** | Serviço — um serviço do Windows iniciando com credenciais |
| **10** | RDP (Remote Desktop) — acesso remoto via área de trabalho remota |

**Por que importa para segurança:** o Logon Type é frequentemente **mais
importante que o próprio Event ID** para julgar se algo é normal.
Exemplo: uma conta de serviço fazendo Logon Type 5 é rotina; a mesma
conta de serviço fazendo Logon Type 10 (RDP interativo) seria muito
estranho — contas de serviço normalmente não "logam" via desktop remoto.
Esse tipo de raciocínio ("esse padrão de logon faz sentido para essa
conta?") é a base do Threat Hunting que veremos no Módulo 14.

## 4. Consultando via PowerShell

```powershell
Get-WinEvent -LogName Security -MaxEvents 20
Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4625} -MaxEvents 20
```

O `-FilterHashtable` filtra diretamente por log e Event ID — muito mais
rápido do que abrir o Event Viewer e navegar manualmente, especialmente
com milhares de eventos.

## 5. Por que auditoria precisa estar habilitada

Por padrão, o Windows **não gera todos** esses eventos — é preciso
habilitar as políticas de auditoria correspondentes (via **Group
Policy** ou `auditpol`). Por exemplo, o Event ID 4688 (criação de
processo) e a captura da **command line completa** dentro dele exigem
configuração explícita:

```
Configuração do Computador → Políticas → Configurações do Windows →
Configurações de Segurança → Configuração Avançada de Política de
Auditoria → Rastreamento Detalhado → Auditar Criação de Processo
```

**Por que importa para segurança:** essa é uma das lacunas mais comuns
em ambientes reais — muitas organizações descobrem, **durante** um
incidente, que a auditoria necessária nunca foi habilitada, e por isso
não existe nenhum registro do que o atacante fez. Verificar e configurar
a política de auditoria corretamente é, em si, um controle de segurança
preventivo, coberto pelo Módulo 21 (Detection Engineering) mais adiante.

## 6. Conectando com o resto do módulo

```
4624/4625 (logon)       → quem entrou, de onde, como (Logon Type)
4672                    → login com privilégio administrativo
4688                    → criação de processo (árvore de processos, Aula 1)
4697                    → novo serviço (persistência, Módulo 00 Aula 3)
4698                    → nova tarefa agendada (persistência, aula anterior)
4720/4732               → nova conta / conta adicionada a grupo (persistência/escalada)
```

Cada Event ID que vimos aqui conecta diretamente com um conceito que já
estudamos — não são números soltos, são o **registro em log** dos
mesmos comportamentos que já sabemos reconhecer como suspeitos.

## 7. Exercício prático

```powershell
Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4624} -MaxEvents 10 |
  Select-Object TimeCreated, Id, Message | Format-List
```

Procure, na mensagem completa de cada evento, o campo **Logon Type** e o
**nome de usuário**. Se não tiver um Windows disponível agora, ainda
vale a pena memorizar a tabela de Event IDs acima — ela vai reaparecer
constantemente nos próximos módulos (Sysmon, SIEM, Threat Hunting,
Incident Response).

## 8. Recapitulando

- Security log = o mais relevante para Blue Team; Event ID identifica o
  tipo de evento.
- 4624/4625 (logon/falha), 4672 (privilégio admin), 4688 (novo
  processo), 4697/4698 (novo serviço/tarefa — persistência), 4720/4732
  (nova conta/grupo) são os IDs essenciais para decorar.
- Logon Type (2=interativo, 3=rede, 4=batch, 5=serviço, 10=RDP) muitas
  vezes importa mais que o Event ID sozinho.
- Auditoria (política) precisa estar habilitada — não assuma que um
  evento "deveria" estar lá sem confirmar a configuração.

## Próxima aula (fecha o Módulo 02)

Sysmon, PowerShell logging e a diferença entre "o Windows já registra
por padrão" e "o que só aparece com telemetria adicional" — o
complemento que praticamente todo SOC profissional instala além dos
logs nativos.

## Fontes recomendadas

- **Microsoft Learn — "Audit Logon Events" e "4624/4625/4688..."**:
  documentação oficial de cada Event ID de segurança.
  <https://learn.microsoft.com/windows/security/threat-protection/auditing/event-4624>
- **Microsoft Learn — "Logon Type"**: tabela oficial completa dos tipos
  de logon. <https://learn.microsoft.com/windows/security/threat-protection/auditing/event-4624>
- **CISA / NSA — orientações de auditoria de Windows Event Log**:
  consulte cisa.gov para recomendações atualizadas de configuração de
  auditoria em ambientes corporativos.
