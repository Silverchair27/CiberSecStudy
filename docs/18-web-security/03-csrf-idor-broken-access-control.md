# Aula 3 (Módulo 18) — CSRF e IDOR / Broken Access Control

[![📄 Baixar PDF desta aula](https://img.shields.io/badge/📄_Baixar-PDF_desta_aula-2b6cb0?style=for-the-badge)](03-csrf-idor-broken-access-control.pdf)

Fechando o módulo com duas vulnerabilidades que não dependem de
"injetar código" (diferente das Aulas 1 e 2) — abusam de **confiança**
entre navegador/servidor, ou de **falhas de autorização**.

## Parte 1 — CSRF (Cross-Site Request Forgery)

### O que é

**CSRF** faz o navegador da **vítima**, já autenticado em um site,
enviar uma requisição **sem ela saber/querer**, para uma ação em nome
dela (ex.: transferir dinheiro, mudar senha, mudar e-mail de
recuperação de conta).

### Por que acontece

Quando você está logado num site (Módulo 03, Aula 7 — cookie de
sessão), o navegador **envia esse cookie automaticamente** em qualquer
requisição para aquele domínio — mesmo que a requisição tenha sido
iniciada por **outra página**, aberta em outra aba. O servidor, ao
receber a requisição com o cookie válido, não tem como saber que ela
não foi realmente iniciada pelo usuário de propósito.

### Como funciona (exemplo didático)

```html
<!-- Numa página maliciosa, apenas de exemplo didático -->
<img src="https://banco-exemplo.com/transferir?para=atacante&valor=1000">
```

Se o site do banco aceitar essa transferência via um simples `GET`
(sem verificação adicional), e a vítima estiver logada nesse banco em
outra aba **enquanto visita a página maliciosa**, o navegador dispara
essa requisição automaticamente (o navegador está só carregando uma
"imagem" — não sabe que na verdade é uma ação sensível), com o cookie
de sessão da vítima anexado.

### Como reproduzir em laboratório

DVWA tem um módulo específico de CSRF, com diferentes níveis de
dificuldade/proteção para praticar.

### Que evidências deixa

Requisições que alteram estado (mudam senha, fazem transferência)
vindas com um cabeçalho `Referer`/`Origin` **diferente** do domínio
esperado — um forte sinal de que a requisição não se originou de
dentro do próprio site.

### Como detectar

```
SE requisição de mudança de estado (POST sensível)
E cabeçalho Origin/Referer NÃO corresponde ao domínio esperado
ENTÃO sinalizar — possível CSRF
```

### Como corrigir

- **CSRF token**: um valor único e imprevisível, gerado pelo servidor
  e incluído em cada formulário — validado a cada submissão. Um site
  malicioso não tem como saber/incluir esse token, então a requisição
  forjada falha.
- **SameSite cookies** (já mencionado no Módulo 03, Aula 7): o
  atributo `SameSite=Strict` ou `Lax` em um cookie impede que ele seja
  enviado automaticamente em requisições originadas de **outro** site
  — uma defesa moderna e muito eficaz, hoje o padrão em navegadores
  atualizados.
- Ações sensíveis nunca deveriam aceitar `GET` simples — exigir `POST`
  já é uma primeira camada (embora não suficiente sozinha).

### Como validar

Tente reproduzir a ação forjada depois da correção — deve falhar por
token ausente/inválido, mesmo com cookie de sessão válido presente.

## Parte 2 — IDOR (Insecure Direct Object Reference) / Broken Access Control

### O que é

**IDOR** acontece quando uma aplicação usa um identificador (ex.: um
número de pedido, um ID de usuário) diretamente numa URL/parâmetro,
sem verificar se o usuário **autenticado** tem permissão para acessar
**aquele** recurso específico.

### Por que acontece

A aplicação confirma **quem** você é (autenticação), mas falha em
confirmar **o que** você tem permissão de acessar (autorização) —
já mencionamos essa distinção no Módulo 03, Aula 7.

### Como funciona (exemplo didático)

```
https://loja-exemplo.com/pedidos/8842   ← seu próprio pedido, normal
https://loja-exemplo.com/pedidos/8843   ← trocando o número manualmente...
```

Se a aplicação só verificar "existe um pedido com esse número?" sem
checar "esse pedido pertence ao usuário logado?", qualquer usuário
autenticado consegue ver (ou até modificar) pedidos de **qualquer
outra pessoa**, só trocando o número na URL.

### Como reproduzir em laboratório

OWASP Juice Shop tem desafios específicos de IDOR/Broken Access
Control catalogados.

### Que evidências deixa

- Um mesmo usuário acessando **sequencialmente** muitos IDs diferentes
  em pouco tempo (`/pedidos/1`, `/pedidos/2`, `/pedidos/3`...) é um
  padrão clássico de **enumeração** — alguém testando sistematicamente
  quais IDs existem e são acessíveis.
- Respostas de sucesso (`200 OK`, Módulo 03 Aula 7) para recursos que
  não pertencem àquele usuário, quando cruzado com dados de
  propriedade/dono do recurso.

### Como detectar

```
SE mesmo usuário acessa MUITOS IDs sequenciais diferentes em curto
   período de tempo
ENTÃO sinalizar — possível enumeração/IDOR em andamento
```

### Como corrigir

Toda consulta que busca um recurso por ID deve **sempre** incluir uma
verificação de propriedade/permissão explícita — nunca confiar que "se
o ID é válido, o acesso é permitido":

```python
# VULNERÁVEL
pedido = db.get_pedido(id=pedido_id)

# CORRETO — verifica propriedade explicitamente
pedido = db.get_pedido(id=pedido_id, usuario_id=usuario_logado.id)
```

Usar identificadores **não sequenciais/não previsíveis** (como UUIDs
em vez de números incrementais) também dificulta enumeração, embora
**nunca** deva ser a única defesa (segurança por obscuridade não
substitui verificação de autorização real).

### Como validar

Logado como um usuário, tente acessar explicitamente um recurso que
pertence a **outro** usuário — a aplicação deve negar (idealmente
retornando `403 Forbidden`, não revelando sequer se o recurso existe,
dependendo da sensibilidade).

## Conectando o Módulo 18 inteiro

```
SQL Injection (Aula 1)  → código+dado misturado no BANCO DE DADOS
XSS (Aula 2)             → código+dado misturado na PÁGINA/NAVEGADOR
CSRF (esta aula)         → confiança abusada entre navegador e servidor
IDOR (esta aula)         → autenticação confirmada, mas AUTORIZAÇÃO
                            não verificada por recurso específico

Correção sempre segue o mesmo princípio:
NUNCA confiar em dado/contexto vindo do lado do usuário sem verificação
explícita no servidor
```

## Recapitulando o Módulo 18

- CSRF explora envio automático de cookie pelo navegador — mitigado
  por CSRF token e `SameSite` cookies.
- IDOR explora falta de verificação de autorização por recurso —
  mitigado por checagem explícita de propriedade em toda consulta.
- Todas as quatro vulnerabilidades deste módulo (SQLi, XSS, CSRF,
  IDOR) compartilham a mesma lição central: **nunca confie em dado ou
  contexto vindo do cliente sem verificação explícita no servidor.**

Módulo 18 concluído. 🎉

## Próximo módulo

**Módulo 19 — Active Directory**: domain, Kerberos, GPO, e os ataques
mais relevantes de credential/lateral movement em ambiente corporativo
— incluindo o Golden Ticket que mencionamos no Módulo 17.

## Fontes recomendadas

- **OWASP — "Cross-Site Request Forgery Prevention Cheat Sheet"**: guia
  oficial da OWASP. <https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html>
- **OWASP — "Insecure Direct Object Reference Prevention Cheat
  Sheet"**: guia oficial da OWASP.
  <https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html>
- **OWASP Top 10 (edição atual)**: referência oficial e atualizada de
  categorias de vulnerabilidade web mais críticas, incluindo Broken
  Access Control (categoria que engloba IDOR). <https://owasp.org/www-project-top-ten/>
