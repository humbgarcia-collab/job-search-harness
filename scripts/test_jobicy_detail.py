import urllib.request
import re

url = 'https://jobicy.com/jobs/158742-technical-program-manager-data-centers-2'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8', errors='ignore')
buttons = re.findall(r'<a[^>]*class="[^"]*apply[^"]*"[^>]*href="([^"]+)"', html, re.IGNORECASE)
print("Apply buttons:", buttons)
links = re.findall(r'href="([^"]+)"', html)
external = [l for l in links if 'jobicy.com' not in l and l.startswith('http')]
print("External links:", external[:5])
