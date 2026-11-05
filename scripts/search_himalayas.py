import urllib.request
import json
from datetime import datetime, timezone, timedelta
import sys

sys.stdout.reconfigure(encoding='utf-8')

cutoff = datetime.now(timezone.utc) - timedelta(days=7)
print("Cutoff date:", cutoff.strftime("%Y-%m-%d"))

all_jobs = []
for offset in range(0, 200, 20):
    url = f"https://himalayas.app/jobs/api?offset={offset}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode('utf-8'))
            jobs = data.get('jobs', [])
            if not jobs: break
            
            stop_paging = False
            for j in jobs:
                pub_ts = j.get('pubDate')
                pub_dt = datetime.fromtimestamp(pub_ts, tz=timezone.utc) if pub_ts else None
                if pub_dt and pub_dt < cutoff:
                    stop_paging = True
                    break
                
                title = j.get('title', '')
                tl = title.lower()
                if any(kw in tl for kw in ['project manager', 'program manager', 'pmo', 'delivery manager', 'agile', 'scrum master', 'operations manager', 'it manager', 'director of engineering']):
                    link = j.get('applicationLink') or f"https://himalayas.app/jobs/{j.get('slug', '')}"
                    loc = ", ".join(j.get('locationRestrictions', [])) or "Worldwide / Remoto"
                    print(f"[{pub_dt.strftime('%Y-%m-%d') if pub_dt else 'N/A'}] {title} @ {j.get('companyName')} | Loc: {loc} | {link}")
                    all_jobs.append(j)
            if stop_paging:
                break
    except Exception as e:
        print(f"Error at offset {offset}: {e}")
        break

print(f"Total PM/Ops jobs found in Himalayas: {len(all_jobs)}")
