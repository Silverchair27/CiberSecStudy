# Aula 2 (Módulo 16) — Artefatos de Windows, Linux e Navegador

[![📄 Baixar PDF desta aula](https://img.shields.io/badge/📄_Baixar-PDF_desta_aula-2b6cb0?style=for-the-badge)](02-artefatos-windows-linux-navegador.pdf)

Cada sistema operacional (e o navegador, independente de qual SO)
guarda seus próprios "rastros" característicos — locais específicos
onde evidência de atividade fica registrada, além dos logs que já
estudamos (Módulo 02, Aula 4; Módulo 01, Aula 5).

## 1. Artefatos do Windows

### Prefetch

Toda vez que um programa é executado, o Windows cria/atualiza um
arquivo de **prefetch** (em `C:\Windows\Prefetch\`) para acelerar a
próxima execução — e, como efeito colateral extremamente útil para
forense, esse arquivo registra **quantas vezes** o programa foi
executado e **quando foi a última vez**.

**Por que importa:** mesmo que um atacante **delete** o executável
malicioso depois de usá-lo, o arquivo de prefetch muitas vezes
continua existindo — provando que aquele programa **foi executado**,
mesmo sem o arquivo original mais presente no disco.

### ShimCache / AmCache

Dois artefatos do Registry que registram, cada um à sua forma, **quais
executáveis já rodaram** no sistema — incluindo caminho completo,
tamanho, e (no caso do AmCache) até hash SHA1 do arquivo em alguns
casos. Como o Prefetch, sobrevive mesmo depois do executável original
ser removido.

### Jump Lists e LNK files

Arquivos de atalho (`.lnk`) e "listas de atividades recentes"
(*Jump Lists*) do Windows registram **quais arquivos foram abertos
recentemente**, por qual aplicação, e quando — útil para reconstruir o
que um usuário (ou um atacante usando a conta dele) esteve acessando.

### Registry — UserAssist e MRU

Além das Run keys (persistência, Módulo 02) e das chaves de
instalação de software, o Registry guarda chaves como **UserAssist**
(programas executados via Explorer, com contador e último horário) e
diversas listas **MRU** (*Most Recently Used* — arquivos recentes por
aplicação).

## 2. Artefatos do Linux

### Histórico de comandos

```bash
cat ~/.bash_history
```

Registra os comandos digitados no terminal (Módulo 00, Aula 4) — mas
**cuidado**: é um artefato **facilmente manipulável** — um atacante
sofisticado pode limpar ou desabilitar esse histórico (`unset
HISTFILE`, ou simplesmente apagando o arquivo). Ausência de histórico
suspeito, por si só, já é um dado (por que estaria vazio, se a conta
foi usada?).

### Logs de sistema (revisão)

Já vimos em detalhe no Módulo 01, Aula 5 — `/var/log/auth.log` (SSH,
sudo), `journalctl`. Vale lembrar: `logrotate` limita quanto tempo esses
dados ficam disponíveis localmente.

### Arquivos temporários e cron

`/tmp` (Módulo 01, Aula 1) e as entradas de `cron`/`/etc/cron.d`
(Módulo 01, Aula 3) continuam sendo pontos de checagem central em
qualquer investigação forense em Linux.

### Metadados de pacotes instalados

```bash
dpkg -l          # Debian/Ubuntu — lista pacotes instalados
rpm -qa          # RHEL/Fedora — equivalente
```

Útil para reconstruir: o que estava **instalado oficialmente** no
sistema, ajudando a identificar binários que **não** vieram de um
pacote conhecido (um forte sinal, combinado com localização incomum,
como vimos no Módulo 01, Aula 1, sobre `/tmp`).

## 3. Artefatos de navegador (qualquer SO)

### Histórico e downloads

Cada navegador guarda histórico de navegação e downloads geralmente em
um banco de dados **SQLite** local (arquivo `History`, no caso do
Chrome, por exemplo) — dá para consultar diretamente com ferramentas de
SQLite, mesmo sem abrir o navegador.

### Cache e cookies

O cache guarda cópias de páginas/recursos já visitados (às vezes
revelando conteúdo de páginas mesmo depois delas serem removidas do
servidor original); cookies (Módulo 03, Aula 7) revelam sessões — um
cookie de sessão roubado de um artefato de navegador é evidência
concreta de comprometimento de conta.

### Extensões instaladas

Extensões maliciosas de navegador são um vetor real de ataque (capazes
de roubar credenciais digitadas, injetar código em páginas) — listar
extensões instaladas e sua origem (loja oficial vs. instalação manual
"sideloaded") é uma checagem forense comum.

**Por que importa:** o navegador é, hoje, uma das superfícies de
ataque mais usadas — praticamente todo phishing (Módulo 02, Aula 5),
toda exfiltração via web (Módulo 03, Aula 7), toda interação inicial
com infraestrutura maliciosa passa, em algum momento, pelo navegador.

## 4. Conectando tudo — reconstruindo uma linha do tempo real

```
Prefetch/ShimCache (Windows)  → confirma execução, mesmo sem o arquivo
Bash history (Linux)          → confirma comandos, mas manipulável
Histórico de navegador        → confirma o que foi acessado/baixado
Logs de sistema (Módulos 01/02) → confirmam contexto (usuário, horário)
Sysmon (Módulo 11)            → confirma processo/rede/registry em
                                  detalhe, se estava instalado

TUDO combinado → super timeline (Aula 1) → reconstrução completa
```

## 5. Exercício prático

```bash
# Linux
ls -la ~/.bash_history
tail -20 ~/.bash_history
```
```powershell
# Windows
Get-ChildItem C:\Windows\Prefetch | Select-Object Name, LastWriteTime | Sort-Object LastWriteTime -Descending | Select-Object -First 10
```

Observe: você reconhece os programas mais recentemente executados
(Prefetch) ou os comandos mais recentes (bash_history)? Isso é
exatamente o tipo de checagem de linha de base que um analista forense
faz ao começar a investigar um sistema desconhecido.

## 6. Recapitulando o Módulo 16

- Windows: Prefetch, ShimCache/AmCache e Jump Lists/LNK sobrevivem
  mesmo depois do executável original ser deletado — provam execução
  passada.
- Linux: bash_history é útil mas facilmente manipulável; ausência
  suspeita também é um dado; logs (Módulo 01) e pacotes instalados
  complementam.
- Navegador: histórico/downloads (SQLite), cache, cookies e extensões
  são centrais, já que o navegador é uma das superfícies de ataque mais
  usadas hoje.
- A reconstrução real combina TODOS esses artefatos numa única
  timeline — nenhum artefato isolado é suficiente.

Módulo 16 concluído. 🎉

## Próximo módulo

**Módulo 17 — Red Team como Apoio ao Blue Team**: agora com toda essa
base defensiva sólida, aprofundamos técnicas ofensivas específicas —
sempre com a mesma pergunta central: como eu detectaria, investigaria e
impediria isso?

## Fontes recomendadas

- **Microsoft Learn — "Prefetch files"** e documentação oficial de
  artefatos do Windows: consulte learn.microsoft.com para referências
  técnicas atualizadas sobre cada artefato citado.
- **SANS — "Windows Forensic Analysis" poster** (referência
  comunitária/educacional amplamente usada como material de consulta
  rápida na indústria, não documentação oficial da Microsoft):
  disponível em sans.org.
- **Chrome/Firefox — documentação oficial de armazenamento de dados do
  usuário**: para detalhes técnicos atualizados sobre onde cada
  navegador guarda histórico/cookies em cada sistema operacional.
