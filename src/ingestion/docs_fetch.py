import csv
import random
import shutil
import subprocess
from pathlib import Path

TNP_DIR = Path("data/tmp_repos")
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