import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
from tracker import add_job

jobs_to_add = [
    {
        'title': 'Technical Project Manager – Application Migration (Cloud & On-Prem)',
        'company': 'iTRTech Group',
        'modality': 'Remoto',
        'location': 'Brasil / SP',
        'published_date': '04/11/2026',
        'competition': 'Baixa (nicho técnico de migração)',
        'fit': 'Alto (Migração de Datacenter, Cloud AWS/Azure, On-Prem e governança)',
        'url': 'https://br.indeed.com/viewjob?jk=c2bbc4cf8954ece6'
    },
    {
        'title': 'PMO Manager – Finance Transformation, LATAM',
        'company': 'QIMA',
        'modality': 'Remoto',
        'location': 'LATAM / Brasil',
        'published_date': '03/11/2026',
        'competition': 'Baixa (nicho executivo LATAM)',
        'fit': 'Alto (PMO corporativo, squads LATAM, espanhol fluente e governança orçamentária)',
        'url': 'https://br.indeed.com/viewjob?jk=46f53f6847bfc63a'
    },
    {
        'title': 'Senior IT Agile Project Manager',
        'company': 'Trafilea',
        'modality': 'Remoto',
        'location': 'Global / Brasil',
        'published_date': '04/11/2026',
        'competition': 'Média (empresa internacional)',
        'fit': 'Alto (PSM I Scrum.org, entrega ágil, liderança global e inglês C1)',
        'url': 'https://br.indeed.com/viewjob?jk=694bfc63f0c26380'
    },
    {
        'title': 'Gerente de Projetos SAP Sênior',
        'company': 'Blend IT Consultoria',
        'modality': 'Remoto',
        'location': 'Brasil',
        'published_date': '04/11/2026',
        'competition': 'Baixa (nicho SAP)',
        'fit': 'Alto (Gestão de ecossistemas SAP, governança e consultoria de TI)',
        'url': 'https://br.indeed.com/viewjob?jk=a65457a13074083f'
    },
    {
        'title': 'Gerente de Projetos Sênior - Remoto',
        'company': 'Lyncas',
        'modality': 'Remoto',
        'location': 'Brasil',
        'published_date': '03/11/2026',
        'competition': 'Média',
        'fit': 'Alto (Gestão de projetos corporativos de TI, senioridade 25+ anos e FGV)',
        'url': 'https://br.indeed.com/viewjob?jk=58232fd972e40fa4'
    },
    {
        'title': 'ScrumMaster / Gerente de Projetos Sênior',
        'company': 'Mooven',
        'modality': 'Remoto',
        'location': 'Brasil',
        'published_date': '02/11/2026',
        'competition': 'Média',
        'fit': 'Alto (PSM I, entrega híbrida Ágil/Waterfall e liderança de squads)',
        'url': 'https://br.indeed.com/viewjob?jk=9f71f275ce17b397'
    }
]

for j in jobs_to_add:
    ok, res = add_job(**j)
    print(f"Adicionado {j['title']}: {ok}")
