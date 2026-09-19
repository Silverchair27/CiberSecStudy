# Aula 2 (Módulo 09) — Laboratório: SIEM com Wazuh

[![📄 Baixar PDF desta aula](https://img.shields.io/badge/📄_Baixar-PDF_desta_aula-2b6cb0?style=for-the-badge)](02-laboratorio-wazuh.pdf)

## 1. Por que Wazuh para este laboratório

**Wazuh** é uma plataforma de SIEM/XDR **gratuita e de código aberto**,
muito usada tanto em produção real quanto para estudo — não exige
licença paga para aprender o pipeline completo (Aula 1) na prática:
coleta (via agente), parsing, normalização, indexação (usa o Wazuh
Indexer, baseado em OpenSearch) e correlação (as "regras" do Wazuh).

Este laboratório é feito com **Docker**, a mesma tecnologia de
containers que vimos no Módulo 00, Aula 3 — permite rodar o manager,
o indexer e o dashboard em containers isolados, sem precisar instalar
nada diretamente no seu sistema operacional.

## 2. Arquitetura do laboratório (single-node)

```
┌─────────────────────────────────────────────┐
│              Seu computador (host)            │
│                                                 │
│  ┌───────────────┐  ┌────────────────────┐    │
│  │ Wazuh Manager  │  │  Wazuh Indexer      │    │
│  │ (recebe eventos,│→│  (armazena e indexa │    │
│  │  aplica regras) │  │   os eventos)       │    │
│  └───────┬────────┘  └──────────┬──────────┘    │
│          │                       │               │
│          │              ┌────────▼──────────┐    │
│          │              │  Wazuh Dashboard   │    │
│          │              │  (interface web)   │    │
│          │              └────────────────────┘    │
│          │                                          │
│   ┌──────▼──────┐                                  │
│   │ Wazuh Agent  │  (instalado na máquina que       │
│   │ (opcional,   │   você quer monitorar)           │
│   │  outro host) │                                  │
│   └─────────────┘                                   │
└─────────────────────────────────────────────┘
```

O **manager** é o cérebro (recebe eventos, aplica regras de
correlação); o **indexer** guarda e indexa tudo (a parte de "Indexação"
da Aula 1); o **dashboard** é a interface web onde você navega,
pesquisa e monta visualizações — o equivalente ao que um analista N1/N2
usa no dia a dia real (Módulo 08).

## 3. Pré-requisitos

- Docker e Docker Compose instalados (`docker --version`,
  `docker compose version`).
- Pelo menos ~4 GB de RAM livres e alguns GB de espaço em disco — o
  Wazuh Indexer (baseado em OpenSearch) é o componente mais pesado.
- **Acesso à internet de dentro dos containers**, para baixar as
  imagens do Wazuh e o script oficial de geração de certificados
  (`wazuh-certs-tool.sh`, baixado de `packages.wazuh.com` durante o
  setup). Isso é importante: em ambientes com proxy/firewall
  corporativo restritivo, essa etapa pode falhar mesmo com o Docker
  funcionando normalmente — foi exatamente o que aconteceu ao tentar
  rodar este laboratório dentro do ambiente sandboxed desta sessão,
  cujo proxy de rede não é repassado para dentro dos containers. Se
  isso acontecer com você, rode o laboratório numa máquina/VM com
  acesso direto à internet.

## 4. Passo a passo (execute na sua máquina/VM)

```bash
git clone https://github.com/wazuh/wazuh-docker.git -b v4.14.7
cd wazuh-docker/single-node

# 1. Ajuste necessário no host Linux para o Indexer (OpenSearch) funcionar
sudo sysctl -w vm.max_map_count=262144

# 2. Gera os certificados TLS usados pela comunicação entre os componentes
docker compose -f generate-indexer-certs.yml run --rm generator

# 3. Sobe o ambiente completo (manager + indexer + dashboard)
docker compose up -d

# 4. Acompanhe os logs até tudo inicializar (leva ~1 minuto na primeira vez)
docker compose logs -f
```

(Ajuste a tag `v4.14.7` para a versão estável mais recente disponível
no momento em que você for fazer o laboratório — confira em
<https://github.com/wazuh/wazuh-docker/tags>.)

Depois de tudo subir, acesse `https://localhost` no navegador
(certificado autoassinado — o navegador vai avisar, é esperado num
laboratório local; nunca ignore esse aviso em um ambiente de produção
real). Login padrão do dashboard: usuário `admin`, senha
`SecretPassword` (definida no `docker-compose.yml` — **troque isso** se
for manter o ambiente rodando por mais tempo, mesmo em laboratório).

## 5. Conectando um agente (opcional, mas recomendado)

Para ver o pipeline completo de verdade (coleta → parsing →
normalização → correlação → alerta), instale o **Wazuh Agent** em uma
segunda máquina (pode ser uma VM Linux separada, lembrando do Módulo
00, Aula 3 — máquinas virtuais são exatamente para isso: laboratório
isolado e seguro):

```bash
# No host que será monitorado (exemplo Ubuntu/Debian):
curl -o wazuh-agent.deb https://packages.wazuh.com/4.x/apt/pool/main/w/wazuh-agent/wazuh-agent_4.14.7-1_amd64.deb
sudo WAZUH_MANAGER='IP_DO_SEU_MANAGER' dpkg -i ./wazuh-agent.deb
sudo systemctl daemon-reload
sudo systemctl enable wazuh-agent
sudo systemctl start wazuh-agent
```

A partir daí, tudo que o agente coleta (logs do sistema, integridade de
arquivos, e — se configurado — eventos do Sysmon num agente Windows)
passa a aparecer no dashboard.

## 6. O que explorar no dashboard depois de configurado

- **Security Events**: os eventos brutos recebidos, já parseados e
  normalizados (Aula 1) — compare com como o log bruto se parecia antes
  (Módulo 01, Aula 5; Módulo 02, Aula 4).
- **Regras (Rules)**: o Wazuh vem com centenas de regras de correlação
  prontas — vale abrir algumas e reconhecer padrões que já estudamos
  (ex.: regras relacionadas a SSH brute force, muito parecidas em
  espírito com o script que construímos no Módulo 06).
- **Vulnerability Detection**: o Wazuh também consegue mapear
  vulnerabilidades conhecidas (CVEs — Módulo 20/21) em softwares
  instalados nos agentes.

## 7. Por que este laboratório importa

Rodar isso na prática (mesmo que só o manager+indexer+dashboard, sem
agente) já demonstra visualmente cada etapa do pipeline da Aula 1: você
vê logs brutos chegando, sendo indexados, e pode escrever suas próprias
buscas — o mesmo tipo de interação que um analista de SOC real faz.
Documentar esse laboratório (prints do dashboard, anotações do que
configurou) em `screenshots/` e `lab/` deste repositório é exatamente o
tipo de evidência de processo que valoriza um portfólio (Módulo 07,
Aula 3).

## 8. Recapitulando o Módulo 09

- Wazuh = SIEM/XDR gratuito e open source; arquitetura single-node =
  manager (correlação) + indexer (armazenamento/busca) + dashboard
  (interface).
- Setup via Docker Compose: gerar certificados → subir os containers →
  acessar o dashboard.
- Agente instalado em outra máquina fecha o pipeline completo: coleta
  real → parsing/normalização automáticos → aparece no dashboard.
- Ambientes com proxy/firewall restritivo podem bloquear o download do
  script de certificados durante o setup — rode em uma rede com acesso
  direto à internet.

Módulo 09 concluído. 🎉

## Próximo módulo

**Módulo 10 — EDR**: telemetria de endpoint, árvore de processos,
detecções e ações de resposta — a camada host-based que complementa o
SIEM que acabamos de configurar.

## Fontes recomendadas

- **Wazuh — documentação oficial de instalação via Docker**: guia
  oficial e atualizado, incluindo troubleshooting.
  <https://documentation.wazuh.com/current/deployment-options/docker/index.html>
- **Wazuh — documentação oficial do Wazuh Agent**: referência de
  instalação em diferentes sistemas operacionais.
  <https://documentation.wazuh.com/current/installation-guide/wazuh-agent/index.html>
