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
def from_docs(row):
    return {**row, "file_type": "md", "published": ""}
def main():
    rows = [from_arxiv(r) for r in read_csv(ARXIV_MANIFEST)]
    rows += [from_docs(r) for r in read_csv(DOCS_MANIFEST)]

    present = [r for r in rows if Path(r["local_path"]).exists()]
    print(f"{len(present)} of {len(rows)} files exist on disk")

    with open(OUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(present)

    counts = {}
    for r in present:
        counts[r["source_type"]] = counts.get(r["source_type"], 0) + 1
    print(counts)


if __name__ == "__main__":
    main()