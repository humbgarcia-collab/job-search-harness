# Job Search Harness — Humberto C. Garcia

> **Agente Autônomo de Pesquisa e Curadoria de Oportunidades Remotas (Brasil & Internacional) e Híbridas para Gerência de Projetos de TI, PMO e Program Management.**

Este projeto combina **Engenharia de Prompt, Automação com Agentes de IA, Web Scraping com Playwright e Pipeline de Notificações SMTP** para criar uma rotina autônoma de busca de empregos. Ele prioriza **vagas com baixa concorrência** (poucos candidatos visíveis, recência de publicação, nichadas) e **alto fit** com o perfil executivo de **Humberto C. Garcia** (25+ anos liderando infraestrutura de TI, migração de datacenters, cloud AWS/Azure, governança e gestão de fornecedores globais).

---

## 🎯 Destaques do Projeto (Portfolio Showcase)

- 🤖 **Orquestração de Agente de IA:** Configuração de harness com persona, regras estritas de contrato de saída, governança de dados e deduplicação persistente.
- 🌐 **Browser Automation (Playwright):** Raspagem headless do Indeed com técnicas anti-detecção (`--disable-blink-features=AutomationControlled`, headers customizados e queries diretas).
- ⏰ **Execução Agendada em Segundo Plano:** Automação via Sidecar agendada (Cron: Segunda, Quarta e Sexta às 13:00 de Brasília) com permissões pré-aprovadas.
- 📧 **Notificações por E-mail (SMTP):** Conversão automática de relatórios em Markdown para HTML estilizado, entregue diretamente no Gmail.
- 📊 **Deduplicação Persistente:** Histórico em JSON (`data/tracker.json`) que previne alertas duplicados e acompanha status de candidaturas.

---

## 📂 Arquitetura do Repositório

```text
Agente Job Search/
├── .agents/
│   └── skills/
│       └── job-search-harness/
│           └── SKILL.md                  # Especificação da habilidade do agente
├── config/
│   └── parametros.json                   # Parâmetros padrão de execução
├── data/
│   ├── tracker.json                      # Base persistente de vagas e histórico
│   └── historico_execucoes.md            # Log cronológico das rodadas
├── reports/                              # Relatórios gerados em Markdown/HTML
├── scripts/
│   ├── search_apis.py                    # Busca em APIs públicas e feeds RSS
│   ├── indeed_browser.py                 # Crawler headless via Playwright para Indeed Brasil
│   ├── tracker.py                        # Módulo de deduplicação e controle de status
│   └── send_email_report.py              # Parser Markdown-HTML e despachante SMTP
├── .env.example                          # Modelo de variáveis de ambiente
├── .gitignore                            # Proteção de credenciais e caches
├── AGENTS.md                             # Regras de orquestração do workspace
├── GEMINI.md                             # Persona, regras e contrato estrito de saída
├── perfil_humberto.md                    # Fonte única da verdade do perfil profissional
├── requirements.txt                      # Dependências Python
└── README.md                             # Documentação do projeto
```

---

## 👤 Perfil Profissional de Referência

| Dimensão | Detalhes |
|---|---|
| **Cargos-alvo** | Gerente de Projetos de TI / PMO Manager / Program Manager / IT Delivery |
| **Modalidade** | Prioridade: **100% Remoto (Brasil e Global)**; Secundário: Híbrido Sul de MG |
| **Experiência** | 25+ anos (J&J, Mapfre, Equatorial Energia, Goodyear, Gamesa, Aon Hewitt, EDS/HP, Cargill) |
| **Competências Core** | Datacenter Tier III, Cloud (AWS/Azure), SAP, ServiceNow, Gestão de Fornecedores Globais, Otimização de Custos (R$2M-3M+/ano) |
| **Formação** | MBA em Project Management (FGV - PMI 360h), Strategic Business Leadership (Ohio University), Gestão de SI (Unip) |
| **Certificações** | ITIL v3, PSM I (Scrum.org), AWS Cloud, Fundamentos de IA Aplicada |
| **Idiomas** | Português (Nativo), Inglês (C1 - Full Professional), Espanhol (Nativo/Bilíngue) |

---

## ⚙️ Como Executar Localmente

### 1. Clonar o Repositório
```bash
git clone https://github.com/<seu-usuario>/job-search-harness.git
cd job-search-harness
```

### 2. Criar e Ativar Ambiente Virtual
```bash
python -m venv .venv
# No Windows:
.venv\Scripts\activate
# No Linux/Mac:
source .venv/bin/activate
```

### 3. Instalar Dependências e Navegadores do Playwright
```bash
pip install -r requirements.txt
playwright install chromium
```

### 4. Configurar Variáveis de Ambiente
Copie o arquivo `.env.example` para `.env` e configure suas credenciais de e-mail (caso queira envio automático via Gmail SMTP):
```bash
cp .env.example .env
```

### 5. Executar os Módulos
- **Busca em APIs abertas:**
  ```bash
  python scripts/search_apis.py
  ```
- **Busca no Indeed via Playwright:**
  ```bash
  python scripts/indeed_browser.py
  ```
- **Envio do relatório por e-mail:**
  ```bash
  python scripts/send_email_report.py
  ```

---

## 📋 Licença
Projeto pessoal desenvolvido para fins de pesquisa, automação de carreira e demonstração de competências em IA Aplicada e Gestão de Tecnologia.
