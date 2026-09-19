# Aula 1 (Módulo 02) — Arquitetura, processos, usuários e Registry no Windows

## 1. Do Linux para o Windows — o que muda e o que se repete

Boa notícia: os **conceitos** do Módulo 00 (CPU/RAM/disco, processos,
usuários, permissões, serviços) são universais — todo sistema operacional
os tem. O que muda é **como o Windows implementa e nomeia** cada um.
Vamos usar exatamente essa comparação para aprender mais rápido.

| Conceito | Linux | Windows |
|---|---|---|
| Identidade de usuário | UID | **SID** (Security Identifier) |
| Super usuário | `root` (UID 0) | **SYSTEM** (privilégio máximo do próprio SO) + grupo **Administrators** |
| Processo em 2º plano | daemon / systemd service | **Windows Service** |
| Configuração do sistema | arquivos texto em `/etc` | **Registry** (banco de dados hierárquico — ver seção 4) |
| Log do sistema | syslog / journald | **Windows Event Log** (Módulo 02, próximas aulas) |

## 2. Processos no Windows

Os mesmos campos que vimos no Linux continuam sendo o centro de tudo:
**PID**, **processo pai/filho**, **usuário dono** e **command line**.
A diferença é a ferramenta para olhar isso:

- **Gerenciador de Tarefas** (Ctrl+Shift+Esc) → aba "Detalhes": mostra
  PID e usuário, mas não a árvore pai/filho nem a command line completa
  por padrão.
- **PowerShell** (vamos aprofundar na próxima aula), com o comando:
  ```powershell
  Get-Process
  ```
- **Process Explorer** (ferramenta gratuita da própria Microsoft,
  parte do Sysinternals): mostra a árvore de processos completa,
  command line, e muito mais — é uma ferramenta que qualquer analista de
  Blue Team no Windows conhece bem.

**Por que importa para segurança:** o mesmo padrão que vimos no Linux se
repete — um processo com processo pai inesperado é suspeito. O exemplo
mais citado em toda formação de Blue Team em Windows:
`winword.exe` (Microsoft Word) tendo como **processo filho**
`powershell.exe` ou `cmd.exe`. Word, no uso normal, não abre PowerShell
sozinho — isso é o padrão clássico de um documento com **macro
maliciosa** executando um comando.

## 3. Usuários e privilégio no Windows

- Cada usuário tem um **SID** único, algo como `S-1-5-21-...-1001`.
- A conta **`SYSTEM`** roda com o privilégio mais alto do sistema
  operacional — mais alto até que um Administrador comum.
- O grupo **`Administrators`** equivale, em espírito, ao grupo `sudo`/
  `wheel` do Linux (Módulo 00, Aula 2): membros podem fazer alterações
  administrativas.
- O **UAC** (*User Account Control* — aquela janela que pede confirmação
  "Deseja permitir que este aplicativo faça alterações?") é o mecanismo
  do Windows que implementa, na prática, o princípio do menor privilégio:
  mesmo um usuário Administrador roda a maior parte do tempo com
  privilégio reduzido, e só "eleva" quando necessário e confirmado.

**Por que importa para segurança:** contornar ou burlar o UAC (técnica
chamada de **UAC Bypass**) é uma categoria inteira de técnicas
ofensivas catalogadas no MITRE ATT&CK, exatamente porque é o principal
obstáculo entre "rodar código como usuário comum" e "rodar código como
Administrador" em um Windows moderno.

## 4. O Registry (Registro do Windows)

O **Registry** é um banco de dados hierárquico que guarda quase toda a
configuração do Windows e dos programas instalados — o equivalente,
em espírito, aos arquivos de configuração em `/etc` no Linux, mas
estruturado como uma árvore de "chaves" (parecido com pastas) e
"valores" (parecido com arquivos dentro delas), acessível pelo
programa gráfico `regedit` ou via PowerShell.

As cinco raízes principais (chamadas de **hives**):

| Hive | Conteúdo |
|---|---|
| `HKEY_LOCAL_MACHINE` (HKLM) | configuração da máquina inteira (afeta todos os usuários) |
| `HKEY_CURRENT_USER` (HKCU) | configuração do usuário atualmente logado |
| `HKEY_USERS` | configuração de todos os usuários com perfil carregado |
| `HKEY_CLASSES_ROOT` | associações de tipo de arquivo, componentes COM |
| `HKEY_CURRENT_CONFIG` | perfil de hardware atual |

**Por que importa para segurança:** o Registry é, provavelmente, o
**principal mecanismo de persistência** no Windows. As chaves mais
citadas em toda formação de Blue Team são as chamadas **Run keys**:

```
HKLM\Software\Microsoft\Windows\CurrentVersion\Run
HKCU\Software\Microsoft\Windows\CurrentVersion\Run
```

Qualquer programa listado ali é iniciado **automaticamente toda vez que
o Windows liga** (ou que o usuário loga, no caso do HKCU) — exatamente a
definição de persistência que já vimos no Linux com `systemd`/`cron`
(Módulo 01, Aula 3). No MITRE ATT&CK, isso é catalogado como
**T1547.001 – Boot or Logon Autostart Execution: Registry Run Keys /
Startup Folder**. Verificar essas chaves é um dos primeiros passos em
praticamente toda investigação de um Windows suspeito de comprometimento.

## 5. Conectando com o Módulo 00

```
Windows
  ├─ Processos (mesmo PID/pai-filho/usuário/command line do Módulo 00)
  ├─ Usuários (SID) e Grupos (Administrators) → mesmo princípio de
  │    menor privilégio, reforçado pelo UAC
  ├─ Serviços (Windows Service) → mesma ideia de "roda sempre",
  │    persistência
  └─ Registry → configuração + um dos principais alvos de persistência
       (Run keys)
```

## 6. Exercício prático

Se você tiver acesso a um Windows agora, abra o PowerShell (não precisa
ser administrador) e rode:

```powershell
Get-Process | Sort-Object CPU -Descending | Select-Object -First 10
```

Isso lista os 10 processos que mais consumiram CPU — o equivalente
direto ao `top`/`ps` do Linux que vimos no Módulo 01.

Depois, para ver as Run keys mencionadas acima (não precisa mudar nada,
só olhar):

```powershell
Get-ItemProperty "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
```

Se vier vazio ou der erro dizendo que a chave não existe, isso também é
informação válida: significa que não há nada configurado para
autoexecução via essa chave específica no seu usuário — sua linha de
base.

## 7. Recapitulando

- Os conceitos do Módulo 00 (processo, usuário, permissão, serviço) são
  os mesmos — só muda a implementação: SID em vez de UID, `SYSTEM` em
  vez de `root`, Windows Service em vez de daemon.
- UAC é o mecanismo de menor privilégio do Windows moderno; contorná-lo
  é uma categoria própria de técnica ofensiva.
- Registry = configuração hierárquica do Windows; as **Run keys**
  (`...\CurrentVersion\Run`) são um dos principais mecanismos de
  persistência (MITRE T1547.001).

## Próxima aula

PowerShell — a "linha de comando" moderna do Windows, essencial tanto
para administração legítima quanto (infelizmente) para grande parte dos
ataques modernos contra Windows.

## Fontes recomendadas

- **Microsoft Learn — "Windows Registry"**: documentação oficial da
  estrutura de hives, chaves e valores.
  <https://learn.microsoft.com/troubleshoot/windows-server/performance/windows-registry-advanced-users>
- **MITRE ATT&CK — T1547.001 (Registry Run Keys / Startup Folder)**:
  técnica oficial de persistência via Registry.
  <https://attack.mitre.org/techniques/T1547/001/>
- **Sysinternals (Microsoft) — Process Explorer**: ferramenta oficial
  gratuita para visualizar árvore de processos no Windows.
  <https://learn.microsoft.com/sysinternals/downloads/process-explorer>
