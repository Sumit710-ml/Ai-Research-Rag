import csv
import random
import shutil
import subprocess
from pathlib import Path

TMP_DIR = Path("data/tmp_repos")
RAW_DIR = Path("data/raw")
MANIFEST = Path("data/manifest_docs.csv")

SOURCES = [
    {"repo": "huggingface/transformers", "sparse": ["/docs/source/en/"], "type": "framework_doc", "out": "docs/transformers", "limit": 150},
    {"repo": "huggingface/diffusers", "sparse": ["/docs/source/en/"], "type": "framework_doc", "out": "docs/diffusers", "limit": 100},
    {"repo": "huggingface/peft", "sparse": ["/docs/source/"], "type": "framework_doc", "out": "docs/peft", "limit": 60},
    {"repo": "huggingface/trl", "sparse": ["/docs/source/"], "type": "framework_doc", "out": "docs/trl", "limit": 40},
    {"repo": "huggingface/accelerate", "sparse": ["/docs/source/"], "type": "framework_doc", "out": "docs/accelerate", "limit": 60},
    {"repo": "huggingface/datasets", "sparse": ["/docs/source/"], "type": "framework_doc", "out": "docs/datasets", "limit": 60},
    {"repo": "huggingface/blog", "sparse": ["/*.md"], "type": "blog", "out": "blogs/huggingface", "limit": 200},   
]

def run(cmd):
    subprocess.run(cmd, check=True)


def clone_sparse(repo, patterns):
    dest = TMP_DIR / repo.replace("/", "__")
    if dest.exists():
        return dest
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    run(["git", "clone", "--depth", "1", "--filter=blob:none", "--sparse",
         f"https://github.com/{repo}.git", str(dest)])
    run(["git", "-C", str(dest), "sparse-checkout", "set", "--no-cone", *patterns])
    return dest
def get_title(path):
    text = path.read_text(encoding="utf-8", errors="ignore")
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem
def collect(source):
    repo = source["repo"]
    repo_dir = clone_sparse(repo, source["sparse"])

    files = [p for p in repo_dir.rglob("*.md")
             if p.name.lower() != "readme.md" and ".git" not in p.parts]
    files.sort()
    if len(files) > source["limit"]:
        files = random.Random(42).sample(files, source["limit"])
        files.sort()

    rows = []
    for path in files:
        rel = path.relative_to(repo_dir).as_posix()
        dest = RAW_DIR / source["out"] / rel.replace("/", "__")
        dest.parent.mkdir(parents=True, exist_ok=True)
        if not dest.exists():
            shutil.copy(path, dest)
        rows.append({
            "doc_id": f"{repo}/{rel}",
            "title": get_title(path),
            "source_type": source["type"],
            "source": repo,
            "url": f"https://github.com/{repo}/blob/main/{rel}",
            "local_path": str(dest),
        })
    return rows