"""Tests unitaires du moteur de recherche hybride et du reclassement."""

# Cette ligne importe les dépendances nécessaires : import unittest.
import unittest
# Cette ligne importe les dépendances nécessaires : import io.
import io
# Cette ligne importe les dépendances nécessaires : import json.
import json
# Cette ligne importe les dépendances nécessaires : import urllib.error.
import urllib.error
# Cette ligne importe les dépendances nécessaires : from unittest.mock import patch.
from unittest.mock import patch

# Cette ligne importe les dépendances nécessaires : from rag import BM25, Chunk, GeminiReranker, HybridSearch, create_index, unit_vectors.
from rag import BM25, Chunk, GeminiReranker, HybridSearch, create_index, unit_vectors


# Cette ligne définit la classe FakeEmbeddings, qui regroupe les données et opérations liées à fakeembeddings.
class FakeEmbeddings:
    # Cette ligne affecte le modèle d’intelligence artificielle sélectionné avec `"test"`.
    model = "test"

    # Cette ligne définit embed(self, texts), fonction qui regroupe le traitement décrit par son nom.
    def embed(self, texts):
        # Cette ligne renvoie `[[1.0, 0.0] if "sécurité" in text or "danger" in text else [0.0, 1.0]` au code qui a appelé la fonction.
        return [[1.0, 0.0] if "sécurité" in text or "danger" in text else [0.0, 1.0]
                # Cette ligne parcourt `text in texts]` pour traiter chaque élément.
                for text in texts]


# Cette ligne définit la classe HybridTests, qui regroupe les données et opérations liées à hybridtests.
class HybridTests(unittest.TestCase):
    # Cette ligne définit setUp(self), fonction qui regroupe le traitement décrit par son nom.
    def setUp(self):
        # Cette ligne affecte les passages extraits des fiches avec `[Chunk("1", "sécurité", "Urgence", "Appeler les secours", "a.md"),`.
        self.chunks = [Chunk("1", "sécurité", "Urgence", "Appeler les secours", "a.md"),
                       # Cette ligne exécute `Chunk("2", "Stock", "Pièces", "Ranger les composants", "b.md")]` dans le traitement courant.
                       Chunk("2", "Stock", "Pièces", "Ranger les composants", "b.md")]

    # Cette ligne définit test_semantic_match_without_shared_words(self), fonction qui regroupe le traitement décrit par son nom.
    def test_semantic_match_without_shared_words(self):
        # Cette ligne appelle la méthode `self.assertEqual` pour effectuer cette étape du traitement.
        self.assertEqual(BM25(self.chunks).search("danger"), [])
        # Cette ligne affecte le moteur de recherche documentaire avec `HybridSearch(self.chunks, FakeEmbeddings())`.
        index = HybridSearch(self.chunks, FakeEmbeddings())
        # Cette ligne appelle la méthode `self.assertEqual` pour effectuer cette étape du traitement.
        self.assertEqual(index.search("danger")[0][1].doc_id, "1")
        # Cette ligne appelle la méthode `self.assertTrue` pour effectuer cette étape du traitement.
        self.assertTrue(index.status()["ready"])

    # Cette ligne définit test_fusion_is_unique_and_rewards_agreement(self), fonction qui regroupe le traitement décrit par son nom.
    def test_fusion_is_unique_and_rewards_agreement(self):
        # Cette ligne affecte les passages trouvés par la recherche avec `HybridSearch(self.chunks, FakeEmbeddings()).search("sécurité")`.
        hits = HybridSearch(self.chunks, FakeEmbeddings()).search("sécurité")
        # Cette ligne appelle la méthode `self.assertEqual` pour effectuer cette étape du traitement.
        self.assertEqual(len(hits), 1)
        # Cette ligne appelle la méthode `self.assertAlmostEqual` pour effectuer cette étape du traitement.
        self.assertAlmostEqual(hits[0][0], 2 / 61)

    # Cette ligne définit test_outage_falls_back_and_retries_after_cooldown(self), fonction qui regroupe le traitement décrit par son nom.
    def test_outage_falls_back_and_retries_after_cooldown(self):
        # Cette ligne affecte la variable `embedder` avec `FakeEmbeddings()`.
        embedder = FakeEmbeddings()
        # Cette ligne affecte le moteur de recherche documentaire avec `HybridSearch(self.chunks, embedder)`.
        index = HybridSearch(self.chunks, embedder)
        # Cette ligne ouvre la ressource `patch.object(embedder, "embed", side_effect=OSError("offline")) as call` et garantit sa fermeture à la fin du bloc.
        with patch.object(embedder, "embed", side_effect=OSError("offline")) as call:
            # Cette ligne appelle la méthode `self.assertEqual` pour effectuer cette étape du traitement.
            self.assertEqual(index.search("composants"), BM25(self.chunks).search("composants"))
            # Cette ligne exécute `index.search("composants")` dans le traitement courant.
            index.search("composants")
            # Cette ligne appelle la méthode `self.assertEqual` pour effectuer cette étape du traitement.
            self.assertEqual(call.call_count, 1)
        # Cette ligne affecte la variable `index.retry_at` avec `0`.
        index.retry_at = 0
        # Cette ligne appelle la méthode `self.assertEqual` pour effectuer cette étape du traitement.
        self.assertEqual(index.search("danger")[0][1].doc_id, "1")
        # Cette ligne appelle la méthode `self.assertIsNone` pour effectuer cette étape du traitement.
        self.assertIsNone(index.error)

    # Cette ligne définit test_query_failure_and_dimension_mismatch(self), fonction qui regroupe le traitement décrit par son nom.
    def test_query_failure_and_dimension_mismatch(self):
        # Cette ligne affecte la variable `embedder` avec `FakeEmbeddings()`.
        embedder = FakeEmbeddings()
        # Cette ligne affecte le moteur de recherche documentaire avec `HybridSearch(self.chunks, embedder)`.
        index = HybridSearch(self.chunks, embedder)
        # Cette ligne exécute `index.prepare()` dans le traitement courant.
        index.prepare()
        # Cette ligne ouvre la ressource `patch.object(embedder, "embed", return_value=[[1, 0, 0]])` et garantit sa fermeture à la fin du bloc.
        with patch.object(embedder, "embed", return_value=[[1, 0, 0]]):
            # Cette ligne appelle la méthode `self.assertEqual` pour effectuer cette étape du traitement.
            self.assertEqual(index.search("composants"), BM25(self.chunks).search("composants"))
            # Cette ligne appelle la méthode `self.assertFalse` pour effectuer cette étape du traitement.
            self.assertFalse(index.status()["ready"])

    # Cette ligne définit test_empty_and_limits(self), fonction qui regroupe le traitement décrit par son nom.
    def test_empty_and_limits(self):
        # Cette ligne affecte le moteur de recherche documentaire avec `HybridSearch(self.chunks, FakeEmbeddings())`.
        index = HybridSearch(self.chunks, FakeEmbeddings())
        # Cette ligne appelle la méthode `self.assertEqual` pour effectuer cette étape du traitement.
        self.assertEqual(index.search("  "), [])
        # Cette ligne appelle la méthode `self.assertEqual` pour effectuer cette étape du traitement.
        self.assertEqual(index.search("danger", 0), [])
        # Cette ligne appelle la méthode `self.assertEqual` pour effectuer cette étape du traitement.
        self.assertEqual(HybridSearch([], FakeEmbeddings()).search("danger"), [])
        # Cette ligne appelle la méthode `self.assertEqual` pour effectuer cette étape du traitement.
        self.assertEqual(len(index.search("danger composants", 1)), 1)

    # Cette ligne définit test_rejects_invalid_vectors(self), fonction qui regroupe le traitement décrit par son nom.
    def test_rejects_invalid_vectors(self):
        # Cette ligne parcourt `values in ([[0, 0]], [[float("nan"), 1]], [[1], [1, 2]], [])` pour traiter chaque élément.
        for values in ([[0, 0]], [[float("nan"), 1]], [[1], [1, 2]], []):
            # Cette ligne ouvre la ressource `self.assertRaises(ValueError)` et garantit sa fermeture à la fin du bloc.
            with self.assertRaises(ValueError):
                # Cette ligne exécute `unit_vectors(values, 1)` dans le traitement courant.
                unit_vectors(values, 1)


# Cette ligne définit la classe RerankerTests, qui regroupe les données et opérations liées à rerankertests.
class RerankerTests(unittest.TestCase):
    # Cette ligne définit setUp(self), fonction qui regroupe le traitement décrit par son nom.
    def setUp(self):
        # Cette ligne affecte les passages trouvés par la recherche avec `[(1 / (61 + i), Chunk(str(i), "Stock", "Pièces",`.
        self.hits = [(1 / (61 + i), Chunk(str(i), "Stock", "Pièces",
                     # Cette ligne exécute `"Ranger les composants", f"{i}.md")) for i in range(8)]` dans le traitement courant.
                     "Ranger les composants", f"{i}.md")) for i in range(8)]
        # Cette ligne affecte la variable `self.reranker` avec `GeminiReranker()`.
        self.reranker = GeminiReranker()

    # Cette ligne définit test_promotes_candidate_outside_final_top_k(self), fonction qui regroupe le traitement décrit par son nom.
    def test_promotes_candidate_outside_final_top_k(self):
        # Cette ligne affecte le moteur de recherche documentaire avec `HybridSearch([c for _, c in self.hits], FakeEmbeddings(),`.
        index = HybridSearch([c for _, c in self.hits], FakeEmbeddings(),
                             # Cette ligne affecte la variable `reranker` avec `self.reranker)`.
                             reranker=self.reranker)
        # Cette ligne ouvre la ressource `patch.object(self.reranker, "_rank", return_value=list(reversed(range(8)))) as rank` et garantit sa fermeture à la fin du bloc.
        with patch.object(self.reranker, "_rank", return_value=list(reversed(range(8)))) as rank:
            # Cette ligne affecte les passages trouvés par la recherche avec `index.search("composants", k=2)`.
            hits = index.search("composants", k=2)
        # Cette ligne appelle la méthode `self.assertEqual` pour effectuer cette étape du traitement.
        self.assertEqual(len(rank.call_args.args[1]), 8)
        # Cette ligne appelle la méthode `self.assertEqual` pour effectuer cette étape du traitement.
        self.assertEqual([c.doc_id for _, c in hits], ["7", "6"])
        # Cette ligne appelle la méthode `self.assertTrue` pour effectuer cette étape du traitement.
        self.assertTrue(index.status()["reranker"]["ready"])

    # Cette ligne définit test_invalid_rankings_preserve_original_results(self), fonction qui regroupe le traitement décrit par son nom.
    def test_invalid_rankings_preserve_original_results(self):
        # Cette ligne parcourt `order in ([0, 0], [99], [True, 0], "0", list(range(7)), [0] * 8)` pour traiter chaque élément.
        for order in ([0, 0], [99], [True, 0], "0", list(range(7)), [0] * 8):
            # Cette ligne affecte la variable `reranker` avec `GeminiReranker()`.
            reranker = GeminiReranker()
            # Cette ligne ouvre la ressource `patch.object(reranker, "_rank", return_value=order)` et garantit sa fermeture à la fin du bloc.
            with patch.object(reranker, "_rank", return_value=order):
                # Cette ligne appelle la méthode `self.assertEqual` pour effectuer cette étape du traitement.
                self.assertEqual(reranker.rerank("question", self.hits, 2), self.hits[:2])
            # Cette ligne appelle la méthode `self.assertIsNotNone` pour effectuer cette étape du traitement.
            self.assertIsNotNone(reranker.error)

    # Cette ligne définit test_failure_cooldown_and_recovery(self), fonction qui regroupe le traitement décrit par son nom.
    def test_failure_cooldown_and_recovery(self):
        # Cette ligne ouvre la ressource `patch.object(self.reranker, "_rank", side_effect=TimeoutError) as rank` et garantit sa fermeture à la fin du bloc.
        with patch.object(self.reranker, "_rank", side_effect=TimeoutError) as rank:
            # Cette ligne parcourt `_ in range(2)` pour traiter chaque élément.
            for _ in range(2):
                # Cette ligne appelle la méthode `self.assertEqual` pour effectuer cette étape du traitement.
                self.assertEqual(self.reranker.rerank("q", self.hits, 2), self.hits[:2])
            # Cette ligne appelle la méthode `self.assertEqual` pour effectuer cette étape du traitement.
            self.assertEqual(rank.call_count, 1)
        # Cette ligne affecte la variable `self.reranker.retry_at` avec `0`.
        self.reranker.retry_at = 0
        # Cette ligne ouvre la ressource `patch.object(self.reranker, "_rank", return_value=list(range(8)))` et garantit sa fermeture à la fin du bloc.
        with patch.object(self.reranker, "_rank", return_value=list(range(8))):
            # Cette ligne appelle la méthode `self.reranker.rerank` pour effectuer cette étape du traitement.
            self.reranker.rerank("q", self.hits, 2)
        # Cette ligne appelle la méthode `self.assertTrue` pour effectuer cette étape du traitement.
        self.assertTrue(self.reranker.ready)
        # Cette ligne appelle la méthode `self.assertIsNone` pour effectuer cette étape du traitement.
        self.assertIsNone(self.reranker.error)

    # Cette ligne définit test_no_request_for_empty_single_or_zero_limit(self), fonction qui regroupe le traitement décrit par son nom.
    def test_no_request_for_empty_single_or_zero_limit(self):
        # Cette ligne ouvre la ressource `patch.object(self.reranker, "_rank") as rank` et garantit sa fermeture à la fin du bloc.
        with patch.object(self.reranker, "_rank") as rank:
            # Cette ligne appelle la méthode `self.assertEqual` pour effectuer cette étape du traitement.
            self.assertEqual(self.reranker.rerank("q", [], 6), [])
            # Cette ligne appelle la méthode `self.assertEqual` pour effectuer cette étape du traitement.
            self.assertEqual(self.reranker.rerank("q", self.hits[:1], 6), self.hits[:1])
            # Cette ligne appelle la méthode `self.assertEqual` pour effectuer cette étape du traitement.
            self.assertEqual(self.reranker.rerank("q", self.hits, 0), [])
            # Cette ligne exécute `rank.assert_not_called()` dans le traitement courant.
            rank.assert_not_called()

    # Cette ligne définit test_app_factory_enables_and_disables_reranker(self), fonction qui regroupe le traitement décrit par son nom.
    def test_app_factory_enables_and_disables_reranker(self):
        # Cette ligne ouvre la ressource `patch.dict("os.environ", {"RAG_MODE": "hybrid", "RERANK_MODE": "gemini"})` et garantit sa fermeture à la fin du bloc.
        with patch.dict("os.environ", {"RAG_MODE": "hybrid", "RERANK_MODE": "gemini"}):
            # Cette ligne appelle la méthode `self.assertIsInstance` pour effectuer cette étape du traitement.
            self.assertIsInstance(create_index([]).reranker, GeminiReranker)
        # Cette ligne ouvre la ressource `patch.dict("os.environ", {"RAG_MODE": "hybrid", "RERANK_MODE": "none"})` et garantit sa fermeture à la fin du bloc.
        with patch.dict("os.environ", {"RAG_MODE": "hybrid", "RERANK_MODE": "none"}):
            # Cette ligne appelle la méthode `self.assertIsNone` pour effectuer cette étape du traitement.
            self.assertIsNone(create_index([]).reranker)

    # Cette ligne définit test_unavailable_model_uses_fallback(self), fonction qui regroupe le traitement décrit par son nom.
    def test_unavailable_model_uses_fallback(self):
        # Cette ligne affecte la réponse reçue du service avec `{"candidates": [{"finishReason": "STOP", "content": {`.
        response = {"candidates": [{"finishReason": "STOP", "content": {
            # Cette ligne exécute `"parts": [{"text": "[1, 0]"}]}}]}` dans le traitement courant.
            "parts": [{"text": "[1, 0]"}]}}]}
        # Cette ligne ouvre la ressource `patch.dict("os.environ", {"GEMINI_API_KEY": "test", "GEMINI_FALLBACKS": "backup"}), patch(` et garantit sa fermeture à la fin du bloc.
        with patch.dict("os.environ", {"GEMINI_API_KEY": "test", "GEMINI_FALLBACKS": "backup"}), patch(
                # Cette ligne exécute `"rag.urllib.request.urlopen", side_effect=[` dans le traitement courant.
                "rag.urllib.request.urlopen", side_effect=[
                    # Cette ligne exécute `urllib.error.HTTPError("https://example.test", 404, "missing", {}, None),` dans le traitement courant.
                    urllib.error.HTTPError("https://example.test", 404, "missing", {}, None),
                    # Cette ligne démarre le bloc `io.BytesIO(json.dumps(response).encode())]) as call`.
                    io.BytesIO(json.dumps(response).encode())]) as call:
            # Cette ligne affecte le résultat du traitement avec `self.reranker.rerank("q", self.hits[:2], 1)`.
            result = self.reranker.rerank("q", self.hits[:2], 1)
        # Cette ligne appelle la méthode `self.assertEqual` pour effectuer cette étape du traitement.
        self.assertEqual(result, self.hits[1:2])
        # Cette ligne appelle la méthode `self.assertEqual` pour effectuer cette étape du traitement.
        self.assertEqual(self.reranker.status()["model"], "backup")
        # Cette ligne appelle la méthode `self.assertEqual` pour effectuer cette étape du traitement.
        self.assertEqual(call.call_count, 2)


# Cette ligne vérifie la condition `__name__ == "__main__"` avant d’exécuter le bloc.
if __name__ == "__main__":
    # Cette ligne exécute `unittest.main()` dans le traitement courant.
    unittest.main()
# Cette ligne exécute `"""Vérifie le classement hybride, ses replis et le comportement du reranker."""` dans le traitement courant.
"""Vérifie le classement hybride, ses replis et le comportement du reranker."""

