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