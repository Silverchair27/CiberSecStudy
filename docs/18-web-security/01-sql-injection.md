# Aula 1 (Módulo 18) — SQL Injection

[![📄 Baixar PDF desta aula](https://img.shields.io/badge/📄_Baixar-PDF_desta_aula-2b6cb0?style=for-the-badge)](01-sql-injection.pdf)

> Pratique só em aplicações feitas para isso (ex.: DVWA, OWASP Juice
> Shop, bWAPP — ambientes vulneráveis de propósito, para treino
> autorizado) — nunca em sites/sistemas de terceiros sem autorização
> explícita.

## 1. O que é

**SQL Injection (SQLi)** acontece quando uma aplicação web monta uma
consulta a um banco de dados (SQL — a linguagem usada pela maioria dos
bancos de dados relacionais) **inserindo diretamente** um dado enviado
pelo usuário, sem tratá-lo como dado puro — permitindo que o atacante
**altere a estrutura** da consulta original.

## 2. Por que acontece

O erro central é **misturar código e dado** — a aplicação constrói a
consulta concatenando texto (código SQL) com o que o usuário digitou
(que deveria ser só dado), sem uma separação clara entre os dois.

## 3. Como funciona (exemplo didático)

Imagine uma tela de login que monta a consulta assim (código
**vulnerável**, só para ilustrar o problema — nunca escreva código
assim):

```
SELECT * FROM usuarios WHERE login = '<usuario>' AND senha = '<senha>'
```

Se o usuário digitar, no campo de login:

```
admin' --
```

A consulta final vira:

```sql
SELECT * FROM usuarios WHERE login = 'admin' --' AND senha = '...'
```

O `--` inicia um **comentário** em SQL — tudo depois dele é ignorado.
Resultado: a checagem de senha inteira desaparece da consulta, e o
atacante entra como `admin` sem saber a senha real.

Outras variações comuns: usar `UNION SELECT` para **combinar** o
resultado de uma consulta legítima com dados de **outra tabela**
inteira (extraindo dados que a aplicação nunca deveria expor), ou
técnicas de **blind SQLi** (quando a aplicação não mostra o resultado
diretamente, mas o atacante consegue inferir informação observando
diferenças sutis na resposta — como tempo de resposta ou uma página de
erro vs. sucesso).

## 4. Como reproduzir em laboratório

Ambientes como **OWASP Juice Shop** e **DVWA** (Damn Vulnerable Web
Application) têm páginas **deliberadamente vulneráveis** para praticar
com segurança, em um ambiente isolado (lembrando do Módulo 00, Aula
3 — sempre em VM/container isolado, nunca na sua rede de produção).

## 5. Que evidências deixa

- **Logs de acesso do servidor web**: a URL/parâmetro enviado
  geralmente mostra sintaxe SQL suspeita (aspas, `--`, `UNION`,
  `OR 1=1`) diretamente no parâmetro da requisição.
- **Logs do banco de dados** (se auditoria estiver habilitada):
  consultas anômalas, muito diferentes do padrão esperado da
  aplicação.
- **WAF** (*Web Application Firewall*, mencionado no Módulo 03, Aula
  6): se presente, normalmente gera um log/alerta próprio ao bloquear
  um padrão reconhecido de SQLi.

## 6. Como detectar

```
SE parâmetro de requisição HTTP contém padrões como:
   ' OR '1'='1
   UNION SELECT
   --  (comentário SQL)
   ; DROP TABLE
ENTÃO alertar — possível tentativa de SQL Injection
```

Isso é literalmente o tipo de regra que um WAF/Suricata (Módulo 04)
aplicaria sobre tráfego HTTP — detecção por assinatura de padrão de
texto suspeito no corpo/parâmetros da requisição.

## 7. Como investigar

Se um alerta desse tipo dispara: qual endpoint foi alvo? A consulta
teve sucesso (retornou dados que não deveria) ou foi bloqueada? Houve
**múltiplas variações** tentadas em sequência rápida (sinal de uma
ferramenta automatizada testando SQLi, não uma tentativa manual
isolada)? Os logs do banco de dados confirmam que alguma consulta
anômala realmente chegou a ser executada?

## 8. Como corrigir

**A correção correta não é "filtrar aspas"** (abordagem frágil, fácil
de contornar) — é usar **prepared statements** (também chamados de
*parameterized queries*): o código SQL e os dados do usuário são
enviados **separadamente** para o banco de dados, que nunca interpreta
o dado do usuário como parte da estrutura da consulta, não importa o
que ele contenha.

```python
# VULNERÁVEL — nunca faça isso
cursor.execute(f"SELECT * FROM usuarios WHERE login = '{usuario}'")

# CORRETO — prepared statement
cursor.execute("SELECT * FROM usuarios WHERE login = %s", (usuario,))
```

Além disso: princípio do menor privilégio (Módulo 00, Aula 2) também
se aplica à conta de banco de dados usada pela aplicação — ela não
deveria ter permissão para acessar tabelas que a aplicação nunca
precisa tocar, limitando o dano mesmo se uma injeção acontecer.

## 9. Como validar a correção

Reproduza exatamente o mesmo payload que funcionava antes (`admin' --`,
por exemplo) e confirme que ele agora é tratado como **texto literal**
(um login que simplesmente não existe), não mais como código SQL.

## Conectando com o resto do curso

```
Log de acesso web → mesmo tipo de análise do Módulo 04 (Wireshark/
                     análise de requisição HTTP, Módulo 03 Aula 7)
Detecção por assinatura → mesmo princípio do Suricata (Módulo 04)
MITRE ATT&CK → T1190 (Exploit Public-Facing Application) — já
                mencionada no Cenário 3 do Módulo 10 e na Aula 2
                do Módulo 13
```

## Recapitulando

- SQLi ocorre quando dado do usuário é tratado como código SQL — o
  erro central é misturar código e dado.
- Sintaxe suspeita (`'`, `--`, `UNION SELECT`, `OR 1=1`) em parâmetros
  HTTP é a evidência/detecção mais direta.
- A correção correta é prepared statements, não "filtrar caracteres" —
  além de aplicar menor privilégio na conta de banco de dados.

## Próxima aula

XSS (Cross-Site Scripting) — quando a aplicação permite que código
malicioso rode no **navegador de outro usuário**, não no servidor.

## Fontes recomendadas

- **OWASP — "SQL Injection Prevention Cheat Sheet"**: guia oficial da
  OWASP com a abordagem correta de prevenção.
  <https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html>
- **MITRE ATT&CK — T1190 (Exploit Public-Facing Application)**: técnica
  oficial associada à exploração de vulnerabilidades web, incluindo
  SQLi. <https://attack.mitre.org/techniques/T1190/>
- **OWASP Juice Shop / DVWA**: aplicações oficiais de laboratório,
  mantidas pela comunidade de segurança, feitas especificamente para
  prática autorizada. <https://owasp.org/www-project-juice-shop/>
