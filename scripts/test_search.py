import urllib.request
import re

urls = [
    'https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH9pAQOwZkasRXvmaL3HyxZmCAcPB8wvgHHDtIh1-CcP0PiYBTMFSuz27q4DIcfZ0dYFeWq84rGq5sO1edBxGPSarq-D_tmIxuFWSidzNKEs2bBtCUIVEljzfaEK1ib1tMlsiWRdtYmS-Fq',
    'https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHQKPn-JQHOgLwUtGItvt-h-9g4jL7KhyH6ZYmVpmzqBHyA7ll98B15IJC1cZe0btrlo4oOzEhOPYn53uvWRcbdzQDdcst7HyNSNrKZ3qLlD7VE22MnMjTF3WBJeoyF7jaM_lMh29qdESwewWR2qNTUriAGeKY9c9j86fI1Zbgc',
    'https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHfBr9m1ekmFKepeEUBeKfDrFEVI_nT-V3IJleQWi4W3XwEd_oQXicj2_z557Kw7VQ_RPp13UfQlnU7nj3wNl7xhqlKgWILu9L3fu7m2QtFzaqrJiiquG1BoCWUoNSyEtsc80WzFjpv7hE2idd-uaAJAdDdBX8='
]

for u in urls:
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req, timeout=10)
        print("Resolved:", res.geturl())
    except Exception as e:
        print(f"Error {u}: {e}")
