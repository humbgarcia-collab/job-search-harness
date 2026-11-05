import urllib.request
import json
from datetime import datetime, timezone, timedelta
from scripts.search_apis import fetch_himalayas, fetch_remoteok, fetch_weworkremotely, fetch_arbeitnow

h_jobs = fetch_himalayas(days=7)
r_jobs = fetch_remoteok(days=7)
w_jobs = fetch_weworkremotely(days=7)
a_jobs = fetch_arbeitnow(days=7)

all_j = h_jobs + r_jobs + w_jobs + a_jobs
print(f"Total jobs in 7 days: {len(all_j)}")
print(f"Himalayas: {len(h_jobs)}, RemoteOK: {len(r_jobs)}, WWR: {len(w_jobs)}, Arbeitnow: {len(a_jobs)}")

for j in all_j:
    t = j['title']
    print(f"[{j['source']}] {t} | Company: {j['company']} | Loc: {j['location']} | Date: {j['pub_date']}")
