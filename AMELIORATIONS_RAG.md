# Améliorations du chatbot : recherche hybride et reranker

Date : 8 novembre 2026.

Ce document décrit le fonctionnement du projet, les améliorations vérifiées au cours de la session et leurs limites. La recherche hybride était déjà intégrée au début de cette session. L'ajout réalisé pendant la session est le reranker Gemini, accompagné de tests, d'un mode d'évaluation et de documentation. Le streaming SSE a été expliqué, mais n'a pas été implémenté.

## 1. Objectif

Le chatbot aide les nouveaux employés à comprendre les activités d'une usine de faisceaux de câbles. Ses réponses doivent s'appuyer sur les fiches internes : zones de production, contrôle qualité, sécurité et parcours d'intégration.

L'amélioration vise à sélectionner des extraits plus pertinents avant la rédaction de la réponse, notamment lorsque la question utilise des synonymes ou lorsque plusieurs fiches abordent des sujets proches.

## 2. Parcours d'une question dans l'application

```text
Question de l'utilisateur
        |
        v
Interface de chat -> POST /chat
        |
        v
Traduction/reformulation si nécessaire
        |
        v
Recherche BM25 + recherche par embeddings
        |
        v
Fusion des classements par RRF
        |
        v
Jusqu'à 20 extraits candidats avec les réglages par défaut
        |
        v
Reclassement par Gemini (reranker)
        |
        v
Sélection des 6 premiers extraits disponibles
        |
        v
Envoi des extraits, de la question et de l'historique au modèle de réponse
        |
        v
Réponse affichée avec les sources si l'option est activée
```

Le traitement réel des questions se trouve dans [app.py](./app.py). Le moteur de recherche et le reranker sont définis dans [rag.py](./rag.py). L'interface appelle cette chaîne depuis [static/app.js](./static/app.js).

## 3. Recherche hybride déjà en place

### 3.1 Base documentaire

Les documents Markdown du dossier [fiches](./fiches/) sont découpés par sections. Chaque extrait conserve le nom de la fiche, le titre de la section, le texte et le fichier source.

Les lignes marquées « À COMPLÉTER » sont nettoyées et les sections sans contenu utile sont ignorées. L'état fourni par l'utilisateur pendant la session indiquait **89 extraits chargés**. Ce nombre évoluera si les fiches changent.

### 3.2 Recherche par mots-clés : BM25

BM25 classe les extraits selon les mots présents dans la question. Le code normalise notamment les majuscules, les accents et certains pluriels, puis ignore des mots courants. Le nom de la fiche est renforcé dans le texte indexé.

Cette méthode est utile pour les termes précis, comme « zone P1 », « coupe » ou « composants ». Elle peut également réussir une reformulation si celle-ci conserve suffisamment de mots présents dans les documents.

### 3.3 Recherche sémantique : embeddings

Le modèle Ollama `embeddinggemma` transforme les extraits et la question en vecteurs numériques. La similarité cosinus permet de rechercher des passages proches par le sens.

Les vecteurs des documents sont calculés par lots et conservés en mémoire. Ils ne sont pas stockés dans une base vectorielle persistante. Un redémarrage est nécessaire après modification des fiches ou du modèle d'embeddings.

Le seuil `RAG_MIN_SIMILARITY`, fixé par défaut à `0.3`, filtre les candidats sémantiques. Il ne constitue pas un score de confiance de la réponse finale.

### 3.4 Fusion RRF

La fusion Reciprocal Rank Fusion combine les classements BM25 et sémantique. Chaque présence dans une liste apporte une contribution de `1 / (60 + rang)`. Un extrait bien placé dans les deux recherches est ainsi favorisé.

Les scores RRF expriment un classement relatif : ce ne sont pas des probabilités de vérité.

## 4. Amélioration ajoutée : reranker Gemini

### 4.1 Principe

Le reranker reçoit la question et les extraits candidats après la fusion. Il lit leur contenu et renvoie leurs identifiants dans l'ordre de pertinence. Le modèle de réponse reçoit ensuite les six premiers extraits disponibles.

Il s'agit ici d'un **reclassement par un modèle génératif Gemini**, et non d'un modèle cross-encoder installé localement. Cette solution réutilise la clé Gemini déjà présente, sans nouvelle dépendance Python.

Avec les paramètres par défaut, 20 candidats au maximum sont soumis au reranker pour une recherche du chat. Ce nombre correspond aux extraits conservés après fusion ; les recherches internes peuvent examiner davantage de candidats.

### 4.2 Exemple

Question : « Où prépare-t-on les fils à la bonne longueur avant de les assembler ? »

Des passages sur la coupe, la préparation et l'assemblage peuvent tous contenir des mots pertinents. Le reranker cherche à placer en premier le passage qui répond directement à la question, ici le rôle de la zone de coupe P1.

Un appel réel du reranker sur des candidats BM25 pendant la session a placé en premier la section « À quoi sert cette zone » de P1. Cela valide ce cas précis ; cela ne démontre pas une amélioration générale sur toutes les questions.

### 4.3 Validation de la sortie

Le classement retourné doit être une liste d'identifiants entiers contenant tous les candidats exactement une fois. Les doublons, identifiants inconnus, listes incomplètes et réponses interrompues sont rejetés.

Le reranker ne peut donc pas introduire un nouveau document dans la liste. Les consignes lui demandent aussi de considérer la question et les documents comme des données, et non comme des instructions à exécuter. Cela n'est pas une garantie absolue contre les instructions malveillantes contenues dans des textes.

Les scores d'origine sont conservés avec les extraits ; seul leur ordre change. Après reclassement, il ne faut pas interpréter ces scores comme des notes produites par Gemini.

### 4.4 Disponibilité et modèles de secours

Pendant la vérification réelle, l'API a refusé `gemini-2.5-flash` avec une erreur HTTP 404 pour la clé utilisée. Le reranker a ensuite réussi avec `gemini-flash-lite-latest`.

Le code essaie les modèles de `GEMINI_FALLBACKS` en cas de 404, dans le délai restant. Le modèle ayant répondu est conservé pour les appels suivants dans le processus et apparaît dans l'état du reranker. Ce constat concerne cette exécution et ne garantit pas la disponibilité future des modèles.

## 5. Gestion des erreurs

| Situation | Comportement |
|---|---|
| Embeddings indisponibles | Recherche BM25 conservée ; le reranker peut encore reclasser ses candidats. |
| Reranker indisponible, délai dépassé ou sortie invalide | Classement initial conservé pour permettre la réponse. |
| Modèle du reranker introuvable, erreur 404 | Essai des modèles de secours configurés. |
| Échec du reranker | Délai de 60 secondes avant un nouvel essai lors d'une recherche. |
| Aucun candidat ou un seul candidat | Aucun appel de reclassement nécessaire. |
| Reranker désactivé | Utilisation directe du classement de recherche. |

Les mécanismes de repli favorisent la continuité du service. Une réponse du chatbot ne suffit donc pas à prouver que toutes les étapes ont réussi : il faut aussi consulter `/health`.

## 6. Configuration

Les paramètres peuvent être définis dans le fichier [.env](./.env), sans partager sa clé API.

```dotenv
RAG_MODE=hybrid
EMBEDDING_MODEL=embeddinggemma
OLLAMA_URL=http://localhost:11434
EMBEDDING_TIMEOUT=30
RAG_MIN_SIMILARITY=0.3

RERANK_MODE=gemini
RERANK_MODEL=gemini-flash-lite-latest
RERANK_CANDIDATES=20
RERANK_TIMEOUT=20
```

Cet exemple utilise le modèle de reranking qui a effectivement répondu pendant la session. Il ne signifie pas que ces lignes ont été ajoutées automatiquement à la configuration locale.

| Paramètre | Signification |
|---|---|
| `RAG_MODE` | `hybrid` pour combiner les recherches ; `bm25` pour la recherche lexicale seule. |
| `EMBEDDING_MODEL` | Modèle Ollama utilisé pour les vecteurs. |
| `RAG_MIN_SIMILARITY` | Seuil de sélection des candidats sémantiques. |
| `RERANK_MODE` | `gemini` pour activer le reclassement ; `none` pour le désactiver. |
| `RERANK_MODEL` | Modèle de reclassement ; à défaut, `GEMINI_MODEL`, puis `gemini-2.5-flash`. |
| `RERANK_CANDIDATES` | Nombre de candidats visé avant sélection finale, 20 par défaut. |
| `RERANK_TIMEOUT` | Délai réseau configuré pour le reclassement, 20 secondes par défaut. |
| `GEMINI_FALLBACKS` | Liste de modèles de secours séparés par des virgules. |

En mode hybride, si `RERANK_MODE` n'est pas défini, le reranker s'active lorsque `GEMINI_API_KEY` est présente. Le mode `RAG_MODE=bm25` crée un index BM25 seul, sans reranker.

Redémarrer le serveur après modification de la configuration :

```powershell
python -m uvicorn app:app --reload
```

## 7. Lecture de l'état de santé

Ouvrir http://localhost:8000/health après une question. Voici l'état de recherche communiqué par l'utilisateur après l'ajout :

```json
{
  "mode": "hybrid",
  "embedding_model": "embeddinggemma",
  "ready": true,
  "error": null,
  "reranker": {
    "enabled": true,
    "model": "gemini-flash-lite-latest",
    "ready": true,
    "error": null
  }
}
```

- `retrieval.ready: true` indique que les vecteurs sont disponibles et qu'aucune erreur d'embeddings n'est actuellement signalée.
- `reranker.enabled: true` indique que le reclassement est configuré.
- `reranker.ready: true` indique qu'un reclassement a réussi et qu'aucun échec ultérieur n'a remplacé cet état.
- Avant le premier reclassement, `reranker.ready` est `false` et `error` est `null` : ce n'est pas nécessairement une panne.
- Cet état est global au processus et ne constitue pas une trace détaillée de chaque réponse, notamment si plusieurs utilisateurs interrogent le serveur.
- Pour Gemini, le champ général `llm: true` vérifie la présence d'une clé, pas la réussite d'un appel. Le champ général `model` indique le modèle configuré ; il ne prouve pas quel modèle de secours a généré une réponse.

## 8. Vérifications effectuées pendant la session

### Tests automatisés

La commande suivante a terminé avec **12 tests réussis** :

```powershell
python -m unittest discover -s tests -p "test_*.py"
```

Les tests couvrent notamment la recherche sémantique simulée, la fusion, le repli BM25, les vecteurs invalides, la promotion d'un candidat hors du classement final initial, les classements invalides, le délai après échec, la reprise, l'activation du reranker et le secours après une erreur 404.

Une vérification isolée de `_chat`, avec appels externes simulés, a également confirmé que les six extraits reclassés sont transmis au modèle de réponse. La compilation Python des modules concernés a réussi.

### Vérifications réelles et manuelles

- Les embeddings ont été disponibles lors d'une recherche réelle.
- Un appel réel du reranker a réussi avec le modèle de secours et a placé P1 en premier pour la question sur la longueur des fils.
- L'utilisateur a confirmé ensuite un état `/health` avec recherche hybride et reranker prêts, sans erreur.
- Avant l'ajout du reranker, les réponses partagées par l'utilisateur identifiaient déjà P1 pour une question directe et sa reformulation, y compris dans une nouvelle conversation.

Ces résultats confirment l'intégration et le fonctionnement technique observé. Aucun gain chiffré global de pertinence ou de temps de réponse n'a été établi pendant cette session.

## 9. Questions pour tester les réponses

Activer « Afficher sources » et démarrer une nouvelle conversation pour chaque question afin de limiter l'influence de l'historique.

| Question | Vérification attendue |
|---|---|
| À quoi sert la zone de coupe P1 ? | Rôle de P1 et fiche correspondante dans les sources. |
| Où prépare-t-on les fils à la bonne longueur avant de les assembler ? | Identification de P1 malgré la reformulation. |
| Quelle est la différence entre la coupe des fils et leur assemblage ? | Distinction entre les opérations, fondée sur les fiches concernées. |
| Comment vérifie-t-on la qualité des fils après la coupe ? | Utilisation des passages de contrôle qualité de P1 plutôt que de procédures sans rapport. |
| Quelle longueur exacte dois-je régler pour une référence appelée TEST-XYZ-999 ? | Reconnaissance de l'information manquante si cette référence n'est pas documentée ; aucune valeur inventée. |

Comparer chaque affirmation précise aux sections des fiches. Les sources affichées représentent les extraits récupérés ; elles ne prouvent pas que chaque phrase de la réponse leur est fidèle.

## 10. Mesurer l'apport du reranker

Le script [eval.py](./eval.py) permet de comparer trois configurations sur les questions de [tests/questions.json](./tests/questions.json) :

```powershell
python eval.py --mode bm25
python eval.py --mode hybrid
python eval.py --mode hybrid-rerank
```

| Indicateur | Lecture |
|---|---|
| Hit@1 | La section attendue apparaît en première position. |
| Hit@3 | Elle apparaît parmi les trois premières. |
| Hit@6 | Elle apparaît parmi les six premières. |
| MRR | Mesure favorisant les classements où la section attendue arrive tôt ; plus élevée signifie mieux classée sur ce jeu. |

Le mode `hybrid-rerank` effectue de vrais appels Gemini. Il s'arrête si le reranker échoue pour ne pas présenter un repli comme une évaluation réussie du reclassement.

Cette évaluation porte sur la recherche des sections attendues, pas sur les réponses finales. Il reste à comparer les réponses aux sources et à mesurer la latence. Les questions sans réponse documentaire sont indiquées pour vérification manuelle.

## 11. Coûts, limites et prochaines améliorations

- Le reranker ajoute normalement un appel Gemini par recherche comportant au moins deux candidats ; un modèle de secours peut entraîner une tentative supplémentaire.
- Cet appel consomme du quota et peut avoir un coût selon le compte. Il augmente aussi le délai avant la génération de la réponse.
- Jusqu'à 20 extraits sont envoyés à Gemini pour le reclassement avec les réglages par défaut, contre 6 retenus pour la rédaction.
- Un bon reclassement ne garantit pas une réponse sans erreur. Le respect des sources est demandé au modèle, mais n'est pas contrôlé automatiquement phrase par phrase.
- Le reranker ne peut récupérer un passage absent des candidats et ne peut compléter une information manquante dans les fiches.
- Le code conserve un état de santé global, sans détail BM25/sémantique/reranker associé à chaque réponse.

Pistes à évaluer ensuite : enrichir le jeu de questions métier, mesurer la qualité et la latence avant/après, ajuster le nombre de candidats, ajouter une trace de recherche par réponse et envisager un reranker local si les contraintes le justifient.

Le **streaming SSE reste à implémenter**. Il permettrait d'afficher progressivement le texte pendant la génération, mais ne supprimerait pas le temps de recherche et de reclassement préalable.

## 12. Fichiers concernés

| Fichier | Rôle |
|---|---|
| [rag.py](./rag.py) | Recherche hybride, reranker, validation du classement, modèles de secours et repli. |
| [app.py](./app.py) | Intégration existante via `create_index`, traitement des questions et état `/health`. |
| [tests/test_rag.py](./tests/test_rag.py) | Tests automatisés du moteur et du reranker. |
| [eval.py](./eval.py) | Comparaison BM25, hybride et hybride avec reranker. |
| [README.md](./README.md) | Instructions d'installation, configuration et utilisation. |
| [static/app.js](./static/app.js) | Envoi des questions et affichage optionnel des sources dans l'interface existante. |

Les changements d'implémentation du reranker ont porté sur le moteur, les tests, l'évaluation et la documentation. L'application et l'interface utilisent les points d'intégration déjà présents.
