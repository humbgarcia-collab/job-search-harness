#!/usr/bin/env python3
"""
send_email_report.py - Envio de relatório de vagas por email ou gravação em arquivo.
Suporta qualquer provedor SMTP (Gmail, Outlook, etc.) via variáveis em .env.
Converte markdown básico para HTML limpo para leitura confortável no Gmail/Outlook.
"""

import os
import sys
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
REPORTS_DIR = BASE_DIR / "reports"
ENV_FILE = BASE_DIR / ".env"

def load_env():
    env_vars = {}
    if ENV_FILE.exists():
        with open(ENV_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env_vars[k.strip()] = v.strip().strip('"').strip("'")
    return env_vars

def markdown_to_html(md_text: str) -> str:
    # Cabeçalhos
    html = re.sub(r"^### (.*?)$", r"<h3 style='color: #1a73e8; margin-top: 18px;'>\1</h3>", md_text, flags=re.MULTILINE)
    html = re.sub(r"^## (.*?)$", r"<h2 style='color: #202124; border-bottom: 2px solid #e0e0e0; padding-bottom: 4px;'>\1</h2>", html, flags=re.MULTILINE)
    html = re.sub(r"^# (.*?)$", r"<h1 style='color: #202124;'>\1</h1>", html, flags=re.MULTILINE)
    
    # Negrito
    html = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", html)
    
    # Links
    html = re.sub(r"\[(.*?)\]\((.*?)\)", r"<a href='\2' style='color: #1a73e8; font-weight: bold;' target='_blank'>\1</a>", html)
    
    # Linhas de tabela simples ou quebras
    lines = html.split("\n")
    processed_lines = []
    in_table = False
    
    for line in lines:
        if line.strip().startswith("|") and line.strip().endswith("|"):
            if "---" in line:
                continue
            cols = [c.strip() for c in line.strip().split("|")[1:-1]]
            if not in_table:
                in_table = True
                processed_lines.append("<table border='1' cellpadding='8' cellspacing='0' style='border-collapse: collapse; width: 100%; border-color: #e0e0e0; font-family: sans-serif; font-size: 13px;'>")
                row_cells = "".join(f"<th style='background-color: #f1f3f4; color: #333;'>{c}</th>" for c in cols)
                processed_lines.append(f"<tr>{row_cells}</tr>")
            else:
                row_cells = "".join(f"<td style='padding: 8px; vertical-align: top;'>{c}</td>" for c in cols)
                processed_lines.append(f"<tr>{row_cells}</tr>")
        else:
            if in_table:
                processed_lines.append("</table>")
                in_table = False
            if line.strip():
                processed_lines.append(f"<p style='margin: 6px 0; font-family: sans-serif; font-size: 14px; line-height: 1.5;'>{line}</p>")
            else:
                processed_lines.append("<br/>")
                
    if in_table:
        processed_lines.append("</table>")
        
    body_content = "\n".join(processed_lines)
    return f"""
    <html>
      <body style='font-family: Arial, Helvetica, sans-serif; color: #202124; background-color: #ffffff; padding: 15px;'>
        {body_content}
      </body>
    </html>
    """

def save_report_locally(subject: str, content_markdown: str):
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d_%H%M")
    filename = REPORTS_DIR / f"relatorio_vagas_{today}.md"
    filename.write_text(f"# {subject}\n\n{content_markdown}", encoding="utf-8")
    print(f"[OK] Relatório salvo com sucesso em: {filename}")
    return filename

def send_email(subject: str, content_markdown: str):
    env = load_env()
    smtp_server = env.get("SMTP_SERVER", os.getenv("SMTP_SERVER", "smtp.gmail.com"))
    smtp_port = int(env.get("SMTP_PORT", os.getenv("SMTP_PORT", 587)))
    smtp_user = env.get("SMTP_USER", os.getenv("SMTP_USER"))
    smtp_pass = env.get("SMTP_PASS", os.getenv("SMTP_PASS"))
    email_to = env.get("EMAIL_TO", os.getenv("EMAIL_TO", smtp_user))

    # Salva sempre uma cópia local por segurança
    save_report_locally(subject, content_markdown)

    if not smtp_user or not smtp_pass or not email_to:
        print("[Aviso] Credenciais de email (SMTP_USER / SMTP_PASS) não configuradas no arquivo .env.")
        return False

    # Remove espaços da senha se houver
    clean_pass = smtp_pass.replace(" ", "")

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"Job Search Agent <{smtp_user}>"
        msg["To"] = email_to

        part_text = MIMEText(content_markdown, "plain", "utf-8")
        part_html = MIMEText(markdown_to_html(content_markdown), "html", "utf-8")
        
        msg.attach(part_text)
        msg.attach(part_html)

        with smtplib.SMTP(smtp_server, smtp_port, timeout=25) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(smtp_user, clean_pass)
            server.sendmail(smtp_user, [email_to], msg.as_string())

        print(f"[OK] Email enviado com sucesso para {email_to}!")
        return True
    except Exception as e:
        print(f"[Erro] Falha ao enviar email via SMTP: {e}")
        return False

if __name__ == "__main__":
    report_text = """
## Parâmetros da Rodada
- **Modalidade:** Remoto (Brasil e Exterior)
- **Cargos-alvo:** Gerente de Projetos de TI / PMO / Program Manager
- **Janela:** Últimos 7 dias
- **Candidato:** Humberto C. Garcia

## Oportunidades Identificadas (Indeed & Portais)

| Vaga (Link Direto) | Empresa | Fit | Concorrência | Modalidade / Local | Publicada em |
| [Technical Project Manager – Application Migration](https://br.indeed.com/viewjob?jk=c2bbc4cf8954ece6) | iTRTech Group | Alto (Datacenter, Cloud AWS/Azure, On-Prem) | Baixa | Remoto / SP | 04/11/2026 |
| [PMO Manager – Finance Transformation, LATAM](https://br.indeed.com/viewjob?jk=46f53f6847bfc63a) | QIMA | Alto (PMO executivo, squads LATAM, espanhol fluente) | Baixa | Remoto / LATAM | 03/11/2026 |
| [Senior IT Agile Project Manager](https://br.indeed.com/viewjob?jk=694bfc63f0c26380) | Trafilea | Alto (PSM I, entrega ágil, squads globais, inglês C1) | Média | Remoto / Global | 04/11/2026 |
| [Gerente de Projetos SAP Sênior](https://br.indeed.com/viewjob?jk=a65457a13074083f) | Blend IT Consultoria | Alto (Projetos SAP, governança e consultoria) | Baixa | Remoto / Brasil | 04/11/2026 |
| [Gerente de Projetos Sênior](https://br.indeed.com/viewjob?jk=58232fd972e40fa4) | Lyncas | Alto (Gestão corporativa de TI, FGV, 25+ anos) | Média | Remoto / Brasil | 03/11/2026 |
| [ScrumMaster / Gerente de Projetos Sênior](https://br.indeed.com/viewjob?jk=9f71f275ce17b397) | Mooven | Alto (PSM I, híbrido Ágil/Waterfall) | Média | Remoto / Brasil | 02/11/2026 |
| [Gerente de Projetos e Contratos de TI](https://itix.gupy.io/) | Itix | Alto (Gestão de fornecedores, contratos de TI) | Baixa | Remoto / Brasil | 01/11/2026 |
| [Tech Project Manager](https://br.indeed.com/viewjob?jk=9f6d7a649bd3951b) | Vortigo | Médio (Gestão de squad de produto digital ágil) | Média | Remoto / Brasil | 04/11/2026 |

## Resumo de Descartes
- 26 vagas descartadas: 14 por nível operacional/júnior, 7 duplicadas de buscas anteriores e 5 por perfil puramente dev.

## Próximos Passos (3 Vagas Prioritárias)
1. **Technical Project Manager – Application Migration (iTRTech Group):** Encaixe exato com sua vivência de 25+ anos em Datacenters, migrações complexas e Cloud AWS/Azure.
2. **PMO Manager – Finance Transformation, LATAM (QIMA):** Posição executiva regional LATAM valorizando liderança multicultural, espanhol fluente e otimização financeira.
3. **Senior IT Agile Project Manager (Trafilea):** Oportunidade internacional remota com remuneração global, aplicando certificação PSM I e inglês C1.

*Confirme a disponibilidade direto na fonte antes de aplicar; vagas podem ser encerradas rapidamente.*
"""
    subject = f"🎯 Vagas de TI & PMO Remoto - Humberto C. Garcia ({datetime.now().strftime('%d/%m/%Y')})"
    send_email(subject, report_text.strip())
