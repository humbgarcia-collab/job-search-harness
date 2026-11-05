#!/usr/bin/env python3
"""
search_indeed.py - Busca de vagas no Indeed Brasil via web scraping simples.
Indeed bloqueia bots pesados mas aceita requests básicos com User-Agent adequado.
Complementa as fontes de API com resultados do maior agregador de vagas do Brasil.
"""

import json
import re
import sys
import urllib.request
import urllib.parse
import html as html_lib
from datetime import datetime, timezone, timedelta

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

# Termos de busca no Indeed Brasil
INDEED_QUERIES = [
    "gerente de projetos ti remoto",
    "it project manager remoto brasil",
    "pmo gestor projetos remoto",
    "program manager remoto",
    "gerente projetos infraestrutura remoto",
]

EXCLUDE_TERMS = [
    "junior", "júnior", "estagiário", "estágio", "intern",
    "obras", "civil", "construção", "imóveis", "marketing"
]


def _get_headers():
    return {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }


def fetch_indeed_brasil(query: str, days: int = 7) -> list:
    """Busca vagas no Indeed Brasil para uma query específica."""
    jobs = []
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)

    # Map days to Indeed's fromage parameter
    if days <= 1:
        fromage = "1"
    elif days <= 3:
        fromage = "3"
    elif days <= 7:
        fromage = "7"
    else:
        fromage = "14"

    encoded_q = urllib.parse.quote(query)
    url = (
        f"https://br.indeed.com/vagas?q={encoded_q}"
        f"&remotejob=032b3046-06a3-4876-8dfd-474eb5e7ed11"
        f"&fromage={fromage}&sort=date"
    )

    try:
        req = urllib.request.Request(url, headers=_get_headers())
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read()
            # Indeed may return gzip
            try:
                import gzip
                content = gzip.decompress(raw).decode("utf-8", errors="ignore")
            except Exception:
                content = raw.decode("utf-8", errors="ignore")

            # Indeed embeds job data in a JSON-like script tag
            # Look for window.mosaic.providerData
            m_data = re.search(
                r'"jobKeysWithInfo":\s*(\{.*?\})\s*,\s*"jobKeys"',
                content,
                re.DOTALL
            )
            if not m_data:
                # Fallback: parse visible job cards from HTML
                return _parse_indeed_html(content, query, cutoff)

            job_data = json.loads(m_data.group(1))
            for jk, jv in job_data.items():
                title = jv.get("title", "")
                company = jv.get("company", "Unknown")
                loc = jv.get("formattedLocation", "Brasil")
                date_ms = jv.get("pubDate") or jv.get("createDate")
                pub_dt = None
                if date_ms:
                    try:
                        pub_dt = datetime.fromtimestamp(date_ms / 1000, tz=timezone.utc)
                    except Exception:
                        pass

                if pub_dt and pub_dt < cutoff:
                    continue

                tl = title.lower()
                if any(ex in tl for ex in EXCLUDE_TERMS):
                    continue

                link = f"https://br.indeed.com/viewjob?jk={jk}"
                jobs.append({
                    "title": title,
                    "company": company,
                    "source": "Indeed Brasil",
                    "modality": "Remoto",
                    "location": loc,
                    "pub_date": pub_dt.strftime("%Y-%m-%d") if pub_dt else "Recente",
                    "url": link,
                    "description": jv.get("snippetHtml", ""),
                })

    except urllib.error.HTTPError as e:
        print(f"[Indeed] HTTPError {e.code} para query '{query}': {e.reason}", file=sys.stderr)
    except Exception as e:
        print(f"[Indeed] Erro para query '{query}': {e}", file=sys.stderr)

    return jobs


def _parse_indeed_html(html: str, query: str, cutoff: datetime) -> list:
    """
    Fallback parser para o HTML estático do Indeed quando o JSON embutido
    não está disponível (ex.: resposta sem JavaScript).
    """
    jobs = []
    decoded = html_lib.unescape(html)

    # Captura blocos de vagas pelo padrão de cards do Indeed
    card_pattern = re.compile(
        r'data-jk="([a-z0-9]+)"[^>]*>.*?'
        r'<span[^>]*class="[^"]*jobTitle[^"]*"[^>]*>.*?<span[^>]*>(.*?)</span>.*?'
        r'<span[^>]*class="[^"]*companyName[^"]*"[^>]*>(.*?)</span>',
        re.DOTALL | re.IGNORECASE
    )

    for m in card_pattern.finditer(decoded):
        jk = m.group(1)
        title = re.sub(r'<[^>]+>', '', m.group(2)).strip()
        company = re.sub(r'<[^>]+>', '', m.group(3)).strip()

        tl = title.lower()
        if any(ex in tl for ex in EXCLUDE_TERMS):
            continue

        # Keep only PM-relevant titles
        if not any(k in tl for k in [
            "project", "projetos", "programa", "program", "pmo",
            "delivery", "gerente", "gestor", "it manager"
        ]):
            continue

        link = f"https://br.indeed.com/viewjob?jk={jk}"
        jobs.append({
            "title": title,
            "company": company,
            "source": "Indeed Brasil",
            "modality": "Remoto",
            "location": "Brasil",
            "pub_date": "Recente",
            "url": link,
            "description": "",
        })

    return jobs


def search_indeed_all_queries(days: int = 7) -> list:
    """
    Executa todas as queries predefinidas no Indeed e retorna lista deduplicada.
    """
    seen_urls: set = set()
    all_jobs: list = []

    for query in INDEED_QUERIES:
        results = fetch_indeed_brasil(query, days=days)
        for j in results:
            if j["url"] not in seen_urls:
                seen_urls.add(j["url"])
                all_jobs.append(j)

    return all_jobs


if __name__ == "__main__":
    print("Testando busca no Indeed Brasil (últimos 7 dias)...")
    results = search_indeed_all_queries(days=7)
    print(f"Total vagas Indeed (deduplicadas): {len(results)}")
    for j in results:
        print(f"  [{j['pub_date']}] {j['title']} @ {j['company']} | {j['url']}")
