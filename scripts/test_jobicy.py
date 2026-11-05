import urllib.request
import json
import sys

# Force UTF-8 stdout
sys.stdout.reconfigure(encoding='utf-8')

geos = ['', 'latam', 'brazil', 'usa', 'emea', 'apac']
seen_urls = set()

for g in geos:
    geo_param = f"&geo={g}" if g else ""
    url = f"https://jobicy.com/api/v2/remote-jobs?count=100{geo_param}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            d = json.loads(r.read().decode('utf-8'))
            jobs = d.get('jobs', [])
            for j in jobs:
                u = j.get('url')
                if u in seen_urls: continue
                seen_urls.add(u)
                
                title = j.get('jobTitle', '')
                tl = title.lower()
                # Targets: project manager, pmo, program manager, delivery manager, it project
                if any(k in tl for k in ['project manager', 'program manager', 'pmo', 'delivery manager', 'it manager', 'infrastructure manager', 'transformation manager', 'scrum master']):
                    print(f"[{j.get('pubDate')[:10]}] {title} @ {j.get('companyName')} | Geo: {j.get('jobGeo')} | {u}")
    except Exception as e:
        print(f"Error {g}: {e}")
