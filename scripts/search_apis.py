#!/usr/bin/env python3
"""
search_apis.py - Módulo de consulta de vagas remotas via APIs públicas e feeds RSS.
Fontes: Himalayas API, WeWorkRemotely RSS, RemoteOK API, Arbeitnow API.
"""

import json
import os
import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) JobSearchHarness/1.0"

DEFAULT_KEYWORDS = [
    "project manager",
    "gerente de projetos",
    "pmo",
    "program manager",
    "delivery manager",
    "it project",
    "infrastructure project",
    "cloud project",
    "scrum master"
]

EXCLUDE_TERMS = [
    "intern",
    "estagiário",
    "estágio",
    "junior",
    "júnior",
    "entry level",
    "construction",
    "obras",
    "civil"
]

def get_headers():
    return {"User-Agent": USER_AGENT}

def fetch_himalayas(days=7):
    jobs = []
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    try:
        url = "https://himalayas.app/jobs/api?limit=100"
        req = urllib.request.Request(url, headers=get_headers())
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode())
            for item in data.get("jobs", []):
                title = item.get("title", "")
                company = item.get("companyName", "")
                pub_ts = item.get("pubDate")
                
                # Check date
                pub_dt = None
                if pub_ts:
                    try:
                        pub_dt = datetime.fromtimestamp(pub_ts, tz=timezone.utc)
                    except Exception:
                        pass
                
                if pub_dt and pub_dt < cutoff:
                    continue
                
                link = item.get("applicationLink") or f"https://himalayas.app/jobs/{item.get('slug', '')}"
                loc = ", ".join(item.get("locationRestrictions", [])) or "Worldwide / Remoto"
                
                jobs.append({
                    "title": title,
                    "company": company,
                    "source": "Himalayas",
                    "modality": "Remoto",
                    "location": loc,
                    "pub_date": pub_dt.strftime("%Y-%m-%d") if pub_dt else "Recente",
                    "url": link,
                    "description": item.get("excerpt", "")
                })
    except Exception as e:
        print(f"[Aviso] Erro ao consultar Himalayas: {e}")
    return jobs

def fetch_remoteok(days=7):
    jobs = []
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    try:
        url = "https://remoteok.com/api"
        req = urllib.request.Request(url, headers=get_headers())
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode())
            for item in data[1:]:  # O primeiro item é aviso legal
                title = item.get("position", "")
                company = item.get("company", "")
                date_str = item.get("date")
                
                pub_dt = None
                if date_str:
                    try:
                        pub_dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                    except Exception:
                        pass
                
                if pub_dt and pub_dt < cutoff:
                    continue
                
                link = item.get("url") or item.get("apply_url")
                loc = item.get("location") or "Worldwide / Remoto"
                
                jobs.append({
                    "title": title,
                    "company": company,
                    "source": "Remote OK",
                    "modality": "Remoto",
                    "location": loc,
                    "pub_date": pub_dt.strftime("%Y-%m-%d") if pub_dt else "Recente",
                    "url": link,
                    "description": item.get("description", "")[:300]
                })
    except Exception as e:
        print(f"[Aviso] Erro ao consultar Remote OK: {e}")
    return jobs

def fetch_weworkremotely(days=7):
    jobs = []
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    feeds = [
        "https://weworkremotely.com/categories/remote-management-and-finance-jobs.rss",
        "https://weworkremotely.com/remote-jobs.rss"
    ]
    for feed in feeds:
        try:
            req = urllib.request.Request(feed, headers=get_headers())
            with urllib.request.urlopen(req, timeout=12) as resp:
                root = ET.fromstring(resp.read())
                channel = root.find("channel")
                if channel is None:
                    continue
                for item in channel.findall("item"):
                    raw_title = item.find("title").text or ""
                    parts = raw_title.split(":", 1)
                    if len(parts) == 2:
                        company = parts[0].strip()
                        title = parts[1].strip()
                    else:
                        company = "WWR"
                        title = raw_title
                    
                    pub_str = item.find("pubDate").text if item.find("pubDate") is not None else ""
                    pub_dt = None
                    if pub_str:
                        try:
                            # RFC 822 format: e.g. Mon, 02 Nov 2026 07:31:12 +0000
                            pub_dt = datetime.strptime(pub_str[:25], "%a, %d %b %Y %H:%M:%S").replace(tzinfo=timezone.utc)
                        except Exception:
                            pass
                    
                    if pub_dt and pub_dt < cutoff:
                        continue
                    
                    link = item.find("link").text if item.find("link") is not None else ""
                    
                    jobs.append({
                        "title": title,
                        "company": company,
                        "source": "We Work Remotely",
                        "modality": "Remoto",
                        "location": "Global / Remoto",
                        "pub_date": pub_dt.strftime("%Y-%m-%d") if pub_dt else "Recente",
                        "url": link,
                        "description": item.find("description").text[:300] if item.find("description") is not None else ""
                    })
        except Exception as e:
            print(f"[Aviso] Erro ao consultar We Work Remotely ({feed}): {e}")
    return jobs

def fetch_arbeitnow(days=7):
    jobs = []
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    try:
        url = "https://www.arbeitnow.com/api/job-board-api"
        req = urllib.request.Request(url, headers=get_headers())
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode())
            for item in data.get("data", []):
                if not item.get("remote", False):
                    continue
                title = item.get("title", "")
                company = item.get("company_name", "")
                created_at = item.get("created_at")
                
                pub_dt = None
                if created_at:
                    try:
                        pub_dt = datetime.fromtimestamp(created_at, tz=timezone.utc)
                    except Exception:
                        pass
                
                if pub_dt and pub_dt < cutoff:
                    continue
                
                link = item.get("url")
                loc = item.get("location") or "Remoto"
                
                jobs.append({
                    "title": title,
                    "company": company,
                    "source": "Arbeitnow",
                    "modality": "Remoto",
                    "location": loc,
                    "pub_date": pub_dt.strftime("%Y-%m-%d") if pub_dt else "Recente",
                    "url": link,
                    "description": item.get("description", "")[:300]
                })
    except Exception as e:
        print(f"[Aviso] Erro ao consultar Arbeitnow: {e}")
    return jobs

def filter_jobs(raw_jobs, keywords=None, exclude_terms=None):
    if keywords is None:
        keywords = DEFAULT_KEYWORDS
    if exclude_terms is None:
        exclude_terms = EXCLUDE_TERMS
        
    filtered = []
    for j in raw_jobs:
        title_lower = j["title"].lower()
        desc_lower = j.get("description", "").lower()
        
        # Exclusão
        if any(term in title_lower for term in exclude_terms):
            continue
            
        # Correspondência de cargo-alvo
        match = any(kw in title_lower for kw in keywords) or ("project manager" in desc_lower and "manager" in title_lower)
        if match:
            filtered.append(j)
    return filtered

def search_all_open_sources(days=7):
    all_raw = []
    all_raw.extend(fetch_himalayas(days=days))
    all_raw.extend(fetch_remoteok(days=days))
    all_raw.extend(fetch_weworkremotely(days=days))
    all_raw.extend(fetch_arbeitnow(days=days))
    
    filtered = filter_jobs(all_raw)
    return filtered

if __name__ == "__main__":
    print("Executando busca teste em APIs públicas (últimos 7 dias)...")
    res = search_all_open_sources(days=7)
    print(f"Total encontradas que batem com cargos-alvo: {len(res)}")
    for j in res:
        print(f"- [{j['source']}] {j['title']} @ {j['company']} ({j['pub_date']}) - {j['url']}")
