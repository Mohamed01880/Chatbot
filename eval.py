"""Évalue le classement des fiches sans générer de réponse avec un LLM.

Usage : python eval.py
Indicateurs : Hit@1 / Hit@3 / Hit@4 (la bonne section est-elle dans les N premiers ?) et MRR."""
# Cette ligne importe les dépendances nécessaires : import json.
import json
# Cette ligne importe les dépendances nécessaires : import argparse.
import argparse
# Cette ligne importe les dépendances nécessaires : import os.
import os
# Cette ligne importe les dépendances nécessaires : from pathlib import Path.
from pathlib import Path
# Cette ligne importe les dépendances nécessaires : from dotenv import load_dotenv.
from dotenv import load_dotenv

# Cette ligne importe les dépendances nécessaires : from rag import BM25, GeminiReranker, HybridSearch, load_chunks.
from rag import BM25, GeminiReranker, HybridSearch, load_chunks

# Cette ligne affecte la variable `BASE` avec `Path(__file__).parent`.
BASE = Path(__file__).parent
# Cette ligne exécute `load_dotenv(BASE / ".env")` dans le traitement courant.
load_dotenv(BASE / ".env")
# Cette ligne affecte la variable `parser` avec `argparse.ArgumentParser(description="Évaluation de la recherche sans LLM")`.
parser = argparse.ArgumentParser(description="Évaluation de la recherche sans LLM")
# Cette ligne exécute `parser.add_argument("--mode", choices=("bm25", "hybrid", "hybrid-rerank"), default="bm25")` dans le traitement courant.
parser.add_argument("--mode", choices=("bm25", "hybrid", "hybrid-rerank"), default="bm25")
# Cette ligne affecte la variable `args` avec `parser.parse_args()`.
args = parser.parse_args()
# Cette ligne affecte les passages extraits des fiches avec `load_chunks(BASE / "fiches")`.
chunks = load_chunks(BASE / "fiches")
# Cette ligne affecte le moteur de recherche documentaire avec `BM25(chunks) if args.mode == "bm25" else HybridSearch(`.
index = BM25(chunks) if args.mode == "bm25" else HybridSearch(
    # Cette ligne exécute `chunks, min_similarity=float(os.getenv("RAG_MIN_SIMILARITY", "0.3")),` dans le traitement courant.
    chunks, min_similarity=float(os.getenv("RAG_MIN_SIMILARITY", "0.3")),
    # Cette ligne affecte la variable `reranker` avec `GeminiReranker() if args.mode == "hybrid-rerank" else None,`.
    reranker=GeminiReranker() if args.mode == "hybrid-rerank" else None,
    # Cette ligne affecte la variable `rerank_candidates` avec `int(os.getenv("RERANK_CANDIDATES", "20")))`.
    rerank_candidates=int(os.getenv("RERANK_CANDIDATES", "20")))
# Cette ligne vérifie la condition `isinstance(index, HybridSearch)` avant d’exécuter le bloc.
if isinstance(index, HybridSearch):
    # Cette ligne exécute `index.prepare()` dans le traitement courant.
    index.prepare()
    # Cette ligne vérifie la condition `not index.status()["ready"]` avant d’exécuter le bloc.
    if not index.status()["ready"]:
        # Cette ligne signale l’erreur `SystemExit("Embeddings indisponibles : impossible d'évaluer le mode hybride.")` et interrompt le traitement courant.
        raise SystemExit("Embeddings indisponibles : impossible d'évaluer le mode hybride.")
# Cette ligne affecte les données reçues avec `json.loads((BASE / "tests" / "questions.json").read_text(encoding="utf-8"))`.
data = json.loads((BASE / "tests" / "questions.json").read_text(encoding="utf-8"))


# Cette définition sert à Renvoie le rang du premier passage correspondant à une section attendue .
def rank_of(question, expected, k=6):
    """Renvoie le rang du premier passage correspondant à une section attendue."""
    # Cette ligne affecte les passages trouvés par la recherche avec `index.search(question, k=k)`.
    hits = index.search(question, k=k)
    # Cette ligne vérifie la condition `isinstance(index, HybridSearch) and index.reranker and index.reranker.error` avant d’exécuter le bloc.
    if isinstance(index, HybridSearch) and index.reranker and index.reranker.error:
        # Cette ligne signale l’erreur `SystemExit("Reranker indisponible ; évaluation annulée pour éviter un résultat trompeur.")` et interrompt le traitement courant.
        raise SystemExit("Reranker indisponible ; évaluation annulée pour éviter un résultat trompeur.")
    # Cette ligne vérifie la condition `isinstance(index, HybridSearch) and index.error` avant d’exécuter le bloc.
    if isinstance(index, HybridSearch) and index.error:
        # Cette ligne signale l’erreur `SystemExit("Embeddings indisponibles pendant l'évaluation ; résultats invalides.")` et interrompt le traitement courant.
        raise SystemExit("Embeddings indisponibles pendant l'évaluation ; résultats invalides.")
    # Cette ligne parcourt `i, (_, c) in enumerate(hits, start=1)` pour traiter chaque élément.
    for i, (_, c) in enumerate(hits, start=1):
        # Cette ligne vérifie la condition `any(c.doc_id == d and s.lower() in c.section.lower() for d, s in expected)` avant d’exécuter le bloc.
        if any(c.doc_id == d and s.lower() in c.section.lower() for d, s in expected):
            # Cette ligne renvoie `i` au code qui a appelé la fonction.
            return i
    # Cette ligne renvoie `None` au code qui a appelé la fonction.
    return None


# Cette ligne affecte la variable `rows` avec `[(it, rank_of(it["question"], it["expected"])) for it in data["answerable"]]`.
rows = [(it, rank_of(it["question"], it["expected"])) for it in data["answerable"]]
# Cette ligne vérifie la condition `isinstance(index, HybridSearch) and index.error` avant d’exécuter le bloc.
if isinstance(index, HybridSearch) and index.error:
    # Cette ligne signale l’erreur `SystemExit("Embeddings indisponibles pendant l'évaluation ; résultats invalides.")` et interrompt le traitement courant.
    raise SystemExit("Embeddings indisponibles pendant l'évaluation ; résultats invalides.")
# Cette ligne écrit une information de suivi : `print(f"Mode : {args.mode}")`.
print(f"Mode : {args.mode}")
# Cette ligne affecte la variable `n` avec `len(rows)`.
n = len(rows)
# Cette ligne parcourt `k in (1, 3, 6)` pour traiter chaque élément.
for k in (1, 3, 6):
    # Cette ligne écrit une information de suivi : `print(f"Hit@{k} : {sum(1 for _, r in rows if r and r <= k)}/{n}")`.
    print(f"Hit@{k} : {sum(1 for _, r in rows if r and r <= k)}/{n}")
# Cette ligne écrit une information de suivi : `print(f"MRR   : {sum(1/r for _, r in rows if r)/n:.2f}")`.
print(f"MRR   : {sum(1/r for _, r in rows if r)/n:.2f}")
# Cette ligne parcourt `typ in ("direct", "indirecte")` pour traiter chaque élément.
for typ in ("direct", "indirecte"):
    # Cette ligne affecte la variable `sub` avec `[(it, r) for it, r in rows if it["type"] == typ]`.
    sub = [(it, r) for it, r in rows if it["type"] == typ]
    # Cette ligne écrit une information de suivi : `print(f"  questions {typ}s : Hit@3 = {sum(1 for _, r in sub if r and r <= 3)}/{len(sub)}")`.
    print(f"  questions {typ}s : Hit@3 = {sum(1 for _, r in sub if r and r <= 3)}/{len(sub)}")
# Cette ligne écrit une information de suivi : `print("\nÉchecs (bonne section hors du top 6) :")`.
print("\nÉchecs (bonne section hors du top 6) :")
# Cette ligne parcourt `it, r in rows` pour traiter chaque élément.
for it, r in rows:
    # Cette ligne vérifie la condition `r is None` avant d’exécuter le bloc.
    if r is None:
        # Cette ligne écrit une information de suivi : `print(" -", it["question"])`.
        print(" -", it["question"])
# Cette ligne écrit une information de suivi : `print("\nÀ vérifier à la main (réponse non documentée, le bot doit dire qu'il ne sait pas / escalader) :")`.
print("\nÀ vérifier à la main (réponse non documentée, le bot doit dire qu'il ne sait pas / escalader) :")
# Cette ligne parcourt `q in data["no_answer"]` pour traiter chaque élément.
for q in data["no_answer"]:
    # Cette ligne écrit une information de suivi : `print(" -", q)`.
    print(" -", q)
