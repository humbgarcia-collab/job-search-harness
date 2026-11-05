# indeed_browser.py
"""
Scrape remote IT Project Manager jobs from Indeed Brazil using Playwright.
Uses direct search URLs with filters (Remote, published within last 7 days)
and extracts job title, company, location, date, and direct viewjob link.
"""

import json
import asyncio
import urllib.parse
from pathlib import Path
from playwright.async_api import async_playwright

INDEED_QUERIES = [
    "gerente de projetos ti",
    "project manager ti",
    "pmo",
    "gerente de infraestrutura ti"
]

OUTPUT_FILE = Path(__file__).parent / "indeed_jobs.json"

async def scrape_query(context, query: str):
    page = await context.new_page()
    jobs = []
    try:
        encoded_q = urllib.parse.quote_plus(query)
        # Direct URL: Remote location, fromage=7 (posted in last 7 days)
        url = f"https://br.indeed.com/jobs?q={encoded_q}&l=Remoto&fromage=7"
        print(f"[Indeed] Consultando: {url}")
        resp = await page.goto(url, timeout=40000, wait_until="domcontentloaded")
        await asyncio.sleep(2)
        
        cards = await page.query_selector_all("div.job_seen_beacon")
        print(f"[Indeed] Encontrados {len(cards)} cards para '{query}'")
        
        for card in cards:
            title_el = await card.query_selector("h2.jobTitle span, a[data-jk] span")
            title = await title_el.inner_text() if title_el else ""
            if not title:
                continue

            comp_el = await card.query_selector("[data-testid='company-name']")
            company = await comp_el.inner_text() if comp_el else "Empresa Confidencial"

            loc_el = await card.query_selector("[data-testid='text-location']")
            location = await loc_el.inner_text() if loc_el else "Remoto"

            date_el = await card.query_selector("[data-testid='myJobsStateDate']")
            date_str = await date_el.inner_text() if date_el else "Recente"

            link_el = await card.query_selector("a[data-jk]")
            jk = await link_el.get_attribute("data-jk") if link_el else ""
            job_url = f"https://br.indeed.com/viewjob?jk={jk}" if jk else ""

            if job_url:
                jobs.append({
                    "title": title.strip(),
                    "company": company.strip(),
                    "location": location.strip() if location else "Remoto",
                    "date": date_str.strip().replace("\n", " "),
                    "url": job_url,
                    "source": "Indeed",
                    "modality": "Remoto"
                })
    except Exception as e:
        print(f"[Indeed] Erro na busca por '{query}': {e}")
    finally:
        await page.close()
    return jobs

async def main():
    all_jobs = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-setuid-sandbox"
            ]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            locale="pt-BR"
        )

        for q in INDEED_QUERIES:
            jobs = await scrape_query(context, q)
            all_jobs.extend(jobs)
            await asyncio.sleep(1)

        await browser.close()

    # Deduplicação por URL
    seen = set()
    unique_jobs = []
    for job in all_jobs:
        if job["url"] not in seen:
            seen.add(job["url"])
            unique_jobs.append(job)

    OUTPUT_FILE.write_text(json.dumps(unique_jobs, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[Indeed OK] Total de vagas extraídas e salvas: {len(unique_jobs)} em {OUTPUT_FILE}")
    return unique_jobs

if __name__ == "__main__":
    asyncio.run(main())
