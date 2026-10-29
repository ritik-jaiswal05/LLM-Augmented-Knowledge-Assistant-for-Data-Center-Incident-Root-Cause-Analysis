"""Evaluation on held-out synthetic incidents. Prints a results table and saves results/results.json."""
import json, time, os
from rca import load_docs, chunk_docs, Index, keyword_baseline, analyze

tests = json.load(open("data/tests.json"))
chunks = chunk_docs(load_docs())
idx = Index(chunks)
K = 4
def cat_hit(hits, cat, k): return any(h["category"] == cat for h in hits[:k])
rows, t_ret = [], []
use_llm = bool(os.getenv("LLM_API_KEY"))
for t in tests:
    s = time.time(); hits = idx.search(t["query"], K); t_ret.append(time.time() - s)
    kb = keyword_baseline(chunks, t["query"], K)
    row = {"query": t["query"], "expected": t["category"],
           "sem_top1": hits[0]["category"] == t["category"], "sem_recall@k": cat_hit(hits, t["category"], K),
           "kw_top1": kb[0]["category"] == t["category"], "kw_recall@k": cat_hit(kb, t["category"], K)}
    if use_llm:
        out, _ = analyze(t["query"], idx, K)
        text = json.dumps(out.get("hypotheses", [])).lower()
        row["llm_top1_keyword"] = bool(out.get("hypotheses")) and t["keyword"] in json.dumps(out["hypotheses"][0]).lower()
        row["llm_topk_keyword"] = t["keyword"] in text
    rows.append(row)
n = len(rows)
def pct(key): return f"{100*sum(r[key] for r in rows)/n:.1f}% ({sum(r[key] for r in rows)}/{n})"
summary = {"backend": idx.backend, "n_cases": n, "k": K, "data": "synthetic",
           "semantic_top1_category": pct("sem_top1"), f"semantic_recall@{K}": pct("sem_recall@k"),
           "keyword_top1_category": pct("kw_top1"), f"keyword_recall@{K}": pct("kw_recall@k"),
           "avg_retrieval_latency_ms": round(1000*sum(t_ret)/n, 2)}
if use_llm: summary.update({"llm_top1_keyword_match": pct("llm_top1_keyword"), "llm_topk_keyword_match": pct("llm_topk_keyword")})
print(json.dumps(summary, indent=2))
for r in rows: print(("OK " if r["sem_top1"] else "MISS"), r["expected"], "|", r["query"][:70])
json.dump({"summary": summary, "rows": rows}, open("results/results.json", "w"), indent=2)
