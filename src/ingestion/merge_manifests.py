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
