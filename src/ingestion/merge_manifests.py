import csv
from pathlib import Path

ARXIV_MANIFEST = Path("data/manifest.csv")
DOCS_MANIFEST = Path("data/manifest_docs.csv")
OUT = Path("data/manifest_all.csv")
FIELDS = ["doc_id", "title", "source_type", "source", "url",
          "local_path", "file_type", "published"]


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))
def from_arxiv(row):
    return {
        "doc_id": f"arxiv:{row['arxiv_id']}",
        "title": row["title"],
        "source_type": "paper",
        "source": "arxiv",
        "url": f"https://arxiv.org/abs/{row['arxiv_id']}",
        "local_path": row["local_path"],
        "file_type": "pdf",
        "published": row["published"],
    }