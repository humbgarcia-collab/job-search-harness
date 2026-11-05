import urllib.request
import re
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

urls = [
    'https://jobicy.com/jobs/158742-technical-program-manager-data-centers-2',
    'https://jobicy.com/jobs/158067-enterprise-project-manager-2',
    'https://himalayas.app/companies/nearshore-business-solutions/jobs/project-manager?utm_source=api'
]

for u in urls:
    req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        html = urllib.request.urlopen(req, timeout=12).read().decode('utf-8', errors='ignore')
        title = re.search(r'<title>(.*?)</title>', html)
        print("URL:", u)
        print("Title:", title.group(1) if title else "N/A")
        # Check apply link
        apply_links = re.findall(r'href="([^"]*(?:apply|lever|greenhouse|workable)[^"]*)"', html, re.IGNORECASE)
        print("Apply links:", apply_links[:3])
        print("---")
    except Exception as e:
        print(f"Error {u}: {e}")
