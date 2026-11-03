#!/usr/bin/env python3
"""
tracker.py - Gerenciador de Histórico e Deduplicação de Vagas
Permite armazenar, verificar duplicatas e atualizar status de candidaturas de Humberto C. Garcia.
"""

import json
import os
import re
from datetime import datetime

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "tracker.json")

def load_tracker():
    if not os.path.exists(DATA_PATH):
        return {"last_updated": datetime.now().isoformat(), "total_tracked": 0, "jobs": []}
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"last_updated": datetime.now().isoformat(), "total_tracked": 0, "jobs": []}

def save_tracker(data):
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    data["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data["total_tracked"] = len(data.get("jobs", []))
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def _normalize_str(text):
    if not text:
        return ""
    return re.sub(r"\W+", "", text.lower())

def is_duplicate(title, company, url="", tracker_data=None):
    if tracker_data is None:
        tracker_data = load_tracker()
    
    norm_title = _normalize_str(title)
    norm_company = _normalize_str(company)
    
    for job in tracker_data.get("jobs", []):
        if url and job.get("url") and url.strip().rstrip("/") == job.get("url", "").strip().rstrip("/"):
            return True
        if _normalize_str(job.get("title")) == norm_title and _normalize_str(job.get("company")) == norm_company:
            return True
    return False

def add_job(title, company, modality, location, published_date, competition, fit, url, status="Identificada"):
    tracker = load_tracker()
    if is_duplicate(title, company, url, tracker):
        return False, "Vaga já existe no histórico."
    
    new_job = {
        "id": f"job-{len(tracker['jobs']) + 1:04d}",
        "title": title.strip(),
        "company": company.strip(),
        "modality": modality.strip(),
        "location": location.strip(),
        "published_date": published_date.strip(),
        "competition": competition.strip(),
        "fit": fit.strip(),
        "url": url.strip(),
        "status": status,
        "date_added": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    tracker["jobs"].append(new_job)
    save_tracker(tracker)
    return True, new_job

def list_jobs(status=None):
    tracker = load_tracker()
    jobs = tracker.get("jobs", [])
    if status:
        jobs = [j for j in jobs if j.get("status", "").lower() == status.lower()]
    return jobs

if __name__ == "__main__":
    import sys
    tracker = load_tracker()
    print(f"Total de vagas rastreadas: {tracker.get('total_tracked', 0)}")
    for j in tracker.get("jobs", []):
        print(f"[{j.get('id')}] {j.get('title')} @ {j.get('company')} | Fit: {j.get('fit')} | Status: {j.get('status')}")
