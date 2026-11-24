# Chatbot d'intégration (version simple)

## Option gratuite cloud : Google Gemini (recommandée)
1. Créer une clé gratuite sur https://aistudio.google.com (Get API key).
2. Dans PowerShell :
```powershell
$env:GEMINI_API_KEY="votre-cle"
python -m uvicorn app:app --reload
```
`/health` doit afficher `"provider": "gemini"` et `"llm": true`. Changer de modèle : `$env:GEMINI_MODEL="..."`.
Attention : le niveau gratuit peut réutiliser les données envoyées et exclut l'usage commercial : prototype seulement,
sans données personnelles d'employés.

## Option locale : Ollama (voir ci-dessous)

## Lancer avec Ollama (Windows PowerShell)
1. Installer Ollama (https://ollama.com), puis :
```powershell
ollama pull qwen2.5:3b
```
2. Lancer le chatbot :
```powershell
pip install -r requirements.txt
python -m uvicorn app:app --reload
```
3. Ouvrir http://localhost:8000 (et http://localhost:8000/health : `"llm": true` = modèle prêt).

Options (variables d'environnement) : `OLLAMA_MODEL` (ex. `qwen2.5:7b`), `LLM_PROVIDER=anthropic` + `ANTHROPIC_API_KEY`.

## Recherche hybride : BM25 + embeddings

La recherche combine les mots-clés BM25 et la similarité cosinus des embeddings
locaux Ollama. Les classements sont fusionnés avec Reciprocal Rank Fusion (RRF).
Le modèle de réponse (Gemini, Ollama ou Claude) reste indépendant des embeddings.
Aucune dépendance Python supplémentaire n'est nécessaire.

1. Installer et démarrer Ollama, puis télécharger le modèle d'embeddings :
   ```powershell
   ollama pull embeddinggemma
   ```
   Si Ollama n'est pas déjà lancé, exécuter `ollama serve` dans un autre terminal.
2. Ajouter ces options dans `.env` :
   ```dotenv
   RAG_MODE=hybrid
   EMBEDDING_MODEL=embeddinggemma
   OLLAMA_URL=http://localhost:11434
   EMBEDDING_TIMEOUT=30
   RAG_MIN_SIMILARITY=0.3
   ```
3. Lancer `python -m uvicorn app:app --reload`.
4. Vérifier http://localhost:8000/health : `retrieval.mode` doit être `hybrid`
   et `retrieval.ready` doit être `true`.

Les sections sont encodées par lots au démarrage et conservées en mémoire.
Redémarrer après toute modification des fiches ou du modèle d'embeddings.
Le premier démarrage peut prendre du temps pendant le chargement du modèle.
Les textes trop longs provoquent un repli BM25 plutôt qu'une troncature silencieuse.
Si les embeddings échouent, la recherche reste disponible en BM25 et réessaie
après 60 secondes lors d'une nouvelle recherche. L'état dégradé apparaît dans `/health`.
Pour désactiver les embeddings, utiliser `RAG_MODE=bm25`.

Le seuil cosinus `RAG_MIN_SIMILARITY` est un point de départ à ajuster avec les
questions métier ; il ne garantit pas qu'une réponse est documentée.
Comparer les résultats sur le même jeu de questions :
```powershell
python eval.py --mode bm25
python eval.py --mode hybrid
python -m unittest discover -s tests -p "test_*.py"
```
L'évaluation hybride exige un modèle disponible et s'arrête en cas d'échec.
Référence de l'API utilisée : [Ollama /api/embed](https://docs.ollama.com/api/embed).

## Reranker Gemini

Dans l'application principale, le reranker est activé par défaut en mode hybride
si `GEMINI_API_KEY` est présente. Il reclasse jusqu'à 20 candidats en lisant leur
contenu avec la question, puis transmet les 6 premiers au modèle de réponse.
Il utilise un appel Gemini supplémentaire par recherche (quota, coût éventuel et latence).
Les scores retournés restent les scores RRF d'origine, pas des probabilités.

Options dans `.env` :
```dotenv
RERANK_MODE=gemini
RERANK_MODEL=gemini-2.5-flash
RERANK_CANDIDATES=20
RERANK_TIMEOUT=20
```
`RERANK_MODE=none` désactive cette étape. Redémarrer le serveur après modification.
Si le modèle renvoie une erreur 404, les modèles de `GEMINI_FALLBACKS` sont essayés
dans le délai restant. Le modèle effectivement utilisé apparaît dans `/health`.
Le classement est aussi appliqué aux candidats BM25 si les embeddings sont indisponibles.
Si Gemini échoue ou renvoie un classement invalide, l'ordre initial est conservé ;
un nouvel essai est possible après 60 secondes. Aucun nouvel extrait n'est inventé.

Après une question, vérifier `retrieval.reranker` dans `/health` :
`enabled: true`, `ready: true`, `error: null` indiquent un reclassement réussi.
Avant le premier reclassement, `ready` vaut `false` et `error` vaut `null`.
Cet état correspond au dernier appel, pas à une mesure de qualité.

Comparer les mêmes questions avec et sans reranker :
```powershell
python eval.py --mode hybrid
python eval.py --mode hybrid-rerank
```
Le second mode effectue de vrais appels Gemini et s'arrête si le reranker échoue.
API : [sorties structurées Gemini](https://ai.google.dev/gemini-api/docs/structured-output).

## Ajouter / modifier des fiches
Déposer un fichier `.md` dans `fiches/` (même format que les autres : en-tête `---`, sections `## `)
puis relancer le serveur. Les sections qui ne contiennent que « À COMPLÉTER » sont ignorées.

## Structure
- `rag.py` : lecture des fiches, recherche BM25 et embeddings, fusion RRF
- `app.py` : API FastAPI (`/chat`, `/health`) + appel à Claude
- `static/index.html` : interface de chat
- `fiches/` : base de connaissances

## Prochaines étapes (feuille de route)
1. Mesurer et ajuster la pertinence du reranker
2. Streaming SSE
3. Connexion SIRH/ERP
4. Voix Darija
5. Tableau de bord RH
# Voice Interaction (STT/TTS)

- **Parcours** : parler → comprendre → répondre → écouter.
- **Technologies** : Web Speech API – SpeechRecognition (STT) et SpeechSynthesis (TTS) intégrés au navigateur.
- **Fonctionnalités** :
  - Bouton micro pour lancer la reconnaissance vocale.
  - Sélecteur de langue (fr-FR, en-US, …) persistant.
  - Retour texte affiché dans le champ de saisie.
  - Synthèse vocale de la réponse du bot, bouton replay.
  - Gestion des erreurs (micro non disponible, voix introuvable, API chat en échec) via toasts.
- **Pré‑requis** :
  - Site servi en HTTPS (ou `localhost`).
  - Autorisation d’accès au microphone.
  - Navigateur supportant Web Speech API (Chrome, Edge, Safari ≥ 14).
- **Points d’implémentation** :
  - `static/app.js` : classes `SpeechRecognizer` et `SpeechSynthesizer`.
  - `static/index.html` : ajout des boutons `#btn-mic`, `#btn‑play` et du sélecteur `#lang-select`.
  - `static/style.css` : styles des icônes et des toasts.
- **Débogage** : ouvrir la console et vérifier `speechSynthesis.getVoices()` et `new SpeechRecognition()`.
