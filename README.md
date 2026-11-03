# Job Search Harness — Humberto C. Garcia

> **Agente de pesquisa automatizada especializado em oportunidades remotas (Brasil e Internacional) e híbridas (região de Pouso Alegre/MG) para Gerência de Projetos de TI, PMO e Program Management.**

Este projeto foi construído para potencializar a recolocação profissional de **Humberto C. Garcia**, priorizando **vagas com baixa concorrência** (poucos candidatos visíveis, recência de publicação, nichadas) e **alto fit** com sua sólida trajetória de 25+ anos em liderança de infraestrutura de TI, migração de datacenters, cloud (AWS), governança, PMO corporativo e gestão de grandes fornecedores globais.

---

## 🎯 Objetivo

Eliminar o tempo gasto navegando manualmente em vagas saturadas (+100 candidatos) e entregar listas curadas, desduplicadas, com concorrência estimada e indicação precisa de fit para aplicação imediata.

---

## 📂 Arquitetura do Workspace

```text
Agente Job Search/
├── .agents/
│   └── skills/
│       └── job-search-harness/
│           └── SKILL.md                  # Habilidade Antigravity registrada
├── config/
│   └── parametros.json                   # Parâmetros padrão de execução
├── data/
│   ├── tracker.json                      # Base persistente de vagas e status
│   └── historico_execucoes.md            # Log cronológico em markdown
├── scripts/
│   ├── search_apis.py                    # Busca automatizada em APIs públicas e RSS feeds
│   └── tracker.py                        # Utilitário de deduplicação e controle de status
├── .gitignore                            # Exclusões de arquivos temporários
├── AGENTS.md                             # Regras do workspace para agentes
├── GEMINI.md                             # Instruções, persona e contrato do Job Search Harness
├── perfil_humberto.md                    # Fonte única da verdade do perfil profissional
├── prompt-job-search-harness-antigravity.md # Prompt mestre de especificação
└── README.md                             # Documentação do projeto
```

---

## 👤 Perfil de Humberto (Resumo de Referência)

| Dimensão | Detalhes |
|---|---|
| **Cargo-alvo** | Gerente de Projetos de TI / PMO / Program Manager / IT Project Manager (Sênior) |
| **Localização** | Pouso Alegre/MG (Foco: **100% Remoto Brasil/Exterior**; Secundário: Híbrido Sul de MG) |
| **Experiência** | 25+ anos liderando projetos de TI em multinacionais (J&J, Mapfre, Equatorial, Goodyear, Gamesa, Aon Hewitt, EDS/HP, Cargill) |
| **Competências Core** | Datacenter Tier III, Cloud (AWS/Azure), SAP, ServiceNow, Gestão de Fornecedores Globais, Economias R$2M-3M+/ano |
| **Formação** | MBA em Project Management (FGV - PMI 360h), Strategic Business Leadership (Ohio University), Gestão de SI (Unip) |
| **Certificações** | ITIL v3, PSM I (Scrum.org), AWS, Fundamentos de IA Aplicada |
| **Idiomas** | Português (Nativo), Inglês (C1 - Full Professional), Espanhol (Fluente/Bilíngue) |
| **Pretensão** | Aberto a negociação (sem piso/teto pré-fixado) |

*Para os detalhes completos, consulte [perfil_humberto.md](file:///c:/Users/LENOVO/OneDrive/Humberto/pessoal/Emprego/INTELIGENCIA%20ARTIFICIAL/Agente%20de%20IA/Agente%20Job%20Search/perfil_humberto.md).*

---

## 🔎 Repositórios Monitorados

1. **LinkedIn Jobs** (Remoto, Gerente de Projetos / PMO, últimos 7 dias)
2. **We Work Remotely**
3. **Remote OK**
4. **Himalayas**
5. **Wellfound (AngelList Talent)**
6. **Indeed** (Brasil e Internacional)
7. **Gupy** (Brasil Remoto)
8. **Catho**
9. **Glassdoor**
10. **Vagas.com**
*(Fontes adicionais como PMAlliance, ProjectManagementJobs e EU Remote Jobs são incluídas sob demanda).*

---

## ⚙️ Parâmetros de Execução

Você pode alterar os parâmetros a qualquer momento em [config/parametros.json](file:///c:/Users/LENOVO/OneDrive/Humberto/pessoal/Emprego/INTELIGENCIA%20ARTIFICIAL/Agente%20de%20IA/Agente%20Job%20Search/config/parametros.json) ou simplesmente pedir no chat:

```text
MODALIDADE: remoto (padrão) | remoto + híbrido região Pouso Alegre/MG | todas
PAÍSES/REGIÕES: Brasil + Exterior (padrão) | somente Brasil | somente Exterior
CARGOS-ALVO: Gerente de Projetos de TI, IT Project Manager, PMO Manager, Program Manager
SETORES PREFERENCIAIS: nenhum (todos aceitos) | [ex.: energia, farmacêutica, cloud]
JANELA DE PUBLICAÇÃO: últimos 7 dias (padrão) | últimos 3 dias | últimos 15 dias
LIMITE DE CONCORRÊNCIA: excluir vagas com 100+ candidatos visíveis
QUANTIDADE DE RESULTADOS: 10-15 vagas (padrão)
IDIOMA DAS VAGAS: Português, Inglês, Espanhol
```

---

## 🚀 Como Executar

Basta interagir diretamente no chat do Antigravity neste workspace:

- **Execução padrão:** *"Buscar vagas"* ou *"Execute uma nova rodada de busca"*.
- **Com parâmetros customizados:** *"Busque vagas remotas internacionais em inglês nos últimos 3 dias com foco em Cloud"*.
- **Atualizar status:** *"Marque a vaga do Lifelancer como Candidatura Enviada"*.

---

## 📋 Contrato Estrito de Saída

Cada execução do agente entrega obrigatoriamente:
1. **Cabeçalho da execução** com parâmetros adotados.
2. **Tabela estruturada** com colunas:
   `Vaga | Empresa | Modalidade | Local/País | Publicada em | Concorrência (estimativa) | Fit | Link`.
3. **Observações de descarte** resumidas (quantidade excluída por alta concorrência, fora da janela ou duplicatas).
4. **Próximos Passos** com as 3 vagas prioritárias para aplicar primeiro.
5. **Aviso de confirmação** na fonte.
