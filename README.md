# AI Research RAG

A production-style Retrieval-Augmented Generation pipeline over 1,000+ AI documents
(arXiv papers, framework docs, engineering blogs), with hybrid search, reranking
and verified citations.

> Status: in progress (Day 2: data ingestion)

## Goals
- Answer questions about AI research with cited, verifiable sources
- Measure every pipeline stage instead of guessing (Recall@k, MRR, faithfulness)
- Show an ablation table: baseline vs hybrid vs reranked retrieval

## Pipeline
Ingestion -> Chunking -> Embeddings + BM25 index -> Hybrid search (RRF) -> Reranking -> Cited answers

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