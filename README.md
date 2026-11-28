# AI Research RAG

A production-style Retrieval-Augmented Generation pipeline over 1,000+ AI documents
(arXiv papers, framework docs, engineering blogs), with hybrid search, reranking
and verified citations.

> Status: in progress ( parsing and cleaning)

## Goals
- Answer questions about AI research with cited, verifiable sources
- Measure every pipeline stage instead of guessing (Recall@k, MRR, faithfulness)
- Show an ablation table: baseline vs hybrid vs reranked retrieval

## Pipeline
Ingestion -> Chunking -> Embeddings + BM25 index -> Hybrid search (RRF) -> Reranking -> Cited answers

## Corpus
| Source | Type | Documents |
|---|---|---|
| arXiv (cs.CL, cs.LG, cs.IR, 2023-2025) | PDF papers | X |
| Hugging Face docs (transformers, diffusers, peft, trl, accelerate, datasets) | Markdown | X |
| Hugging Face blog | Markdown | X |
| **Total** | | **X** |

Raw files are not stored in this repo. They are rebuilt by the scripts below.

## How to build the corpus
    python -m src.ingestion.arxiv_fetch        # arXiv PDFs + manifest
    python -m src.ingestion.docs_fetch         # framework docs + blog posts
    python -m src.ingestion.merge_manifests    # unified manifest_all.csv

Downloads respect arXiv's rate limit (one request per 3 seconds) and skip
files that already exist, so re-running is safe.

## Roadmap
- [x] Project skeleton
- [ ] Ingestion (arXiv, docs, blogs)
- [ ] Chunking strategies
- [ ] Indexing (vector + BM25)
- [ ] Hybrid search and reranking
- [ ] Evaluation and ablations
- [ ] Cited answer generation
- [ ] API, UI and Docker

## Project structure
- `src/ingestion/`: download and parse documents
- `src/chunking/`: chunking strategies
- `src/indexing/`: vector and keyword indexes
- `src/retrieval/`: hybrid search and reranking
- `src/generation/`: cited answers
- `src/evaluation/`: metrics and ablations

## Setup
    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt