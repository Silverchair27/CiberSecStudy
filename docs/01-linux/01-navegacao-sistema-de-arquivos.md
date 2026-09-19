# Aula 1 (Módulo 01) — Navegação e Sistema de Arquivos

[![📄 Baixar PDF desta aula](https://img.shields.io/badge/📄_Baixar-PDF_desta_aula-2b6cb0?style=for-the-badge)](01-navegacao-sistema-de-arquivos.pdf)

## 1. Tudo é um arquivo (quase)

No Linux, quase tudo é representado como **arquivo**: seus documentos,
mas também dispositivos (um disco é `/dev/sda`), processos em execução
(cada processo tem uma pasta em `/proc/<PID>/`), e até a configuração de
rede. Isso é diferente do Windows, e é uma das razões pelas quais o
Linux é tão comum em servidores e ferramentas de segurança — dá para
"ler" praticamente qualquer coisa do sistema como se fosse um arquivo de
texto.

## 2. A árvore de diretórios (visão simples → técnica)

Simples: imagine uma pasta gigante chamada `/` (raiz), e dentro dela
todas as outras pastas do sistema — sem "C:\", sem letras de unidade
como no Windows. Tudo pendura a partir da raiz `/`.

```
/
├── home/        → pastas pessoais de cada usuário (ex.: /home/nicolas)
├── etc/         → arquivos de CONFIGURAÇÃO do sistema
├── var/         → dados que mudam com o tempo — INCLUINDO LOGS (/var/log)
├── bin/, usr/bin/ → programas/comandos executáveis
├── tmp/         → arquivos temporários (qualquer usuário pode escrever)
├── proc/        → informação "ao vivo" do kernel e dos processos
└── root/        → pasta pessoal do usuário root (não confundir com /)
```

**Por que importa para segurança:** três dessas pastas são praticamente
"lugares de investigação" fixos:

- **`/etc`** → onde ficam arquivos de configuração sensíveis, como
  `/etc/passwd` (lista de usuários) e `/etc/shadow` (hashes de senha,
  lembra da Aula 2 do Módulo 00?). Modificações inesperadas aqui são um
  sinal de alerta.
- **`/var/log`** → onde a maioria dos logs do sistema fica guardada.
  É provavelmente a pasta mais visitada por um analista Blue Team em um
  host Linux.
- **`/tmp`** → como qualquer usuário pode escrever ali, é um dos lugares
  favoritos de atacantes para soltar arquivos maliciosos temporariamente.
  Um executável rodando a partir de `/tmp` é, sozinho, um padrão que
  costuma virar regra de detecção.

## 3. Caminho absoluto vs. relativo

- **Caminho absoluto**: começa na raiz `/`, funciona de qualquer lugar.
  Ex.: `/var/log/auth.log`.
- **Caminho relativo**: parte de onde você está agora no terminal.
  Ex.: se você já está em `/var/log`, pode digitar só `auth.log`.

## 4. Comandos essenciais de navegação

| Comando | O que faz | Por que um analista usa |
|---|---|---|
| `pwd` | mostra em qual pasta você está agora (*print working directory*) | confirmar contexto antes de rodar qualquer outro comando |
| `ls` | lista arquivos/pastas | ver o que existe em um diretório suspeito |
| `ls -la` | lista **tudo**, inclusive arquivos ocultos (que começam com `.`), com detalhes (permissões, dono, data) | arquivos ocultos são um truque comum para esconder algo — `ls` sozinho não mostra |
| `cd <pasta>` | muda de pasta (*change directory*) | navegar até onde a evidência está |
| `cd ..` | sobe um nível na árvore | voltar |
| `cd ~` ou só `cd` | vai para sua pasta pessoal (`/home/seu_usuario`) | |
| `cat <arquivo>` | mostra o conteúdo inteiro de um arquivo de texto na tela | ler um log pequeno rapidamente |
| `less <arquivo>` | mostra o conteúdo **paginado** (navega com setas, `q` para sair) | ler um log grande sem lotar a tela |
| `file <arquivo>` | diz **que tipo** de arquivo é aquilo, mesmo sem extensão | um atacante pode renomear `malware.exe` para `foto.jpg` — `file` revela o tipo real pelo conteúdo, não pelo nome |

## 5. Exemplo prático guiado

```bash
pwd                     # onde estou?
ls -la                  # o que tem aqui, incluindo ocultos?
cd /var/log             # vou para a pasta de logs
ls -la                  # quais arquivos de log existem?
file auth.log 2>/dev/null || file syslog 2>/dev/null   # que tipo de arquivo é esse log?
less auth.log 2>/dev/null || less syslog 2>/dev/null   # olhar o conteúdo, paginado
```
(Aperte `q` para sair do `less`. Nomes de arquivo de log variam por
distribuição — em Ubuntu/Debian costuma ser `auth.log`, em
RHEL/Fedora/CentOS costuma ser `secure`, dentro de `/var/log`.)

## 6. Conectando com o Módulo 00

```
Sistema de arquivos = onde ficam as EVIDÊNCIAS (Aula 1: onde malware pode
gravar arquivo; Aula 2: onde ficam as permissões; Aula 3: onde serviços
guardam configuração)
```

`/etc/passwd`, `/etc/shadow` e `/var/log` não são pastas aleatórias — elas
existem exatamente por causa dos conceitos que já vimos (usuários,
permissões, logs de sistema).

## 7. Exercício prático

```bash
cd /tmp
pwd
ls -la
touch teste_aula.txt
ls -la
file teste_aula.txt
rm teste_aula.txt
```

Você acabou de: navegar até `/tmp` (a pasta que mencionamos como alvo
comum de atacantes), criar um arquivo vazio (`touch`), confirmar que ele
apareceu (`ls -la`), checar seu tipo (`file` — deve dizer algo como
"empty"), e removê-lo (`rm`). Isso é literalmente o ciclo básico que um
processo malicioso faria ao "soltar" um arquivo em `/tmp` — só que aqui
foi você, de propósito, para aprender.

## 8. Recapitulando

- Linux organiza tudo em uma única árvore a partir de `/` — sem letras de
  unidade.
- `/etc` = configuração, `/var/log` = logs, `/tmp` = escrita livre (alvo
  comum de ataque).
- `pwd`, `ls -la`, `cd`, `cat`, `less`, `file` são a base para navegar e
  inspecionar qualquer sistema Linux durante uma investigação.

## Próxima aula

Permissões na prática: `chmod`, `chown` e `sudo` — como ler, interpretar
e alterar as permissões `rwx` que vimos na teoria (Módulo 00, Aula 2).

## Fontes recomendadas

- **Linux Foundation — "Filesystem Hierarchy Standard (FHS)"**: padrão
  oficial que define o propósito de cada pasta (`/etc`, `/var`, `/tmp`
  etc.). <https://refspecs.linuxfoundation.org/FHS_3.0/fhs-3.0.html>
- **Linux man-pages — `hier(7)`**: referência oficial e resumida da
  hierarquia de diretórios. <https://man7.org/linux/man-pages/man7/hier.7.html>
