import urllib.request
import re
import html as html_lib
import sys

sys.stdout.reconfigure(encoding='utf-8')

urls = [
    'https://intelipost.gupy.io/jobs/12787012',
    'https://stefanini.gupy.io/jobs/12819691'
]

for u in urls:
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
        content = urllib.request.urlopen(req, timeout=10).read().decode('utf-8', errors='ignore')
        decoded = html_lib.unescape(content)
        text = re.sub(r'<[^>]+>', ' ', decoded)
        text = ' '.join(text.split())
        title = re.search(r'<title>(.*?)</title>', content)
        print("URL:", u)
        print("Title:", title.group(1) if title else "N/A")
        idx_r = text.find("Responsabilidades e atribuições")
        if idx_r != -1:
            print("Resp:", text[idx_r:idx_r+350])
        idx_q = text.find("Requisitos e qualificações")
        if idx_q != -1:
            print("Req:", text[idx_q:idx_q+350])
        print("---")
    except Exception as e:
        print(f"Error {u}: {e}")
