"""
knowledge/search.py — Offline knowledge-base search for SolaraAI.

Usage:
    from knowledge.search import search_kb
    results = search_kb("python decorators", top_k=5)
"""
from __future__ import annotations

import os
import re
import math
from pathlib import Path
from typing import List, Tuple, Optional

# ── constants ────────────────────────────────────────────────────────────────

KB_DIR = Path(__file__).parent.parent / "knowledge_base"

# Max chars to show per result snippet
SNIPPET_LEN = 400

# Stop-words to skip in scoring
STOP = frozenset({
    "a", "an", "the", "is", "it", "in", "on", "at", "to", "for",
    "of", "and", "or", "but", "not", "with", "this", "that", "are",
    "was", "be", "as", "by", "from", "do", "so", "if", "its",
})


# ── tokeniser ────────────────────────────────────────────────────────────────

def _tokenize(text: str) -> List[str]:
    """Lowercase, strip punctuation, split into words. Filters stop-words."""
    words = re.findall(r"[a-z0-9_]+", text.lower())
    return [w for w in words if w not in STOP and len(w) > 1]


# ── BM25-lite scorer ─────────────────────────────────────────────────────────

def _bm25_score(
    query_terms: List[str],
    doc_words: List[str],
    avg_dl: float,
    k1: float = 1.5,
    b: float = 0.75,
) -> float:
    """Lightweight BM25 score — no IDF (single-doc scoring)."""
    if not doc_words:
        return 0.0
    dl = len(doc_words)
    freq: dict = {}
    for w in doc_words:
        freq[w] = freq.get(w, 0) + 1

    score = 0.0
    for term in query_terms:
        tf = freq.get(term, 0)
        if tf == 0:
            continue
        tf_norm = (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * dl / max(avg_dl, 1)))
        score += tf_norm
    return score


# ── snippet extractor ────────────────────────────────────────────────────────

def _best_snippet(text: str, query_terms: List[str], length: int = SNIPPET_LEN) -> str:
    """
    Return the excerpt of `text` that contains the most query hits.
    Falls back to the first `length` chars if no hits found.
    """
    lower = text.lower()
    best_pos = 0
    best_hits = 0

    step = max(length // 4, 50)
    for start in range(0, max(1, len(text) - length), step):
        window = lower[start: start + length]
        hits = sum(1 for t in query_terms if t in window)
        if hits > best_hits:
            best_hits = hits
            best_pos = start

    snippet = text[best_pos: best_pos + length].strip()
    # Clean up leading partial lines
    nl = snippet.find("\n")
    if 0 < nl < 60:
        snippet = snippet[nl:].strip()
    return snippet[:length]


# ── main search function ──────────────────────────────────────────────────────

def search_kb(
    query: str,
    top_k: int = 5,
    subdir: Optional[str] = None,
) -> List[dict]:
    """
    Search the local knowledge base for `query`.

    Args:
        query:   Search string (keywords or natural language)
        top_k:   Max results to return
        subdir:  Optional subdirectory to limit search (e.g. "python", "ai_ml")

    Returns:
        List of result dicts:
        {
            "file":    relative path from knowledge_base/,
            "score":   float relevance score,
            "title":   first heading found in the file,
            "snippet": best matching excerpt,
        }
    """
    if not KB_DIR.exists():
        return [{"error": f"Knowledge base not found at {KB_DIR}"}]

    query_terms = _tokenize(query)
    if not query_terms:
        return []

    search_root = KB_DIR / subdir if subdir else KB_DIR
    if not search_root.exists():
        return [{"error": f"Subdir '{subdir}' not found in knowledge base"}]

    # Collect all markdown files
    md_files = list(search_root.rglob("*.md"))
    if not md_files:
        return []

    # Estimate avg document length for BM25
    sample_size   = min(50, len(md_files))
    sample_words  = 0
    for f in md_files[:sample_size]:
        try:
            sample_words += len(f.read_text(encoding="utf-8", errors="ignore").split())
        except Exception:
            pass
    avg_dl = sample_words / max(sample_size, 1)

    # Score all files
    results = []
    for fpath in md_files:
        try:
            raw = fpath.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        doc_words = _tokenize(raw)
        score     = _bm25_score(query_terms, doc_words, avg_dl)
        if score <= 0:
            continue

        # Extract title (first # heading)
        title_match = re.search(r"^#\s+(.+)", raw, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else fpath.stem.replace("_", " ").title()

        snippet = _best_snippet(raw, query_terms)
        rel     = str(fpath.relative_to(KB_DIR)).replace("\\", "/")

        results.append({
            "file":    rel,
            "score":   round(score, 3),
            "title":   title,
            "snippet": snippet,
        })

    results.sort(key=lambda r: r["score"], reverse=True)
    return results[:top_k]


# ── CLI helper ───────────────────────────────────────────────────────────────

def format_results(results: List[dict], query: str, colors: Optional[dict] = None) -> str:
    """Format search results for terminal display."""
    c = colors or {}
    CYAN   = c.get("CYAN",   "\033[36m")
    YELLOW = c.get("YELLOW", "\033[33m")
    GRAY   = c.get("GRAY",   "\033[90m")
    BOLD   = c.get("BOLD",   "\033[1m")
    DIM    = c.get("DIM",    "\033[2m")
    GREEN  = c.get("GREEN",  "\033[32m")
    RESET  = c.get("RESET",  "\033[0m")

    if not results:
        return f"\n  {YELLOW}No results found for: {BOLD}{query}{RESET}\n"

    if "error" in results[0]:
        return f"\n  {YELLOW}⚠  {results[0]['error']}{RESET}\n"

    lines = [
        "",
        f"  {BOLD}{CYAN}◈  KNOWLEDGE BASE SEARCH{RESET}",
        f"  {GRAY}Query: {BOLD}{query}{RESET}  {GRAY}│  {len(results)} result(s){RESET}",
        f"  {GRAY}{'─' * 60}{RESET}",
        "",
    ]

    for i, r in enumerate(results, 1):
        lines += [
            f"  {BOLD}{CYAN}[{i}] {r['title']}{RESET}",
            f"  {DIM}{GRAY}📁 {r['file']}   score={r['score']}{RESET}",
            "",
        ]
        # Show snippet, indented, code blocks highlighted
        for line in r["snippet"].split("\n")[:12]:
            if line.startswith("```"):
                lines.append(f"  {DIM}{GRAY}{line}{RESET}")
            elif line.startswith("#"):
                lines.append(f"  {GREEN}{line}{RESET}")
            else:
                lines.append(f"  {GRAY}{line}{RESET}")
        lines += ["", f"  {GRAY}{'─' * 60}{RESET}", ""]

    return "\n".join(lines)


# ── standalone test ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    q = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "python decorators"
    print(f"Searching for: {q!r}")
    hits = search_kb(q, top_k=5)
    print(format_results(hits, q))
