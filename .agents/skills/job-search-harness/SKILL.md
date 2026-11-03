---
name: job-search-harness
description: >-
  Execute automated job search runs for Humberto C. Garcia, targeting remote and hybrid IT Project Manager, PMO, and Program Manager positions with low competition and verified profile fit.
---

# Job Search Harness — Habilidade de Pesquisa Automatizada de Vagas

Esta habilidade executa a rotina estruturada de localização, filtragem e avaliação de oportunidades para **Humberto C. Garcia**, conforme as regras e perfil definidos no projeto.

## Perfil de Referência
Sempre consulte [perfil_humberto.md](../../perfil_humberto.md) como única fonte da verdade para qualificações, histórico, certificações e idiomas.

## Parâmetros de Execução
Antes de iniciar a busca, carregue os parâmetros de [config/parametros.json](../../config/parametros.json) ou os parâmetros personalizados passados pelo usuário:
- **MODALIDADE:** `remoto` (padrão) | `remoto + híbrido região Pouso Alegre/MG` | `todas`
- **PAÍSES/REGIÕES:** `Brasil + Exterior` (padrão) | `somente Brasil` | `somente Exterior`
- **CARGOS-ALVO:** `Gerente de Projetos de TI, IT Project Manager, PMO Manager, Program Manager`
- **SETORES:** `todos` ou específicos (energia, manufatura, cloud, etc.)
- **JANELA:** `últimos 7 dias` (padrão) | `3 dias` | `15 dias`
- **LIMITE CONCORRÊNCIA:** descartar vagas com 100+ candidatos visíveis
- **QUANTIDADE:** 10 a 15 vagas
- **IDIOMAS:** Português, Inglês (C1), Espanhol (Nativo/Bilíngue)

## Procedimento de Execução

1. **Leitura dos Parâmetros:** Identifique os parâmetros da rodada.
2. **Busca Ativa Multi-Repositório:**
   - Repositórios: LinkedIn Jobs, We Work Remotely, Remote OK, Himalayas, Wellfound, Indeed, Gupy, Catho, Glassdoor, Vagas.com.
   - Use `search_web` ou scripts em `scripts/` para consultas em tempo real.
3. **Deduplicação & Descarte Imediato:**
   - Descartar vagas com 100+ candidatos visíveis.
   - Descartar vagas publicadas fora da janela definida.
   - Descartar duplicatas (consultar `data/tracker.json`).
   - Descartar vagas de nível Júnior/Pleno ou sem relação com Projetos/TI.
4. **Análise de Concorrência & Fit:**
   - Estimar Concorrência (Baixo, Médio, Alto, Não estimável) com justificativa.
   - Avaliar Fit com Humberto (Alto, Médio, Baixo) com justificativa de uma linha baseada no histórico de 25+ anos, certificações (ITIL, PSM I, AWS, FGV) e migrações/cloud/infraestrutura/fornecedores.
5. **Ordenação:**
   - Fit (Alto primeiro) -> Concorrência (Baixo primeiro) -> Data de publicação (mais recente primeiro).
6. **Persistência:**
   - Atualizar `data/tracker.json` com as vagas selecionadas para manter histórico.
7. **Formatação Estrita do Contrato de Saída:**
   - Cabeçalho de parâmetros
   - Tabela de vagas
   - Resumo de descartes
   - Próximos Passos (3 vagas prioritárias)
   - Aviso obrigatório de confirmação na fonte.
