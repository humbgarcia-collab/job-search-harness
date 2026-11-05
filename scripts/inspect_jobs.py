import urllib.request
import re

urls = [
    'https://montreal.gupy.io/jobs/12715928',
    'https://globalhitss.gupy.io/jobs/12502006',
    'https://dc.gupy.io/job/eyJqb2JJZCI6MTI4MjUzMDIsInNvdXJjZSI6Imd1cHlfcG9ydGFsIn0='
]

for u in urls:
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8')
        title = re.findall(r'<title>(.*?)</title>', html)
        wp = re.findall(r'workplaceType["\s:]+([^,}"]+)', html)
        loc = re.findall(r'addressLocality["\s:]+([^,}"]+)', html)
        date = re.findall(r'datePosted["\s:]+([^,}"]+)', html)
        desc = re.findall(r'description["\s:]+([^"]{50,200})', html)
        print('URL:', u)
        print('Title:', title)
        print('Workplace:', wp)
        print('Loc:', loc)
        print('Date:', date)
        print('---')
    except Exception as e:
        print(u, 'Error:', e)
