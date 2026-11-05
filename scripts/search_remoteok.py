import urllib.request
import json
from datetime import datetime, timezone, timedelta
import sys

sys.stdout.reconfigure(encoding='utf-8')

cutoff = datetime.now(timezone.utc) - timedelta(days=7)
url = "https://remoteok.com/api"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

try:
    with urllib.request.urlopen(req, timeout=12) as r:
        data = json.loads(r.read().decode('utf-8'))
        print(f"Total RemoteOK items: {len(data)-1}")
        for item in data[1:]:
            title = item.get("position", "")
            date_str = item.get("date")
            pub_dt = None
            if date_str:
                try:
                    pub_dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                except Exception:
                    pass
            
            if pub_dt and pub_dt < cutoff:
                continue
            
            # Print if any relevance
            tl = title.lower()
            tags = [t.lower() for t in item.get('tags', [])]
            if any(k in tl for k in ['manager', 'pmo', 'agile', 'scrum', 'lead', 'operations', 'project', 'program']) or any('project' in t for t in tags):
                print(f"[{pub_dt.strftime('%Y-%m-%d') if pub_dt else 'N/A'}] {title} @ {item.get('company')} | Loc: {item.get('location')} | URL: {item.get('url')}")
except Exception as e:
    print(f"Error RemoteOK: {e}")
