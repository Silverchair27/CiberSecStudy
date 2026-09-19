# Aula 1 (Módulo 16) — Timeline, Sistema de Arquivos e Memória

[![📄 Baixar PDF desta aula](https://img.shields.io/badge/📄_Baixar-PDF_desta_aula-2b6cb0?style=for-the-badge)](01-timeline-filesystem-memoria.pdf)

## 1. Forense digital vs. o que já fizemos

Diferente de Threat Hunting (busca ativa) ou Incident Response
(processo de resposta), **Digital Forensics** é sobre **reconstruir com
rigor** exatamente o que aconteceu em um sistema — muitas vezes com um
padrão de cuidado alto o suficiente para servir como evidência formal
(inclusive legal, em investigações que chegam a esse nível). O princípio
central: **nunca altere a evidência original** — trabalhe sempre sobre
uma cópia/imagem, preservando a fonte intacta.

## 2. Timeline — a espinha dorsal de qualquer investigação forense

Já construímos timelines informalmente em quase todo módulo (Módulo
11, Aula 2: a cadeia de Event IDs em ordem cronológica). Forense formal
leva isso adiante: uma **super timeline** — todos os timestamps
disponíveis de **todas** as fontes (arquivos, logs, registry, browser),
ordenados juntos, em um só lugar.

**Por que importa:** um evento isolado raramente conta a história
completa; a **ordem** entre eventos revela causa e efeito. "O arquivo
malicioso foi criado **antes** ou **depois** da conexão de rede
suspeita?" muda completamente a interpretação (o arquivo foi baixado
por essa conexão, ou já existia e iniciou a conexão?).

## 3. Metadados de arquivo — os timestamps MACB

Todo arquivo, em qualquer sistema operacional, guarda metadados sobre
seu próprio histórico. No mundo forense, um acrônimo comum é **MACB**:

| Sigla | Significado | O que revela |
|---|---|---|
| **M** | Modified | quando o **conteúdo** do arquivo mudou pela última vez |
| **A** | Accessed | quando o arquivo foi lido pela última vez (nem todo sistema mantém isso atualizado por padrão — pode estar desabilitado por performance) |
| **C** | Changed (Linux) / Created (Windows, no contexto NTFS) | no Linux, quando os **metadados** (não o conteúdo) mudaram; no NTFS, geralmente interpretado como data de criação |
| **B** | Birth | quando o arquivo foi criado (nem todo sistema de arquivos registra isso separadamente) |

```bash
stat arquivo.txt        # Linux — mostra Access, Modify, Change
```

```powershell
Get-Item arquivo.txt | Select-Object CreationTime, LastWriteTime, LastAccessTime   # Windows
```

**Por que importa para segurança:** timestamps manipulados são uma
técnica real de evasão — um atacante pode alterar o timestamp de um
arquivo malicioso para parecer mais antigo (técnica chamada
**timestomping**, catalogada como **T1070.006 — Indicator Removal:
Timestomp**). Um analista forense atento compara **múltiplas** fontes
de timestamp (o arquivo em si, entradas de log relacionadas, registros
do sistema de arquivos em nível mais baixo) — se elas não batem entre
si, isso é, por si só, um forte indício de manipulação.

## 4. Sistema de arquivos — o que sobrevive mesmo depois de "apagado"

Quando um arquivo é "deletado" na maioria dos sistemas de arquivos, o
conteúdo geralmente **não é apagado imediatamente** — o sistema só
marca aquele espaço como "disponível para reuso". Até que outro dado
seja escrito por cima, o conteúdo original pode ser **recuperado** —
essa é a base de ferramentas de **data carving** (recuperação de
arquivos apagados).

**Por que importa:** um atacante que tenta "limpar seus rastros"
deletando arquivos maliciosos muitas vezes não percebe que isso não é
suficiente — o conteúdo pode continuar recuperável por dias, semanas,
ou até mais, dependendo de quanta escrita nova aconteceu no disco desde
então.

## 5. Memória (RAM) — por que é tão valiosa e tão frágil

Lembra do Módulo 00, Aula 1: a RAM guarda o que está **em uso agora**, e
**desaparece ao desligar**. Isso torna a análise de memória (*memory
forensics*) ao mesmo tempo extremamente valiosa e extremamente
sensível ao tempo:

- **Valiosa**: malware fileless (que nunca grava nada em disco) só é
  visível na memória enquanto está em execução; chaves de criptografia
  usadas por ransomware às vezes ficam temporariamente na memória;
  processos e conexões ativas no momento exato da captura ficam
  visíveis de forma muito mais completa do que qualquer log.
- **Frágil**: um reboot, ou até simplesmente desligar a máquina, apaga
  tudo — por isso, em uma investigação real, a **ordem de coleta**
  importa: geralmente memória é coletada **antes** de desligar/isolar
  um sistema, quando possível (chamado de princípio da **ordem de
  volatilidade** — coletar primeiro o que é mais efêmero).

```
Ordem de volatilidade (do mais efêmero ao mais persistente):
Registradores da CPU / cache → Memória RAM → Conexões de rede ativas →
Processos em execução → Disco → Backups/mídia removível
```

Uma imagem de memória é capturada com ferramentas específicas (ex.:
`winpmem` no Windows) e depois analisada (ex.: com o framework
**Volatility**, que consegue extrair processos, conexões de rede,
chaves de registry carregadas, e muito mais, diretamente de uma imagem
de memória congelada no tempo).

## 6. Conectando tudo

```
Timeline (super timeline) reúne TODOS os timestamps disponíveis
   ├─ Metadados MACB de arquivo → revelam quando algo foi
   │   criado/modificado/acessado (cuidado com timestomping)
   ├─ Sistema de arquivos → conteúdo "deletado" pode ser recuperável
   │   (data carving)
   └─ Memória → mais valiosa para malware fileless, mas a mais
       frágil (ordem de volatilidade determina QUANDO coletar)
```

## 7. Exercício prático

```bash
stat /etc/passwd    # (Linux) observe os timestamps Access/Modify/Change
```
```powershell
Get-Item C:\Windows\System32\notepad.exe | Select-Object CreationTime, LastWriteTime, LastAccessTime   # Windows
```

Reflita: esses timestamps fazem sentido para um arquivo do sistema que
você nunca modificou diretamente? O que você esperaria ver diferente se
um atacante tivesse substituído esse arquivo por uma versão maliciosa
(mesmo nome, conteúdo diferente)?

## 8. Recapitulando

- Forense preserva a evidência original intacta — sempre trabalha sobre
  cópia/imagem.
- Timeline (super timeline) junta timestamps de todas as fontes; a
  ordem cronológica revela causa e efeito.
- MACB são os timestamps centrais de arquivo; divergência entre fontes
  de timestamp pode indicar timestomping (T1070.006).
- Conteúdo "deletado" muitas vezes é recuperável (data carving) até ser
  sobrescrito.
- Memória é a fonte mais valiosa para malware fileless, mas a mais
  frágil — ordem de volatilidade define prioridade de coleta.

## Próxima aula (fecha o Módulo 16)

Artefatos específicos de Windows, Linux e navegador — os "lugares"
exatos onde cada sistema operacional deixa rastro de atividade.

## Fontes recomendadas

- **NIST SP 800-86 — "Guide to Integrating Forensic Techniques into
  Incident Response"**: referência oficial de princípios forenses,
  incluindo ordem de volatilidade. <https://csrc.nist.gov/pubs/sp/800/86/final>
- **MITRE ATT&CK — T1070.006 (Timestomp)**: técnica oficial de
  manipulação de timestamp. <https://attack.mitre.org/techniques/T1070/006/>
- **Volatility Foundation — documentação oficial**: referência do
  framework mais usado de análise de memória forense.
  <https://volatilityfoundation.org/>
