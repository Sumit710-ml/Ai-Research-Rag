import csv
import time
from pathlib import Path

import feedparser
import requests

API_URL = "https://export.arxiv.org/api/query"
RAW_DIRT = Path("data/raw/arxiv")
MANIFEST = Path("data/manifest.csv")
CATEGORIES = ["cs.CL", "cs.LG", "cs.IR"]
YEARS = [2023, 2024, 2025]
PER_GROUP = 90
DELAY = 3 # request rate rule. MANDATORY

def fetch_listing(category,year,n):
    query = f"cat:{category} AND submitted Date:[{year}01010000 TO {year}12312359]"
    params = {
        "search_query":query,
        "start":0,
        "max_results":n,
        "sortBy":"submittedDate",
        "sortOrder":"descending",
    }
    resp = requests.get(API_URL,params=params,timeout=30)
    resp.raise_for_status()
    feed = feedparser.parse(resp.text)

    papers = []
    for e in feed.entries:
        arxiv_id = e.id.split("/abs/")[-1]
        papers.append({
            "arxiv_id":arxiv_id,
            "title":" ".join(e.title.split()),
            "published":e.published[:10],
            "category":category,
            "pdf_url":f"https://arxiv.org/pdf/{arxiv_id}.pdf",            
            "local_path":str(RAW_DIRT / f"{arxiv_id}.pdf"),
        })
    return papers    

def write_manifest(papers):
    MANIFEST.parent.mkdir(parents=True,exist_ok=True)
    with open(MANIFEST,"w",newline="",encoding="utf-8") as f:
        writer = csv.DictWriter(f,fieldnames=list(papers[0].keys()))
        writer.writeheader()
        writer.writerows(papers)
def download_pdf(paper):
    path = Path(paper["local_path"])
    if path.exists():
        return False
    resp = requests.get(paper["pdf_url"],timeout=60)
    resp.raise_for_status()
    path.write_bytes(resp.content)
    return True