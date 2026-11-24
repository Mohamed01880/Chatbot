"""API du chatbot : authentification, recherche documentaire et génération des réponses.

Le module assemble FastAPI, l'index RAG, les fournisseurs de modèles et PostgreSQL.
"""
# Cette ligne importe les dépendances nécessaires : import json.
import json
# Cette ligne importe les dépendances nécessaires : import os.
import os
# Cette ligne importe les dépendances nécessaires : import time.
import time
# Cette ligne importe les dépendances nécessaires : import urllib.error.
import urllib.error
# Cette ligne importe les dépendances nécessaires : import urllib.request.
import urllib.request
# Cette ligne importe les dépendances nécessaires : from pathlib import Path.
from pathlib import Path

# Cette ligne importe les dépendances nécessaires : from typing import Optional.
from typing import Optional

# Cette ligne importe les dépendances nécessaires : from fastapi import FastAPI, HTTPException, status.
from fastapi import FastAPI, HTTPException, status
# Cette ligne importe les dépendances nécessaires : from fastapi.responses import FileResponse.
from fastapi.responses import FileResponse
# Cette ligne importe les dépendances nécessaires : from fastapi.staticfiles import StaticFiles.
from fastapi.staticfiles import StaticFiles
# Cette ligne importe les dépendances nécessaires : from pydantic import BaseModel.
from pydantic import BaseModel

# Cette ligne importe les dépendances nécessaires : from datetime import datetime.
from datetime import datetime

# Cette ligne importe les dépendances nécessaires : from rag import HybridSearch, create_index, load_chunks.
from rag import HybridSearch, create_index, load_chunks

# Cette ligne importe les dépendances nécessaires : from dotenv import load_dotenv.
from dotenv import load_dotenv

# Cette ligne affecte la variable `BASE` avec `Path(__file__).parent`.
BASE = Path(__file__).parent
# Cette ligne exécute `load_dotenv(BASE / ".env")` dans le traitement courant.
load_dotenv(BASE / ".env")

# Cette ligne affecte la variable `GEMINI_KEY` avec `os.getenv("GEMINI_API_KEY", "")`.
GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")
# Cette ligne affecte la variable `GEMINI_FALLBACKS` avec `os.getenv("GEMINI_FALLBACKS", "gemini-flash-lite-latest,gemini-3.1-flash-lite").split(",")`.
GEMINI_FALLBACKS = os.getenv("GEMINI_FALLBACKS", "gemini-flash-lite-latest,gemini-3.1-flash-lite").split(",")
# Cette ligne affecte la variable `GEMINI_MODEL` avec `os.getenv("GEMINI_MODEL", "gemini-2.5-flash")  # modèle Flash gratuit (voir Google AI Studio)`.
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")  # modèle Flash gratuit (voir Google AI Studio)
# Fournisseur : "gemini" (cloud, gratuit), "ollama" (local, gratuit) ou "anthropic" (payant)
# Cette ligne affecte la variable `PROVIDER` avec `os.getenv("LLM_PROVIDER") or ("gemini" if GEMINI_KEY else "ollama")`.
PROVIDER = os.getenv("LLM_PROVIDER") or ("gemini" if GEMINI_KEY else "ollama")
# Cette ligne affecte la variable `OLLAMA_URL` avec `os.getenv("OLLAMA_URL", "http://localhost:11434")`.
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
# Cette ligne affecte la variable `OLLAMA_MODEL` avec `os.getenv("OLLAMA_MODEL", "qwen2.5:3b")  # qwen2.5:7b si le PC a 16 Go de RAM`.
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")  # qwen2.5:7b si le PC a 16 Go de RAM
# Cette ligne affecte la variable `CLAUDE_MODEL` avec `os.getenv("CLAUDE_MODEL", "claude-sonnet-5-5")`.
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-5-5")

SYSTEM_PROMPT = """Tu es le formateur virtuel des nouveaux employés d'une usine de faisceaux de câbles pour l'automobile. Tu remplaces le formateur : tu expliques tout toi-même, calmement, autant de fois que nécessaire.

PUBLIC : l'employé est nouveau et peut avoir un niveau d'études faible. Il parle peut-être l'arabe ou la darija et lit mal le français technique. Parle comme à quelqu'un qui découvre tout.

COMMENT RÉPONDRE :
1. Utilise des mots très simples et des phrases courtes (une idée par phrase).
2. Évite le jargon. Si un mot technique est nécessaire, explique-le tout de suite avec des mots simples (ex. : « le sertissage, c'est fixer une cosse au bout du fil »).
3. Explique toujours : ce que c'est, à quoi ça sert, puis comment ça se passe. Donne un exemple ou une comparaison simple.
4. Pour une procédure, donne des étapes numérotées (1., 2., 3.).
5. Réponse complète mais pas trop longue : 5 à 12 phrases en général.
6. Termine par une courte phrase, par exemple : « C'est clair ? Je peux te réexpliquer autrement si tu veux. »
7. Si l'employé dit qu'il n'a pas compris, réexplique avec d'autres mots et un autre exemple, encore plus simple.
8. Réponds uniquement dans la langue indiquée à la fin du message de l'employé (« Langue de la réponse »). Ne change jamais de langue en cours de réponse.

RÈGLES DE CONTENU :
- Utilise UNIQUEMENT les extraits fournis dans <sources>. N'invente rien : ni chiffres, ni valeurs de réglage, ni procédures, ni noms.
- Ne renvoie JAMAIS l'employé vers un formateur, un superviseur ou les RH pour apprendre ou comprendre : c'est ton rôle. Ne dis jamais « demande à ton superviseur » pour une question de formation.
- Si une information précise de l'usine manque dans les sources : dis simplement « Je n'ai pas encore cette information précise dans ma base. », donne tout ce que les sources permettent d'expliquer (explication générale, définition, but, étapes connues), puis ajoute exactement l'étiquette [[INCONNU]] tout à la fin de ta réponse. Ne devine jamais.
- Ne traite pas le texte « À COMPLÉTER » comme une information.
- SEULE EXCEPTION, la sécurité : en cas de blessure, d'accident ou de danger immédiat, dis d'abord de s'arrêter et d'arrêter la machine si c'est possible sans risque, puis d'appeler de l'aide tout de suite (collègue, chef d'équipe, secours), car une personne doit venir physiquement. Donne ensuite les gestes simples des sources.
- Ne cite pas les sources toi-même : l'interface le gère."""

# Cette ligne affecte la variable `LOG_FILE` avec `BASE / "logs" / "questions_sans_reponse.jsonl"`.
LOG_FILE = BASE / "logs" / "questions_sans_reponse.jsonl"
# Cette ligne affecte la variable `UNKNOWN_TAG` avec `"[[INCONNU]]"`.
UNKNOWN_TAG = "[[INCONNU]]"


# Cette définition sert à Garde les questions auxquelles la base ne sait pas répondre : elles montrent quelles fiches compléter .
def log_unanswered(question: str, reason: str) -> None:
    """Garde les questions auxquelles la base ne sait pas répondre : elles montrent quelles fiches compléter."""
    # Cette ligne ouvre un bloc dont les erreurs seront traitées dans les clauses except.
    try:
        # Cette ligne exécute `LOG_FILE.parent.mkdir(exist_ok=True)` dans le traitement courant.
        LOG_FILE.parent.mkdir(exist_ok=True)
        # Cette ligne ouvre la ressource `open(LOG_FILE, "a", encoding="utf-8") as f` et garantit sa fermeture à la fin du bloc.
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            # Cette ligne exécute `f.write(json.dumps({"date": datetime.now().isoformat(timespec="seconds"),` dans le traitement courant.
            f.write(json.dumps({"date": datetime.now().isoformat(timespec="seconds"),
                                # Cette ligne exécute `"question": question, "raison": reason}, ensure_ascii=False) + "\n")` dans le traitement courant.
                                "question": question, "raison": reason}, ensure_ascii=False) + "\n")
    # Cette ligne intercepte les erreurs correspondant à `OSError`.
    except OSError:
        # Cette ligne laisse volontairement ce bloc vide pour le moment.
        pass


# Cette ligne affecte les passages extraits des fiches avec `load_chunks(BASE / "fiches")`.
chunks = load_chunks(BASE / "fiches")
# Cette ligne affecte le moteur de recherche documentaire avec `create_index(chunks)`.
index = create_index(chunks)

# Cette ligne affecte l’application web FastAPI avec `FastAPI(title="Chatbot intégration")`.
app = FastAPI(title="Chatbot intégration")
# Cette ligne exécute `app.mount("/static", StaticFiles(directory=BASE / "static"), name="static")` dans le traitement courant.
app.mount("/static", StaticFiles(directory=BASE / "static"), name="static")


# Cette ligne déclare une route HTTP FastAPI avec le décorateur on_event.
@app.on_event("startup")
# Cette définition sert à Tente de créer les tables PostgreSQL au démarrage si la base est joignable .
def on_startup():
    # Cette ligne exécute `"""Tente de créer les tables PostgreSQL au démarrage si la base est joignable."""` dans le traitement courant.
    """Tente de créer les tables PostgreSQL au démarrage si la base est joignable."""
    # commentaire  # Cette chaîne documente le module, la classe ou la fonction.
    if isinstance(index, HybridSearch):
        # Cette ligne exécute `index.prepare()` dans le traitement courant.
        index.prepare()
    # Cette ligne ouvre un bloc dont les erreurs seront traitées dans les clauses except.
    try:
        # Cette ligne importe les dépendances nécessaires : from database import engine, Base.
        from database import engine, Base
        # Cette ligne importe les dépendances nécessaires : import db_models.
        import db_models
        # Cette ligne exécute `Base.metadata.create_all(bind=engine)` dans le traitement courant.
        Base.metadata.create_all(bind=engine)
        # Cette ligne écrit une information de suivi : `print("PostgreSQL connecté et tables synchronisées.")`.
        print("PostgreSQL connecté et tables synchronisées.")
    # Cette ligne intercepte les erreurs correspondant à `Exception as e`.
    except Exception as e:
        # Cette ligne écrit une information de suivi : `print(f"Initialisation PostgreSQL au démarrage ignorée ({e}). Utilisez init_db.py si nécessaire.")`.
        print(f"Initialisation PostgreSQL au démarrage ignorée ({e}). Utilisez init_db.py si nécessaire.")


# Cette définition sert à Données obligatoires et facultatives envoyées lors d'une inscription .
class SignupRequest(BaseModel):
    # Cette ligne exécute `"""Données obligatoires et facultatives envoyées lors d'une inscription."""` dans le traitement courant.
    """Données obligatoires et facultatives envoyées lors d'une inscription."""
    # commentaire  # Cette chaîne documente le module, la classe ou la fonction.
    name: str
    # Cette ligne exécute `matricule: str` dans le traitement courant.
    matricule: str
    # Cette ligne laisse volontairement ce bloc vide pour le moment.
    password: str
    # Cette ligne affecte la variable `role` avec `"Nouvel Arrivant (Tronc Commun)"`.
    role: str = "Nouvel Arrivant (Tronc Commun)"
    # Cette ligne affecte la variable `lang` avec `"fr"`.
    lang: str = "fr"
    # Cette ligne affecte la variable `email` avec `None`.
    email: Optional[str] = None


# Cette définition sert à Identifiants nécessaires pour ouvrir une session utilisateur .
class LoginRequest(BaseModel):
    # Cette ligne exécute `"""Identifiants nécessaires pour ouvrir une session utilisateur."""` dans le traitement courant.
    """Identifiants nécessaires pour ouvrir une session utilisateur."""
    # commentaire  # Cette chaîne documente le module, la classe ou la fonction.
    matricule: str
    # Cette ligne laisse volontairement ce bloc vide pour le moment.
    password: str


# Cette définition sert à Question du chat, avec historique éventuel et préférences d'affichage .
class Question(BaseModel):
    # Cette ligne exécute `"""Question du chat, avec historique éventuel et préférences d'affichage."""` dans le traitement courant.
    """Question du chat, avec historique éventuel et préférences d'affichage."""
    # commentaire  # Cette chaîne documente le module, la classe ou la fonction.
    question: str
    # Cette ligne affecte les précédents messages de la conversation avec `[]`.
    history: list[dict] = []
    # Cette ligne affecte la variable `show_sources` avec `False  # désactivé par défaut : l'écran n'affiche plus les sources`.
    show_sources: bool = False  # désactivé par défaut : l'écran n'affiche plus les sources
    # Cette ligne affecte la variable `user_matricule` avec `None`.
    user_matricule: Optional[str] = None


# Cette définition sert à Formate les passages retrouvés pour les transmettre au modèle avec leur source .
def build_context(hits) -> str:
    # Cette ligne exécute `"""Formate les passages retrouvés pour les transmettre au modèle avec leur source."""` dans le traitement courant.
    """Formate les passages retrouvés pour les transmettre au modèle avec leur source."""
    # commentaire  # Cette chaîne documente le module, la classe ou la fonction.
    return "\n\n".join(
        # Cette ligne exécute `f"[{c.doc_name} > {c.section}]\n{c.text}" for _, c in hits` dans le traitement courant.
        f"[{c.doc_name} > {c.section}]\n{c.text}" for _, c in hits
    # Cette ligne exécute `)` dans le traitement courant.
    )


# Cette définition sert à Appelle Gemini avec 2 essais par modèle, puis passe aux modèles de secours (erreurs 503/429/404) .
def gemini_generate(payload: dict, timeout: int = 60) -> dict:
    # Cette ligne exécute `"""Appelle Gemini avec 2 essais par modèle, puis passe aux modèles de secours (erreurs 503/429/404)."""` dans le traitement courant.
    """Appelle Gemini avec 2 essais par modèle, puis passe aux modèles de secours (erreurs 503/429/404)."""
    # commentaire  # Cette chaîne documente le module, la classe ou la fonction.
    models = [GEMINI_MODEL] + [m.strip() for m in GEMINI_FALLBACKS if m.strip() and m.strip() != GEMINI_MODEL]
    # Cette ligne affecte la variable `last` avec `RuntimeError("aucun modèle")`.
    last: Exception = RuntimeError("aucun modèle")
    # Cette ligne affecte la variable `apiKey` avec `os.getenv("GEMINI_API_KEY", "") or GEMINI_KEY`.
    apiKey = os.getenv("GEMINI_API_KEY", "") or GEMINI_KEY
    # Cette ligne parcourt `model in models` pour traiter chaque élément.
    for model in models:
        # Cette ligne affecte la variable `url` avec `f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"`.
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        # Cette ligne parcourt `attempt in range(2)` pour traiter chaque élément.
        for attempt in range(2):
            # Cette ligne affecte la variable `req` avec `urllib.request.Request(url, data=json.dumps(payload).encode(),`.
            req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                                         # Cette ligne affecte la variable `headers` avec `{"Content-Type": "application/json", "x-goog-api-key": apiKey})`.
                                         headers={"Content-Type": "application/json", "x-goog-api-key": apiKey})
            # Cette ligne ouvre un bloc dont les erreurs seront traitées dans les clauses except.
            try:
                # Cette ligne ouvre la ressource `urllib.request.urlopen(req, timeout=timeout) as r` et garantit sa fermeture à la fin du bloc.
                with urllib.request.urlopen(req, timeout=timeout) as r:
                    # Cette ligne renvoie `json.loads(r.read())` au code qui a appelé la fonction.
                    return json.loads(r.read())
            # Cette ligne intercepte les erreurs correspondant à `urllib.error.HTTPError as e`.
            except urllib.error.HTTPError as e:
                # Cette ligne affecte la variable `last` avec `e`.
                last = e
                # Cette ligne vérifie la condition `e.code == 404` avant d’exécuter le bloc.
                if e.code == 404:
                    # Cette ligne exécute `break                      # modèle inexistant : on passe au suivant` dans le traitement courant.
                    break                      # modèle inexistant : on passe au suivant
                # Cette ligne vérifie la condition `e.code in (429, 500, 502, 503, 504)` avant d’exécuter le bloc.
                if e.code in (429, 500, 502, 503, 504):
                    # Cette ligne exécute `time.sleep(1.5 * (attempt + 1))` dans le traitement courant.
                    time.sleep(1.5 * (attempt + 1))
                    # Cette ligne exécute `continue                   # surcharge temporaire : on réessaie` dans le traitement courant.
                    continue                   # surcharge temporaire : on réessaie
                # Cette ligne exécute `raise` dans le traitement courant.
                raise
            # Cette ligne intercepte les erreurs correspondant à `urllib.error.URLError as e`.
            except urllib.error.URLError as e:
                # Cette ligne affecte la variable `last` avec `e`.
                last = e
                # Cette ligne exécute `time.sleep(1.5)` dans le traitement courant.
                time.sleep(1.5)
    # Cette ligne signale l’erreur `last` et interrompt le traitement courant.
    raise last


# Cette ligne affecte la variable `LANG_FR` avec `"Langue de la réponse : français uniquement. N'écris aucun mot en arabe."`.
LANG_FR = "Langue de la réponse : français uniquement. N'écris aucun mot en arabe."
# Cette ligne affecte la variable `LANG_AR` avec `("Langue de la réponse : arabe standard moderne simplifié (الفصحى المبسطة) uniquement, avec des mots courants `.
LANG_AR = ("Langue de la réponse : arabe standard moderne simplifié (الفصحى المبسطة) uniquement, avec des mots courants "
           # Cette ligne exécute `"et des phrases courtes. N'écris jamais en dialecte (ni marocain, ni tunisien). "` dans le traitement courant.
           "et des phrases courtes. N'écris jamais en dialecte (ni marocain, ni tunisien). "
           # Cette ligne exécute `"Garde entre parenthèses le mot technique français, par exemple : التقشير (dénudage).")` dans le traitement courant.
           "Garde entre parenthèses le mot technique français, par exemple : التقشير (dénudage).")


# Cette définition sert à Construit les messages du modèle en limitant l'historique aux six derniers échanges .
def make_messages(question: str, history: list[dict], context: str) -> list[dict]:
    # Cette ligne exécute `"""Construit les messages du modèle en limitant l'historique aux six derniers échanges."""` dans le traitement courant.
    """Construit les messages du modèle en limitant l'historique aux six derniers échanges."""
    # commentaire  # Cette chaîne documente le module, la classe ou la fonction.
    messages = [m for m in history[-6:] if m.get("role") in ("user", "assistant")]
    # Cette ligne exécute `messages.append({"role": "user",` dans le traitement courant.
    messages.append({"role": "user",
                     # Cette ligne exécute `"content": f"<sources>\n{context}\n</sources>\n\nQuestion : {question}\n\n{LANG_AR if has_non_latin(question) else LANG_FR}"})` dans le traitement courant.
                     "content": f"<sources>\n{context}\n</sources>\n\nQuestion : {question}\n\n{LANG_AR if has_non_latin(question) else LANG_FR}"})
    # Cette ligne renvoie `messages` au code qui a appelé la fonction.
    return messages


# Cette définition sert à Envoie la conversation au modèle Ollama configuré sur le réseau local .
def answer_ollama(question: str, history: list[dict], context: str) -> str:
    # Cette ligne exécute `"""Envoie la conversation au modèle Ollama configuré sur le réseau local."""` dans le traitement courant.
    """Envoie la conversation au modèle Ollama configuré sur le réseau local."""
    # commentaire  # Cette chaîne documente le module, la classe ou la fonction.
    payload = {
        # Cette ligne exécute `"model": OLLAMA_MODEL,` dans le traitement courant.
        "model": OLLAMA_MODEL,
        # Cette ligne exécute `"stream": False,` dans le traitement courant.
        "stream": False,
        # Cette ligne exécute `"options": {"temperature": 0.2},` dans le traitement courant.
        "options": {"temperature": 0.2},
        # Cette ligne exécute `"messages": [{"role": "system", "content": SYSTEM_PROMPT}] + make_messages(question, history, context),` dans le traitement courant.
        "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + make_messages(question, history, context),
    # Cette ligne exécute `}` dans le traitement courant.
    }
    # Cette ligne affecte la variable `req` avec `urllib.request.Request(f"{OLLAMA_URL}/api/chat", data=json.dumps(payload).encode(),`.
    req = urllib.request.Request(f"{OLLAMA_URL}/api/chat", data=json.dumps(payload).encode(),
                                 # Cette ligne affecte la variable `headers` avec `{"Content-Type": "application/json"})`.
                                 headers={"Content-Type": "application/json"})
    # Cette ligne ouvre la ressource `urllib.request.urlopen(req, timeout=180) as r` et garantit sa fermeture à la fin du bloc.
    with urllib.request.urlopen(req, timeout=180) as r:
        # Cette ligne renvoie `json.loads(r.read())["message"]["content"]` au code qui a appelé la fonction.
        return json.loads(r.read())["message"]["content"]


# Cette définition sert à Prépare et envoie la requête au service Gemini, puis extrait son texte .
def answer_gemini(question: str, history: list[dict], context: str) -> str:
    # Cette ligne exécute `"""Prépare et envoie la requête au service Gemini, puis extrait son texte."""` dans le traitement courant.
    """Prépare et envoie la requête au service Gemini, puis extrait son texte."""
    # commentaire  # Cette chaîne documente le module, la classe ou la fonction.
    msgs = make_messages(question, history, context)
    # Cette ligne affecte les données envoyées au service externe avec `{`.
    payload = {
        # Cette ligne exécute `"systemInstruction": {"parts": [{"text": SYSTEM_PROMPT}]},` dans le traitement courant.
        "systemInstruction": {"parts": [{"text": SYSTEM_PROMPT}]},
        # Cette ligne exécute `"contents": [{"role": "model" if m["role"] == "assistant" else "user",` dans le traitement courant.
        "contents": [{"role": "model" if m["role"] == "assistant" else "user",
                      # Cette ligne exécute `"parts": [{"text": m["content"]}]} for m in msgs],` dans le traitement courant.
                      "parts": [{"text": m["content"]}]} for m in msgs],
        # Cette ligne exécute `"generationConfig": {"temperature": 0.2, "maxOutputTokens": 1000},` dans le traitement courant.
        "generationConfig": {"temperature": 0.2, "maxOutputTokens": 1000},
    # Cette ligne exécute `}` dans le traitement courant.
    }
    # Cette ligne affecte les données reçues avec `gemini_generate(payload)`.
    data = gemini_generate(payload)
    # Cette ligne renvoie `"".join(p.get("text", "") for p in data["candidates"][0]["content"]["parts"])` au code qui a appelé la fonction.
    return "".join(p.get("text", "") for p in data["candidates"][0]["content"]["parts"])


# Cette définition sert à Appelle le fournisseur Anthropic lorsque ce fournisseur est sélectionné .
def answer_anthropic(question: str, history: list[dict], context: str) -> str:
    # Cette ligne exécute `"""Appelle le fournisseur Anthropic lorsque ce fournisseur est sélectionné."""` dans le traitement courant.
    """Appelle le fournisseur Anthropic lorsque ce fournisseur est sélectionné."""
    # commentaire  # Cette chaîne documente le module, la classe ou la fonction.
    import anthropic
    # Cette ligne affecte la variable `client` avec `anthropic.Anthropic()`.
    client = anthropic.Anthropic()
    # Cette ligne affecte la variable `resp` avec `client.messages.create(model=CLAUDE_MODEL, max_tokens=1000, system=SYSTEM_PROMPT,`.
    resp = client.messages.create(model=CLAUDE_MODEL, max_tokens=1000, system=SYSTEM_PROMPT,
                                  # Cette ligne affecte la variable `messages` avec `make_messages(question, history, context))`.
                                  messages=make_messages(question, history, context))
    # Cette ligne renvoie `"".join(b.text for b in resp.content if b.type == "text")` au code qui a appelé la fonction.
    return "".join(b.text for b in resp.content if b.type == "text")


# Cette définition sert à Choisit le fournisseur de génération configuré et produit une réponse .
def answer_with_llm(question: str, history: list[dict], context: str) -> str:
    # Cette ligne exécute `"""Choisit le fournisseur de génération configuré et produit une réponse."""` dans le traitement courant.
    """Choisit le fournisseur de génération configuré et produit une réponse."""
    # commentaire  # Cette chaîne documente le module, la classe ou la fonction.
    if PROVIDER == "anthropic":
        # Cette ligne renvoie `answer_anthropic(question, history, context)` au code qui a appelé la fonction.
        return answer_anthropic(question, history, context)
    # Cette ligne vérifie la condition `PROVIDER == "gemini"` avant d’exécuter le bloc.
    if PROVIDER == "gemini":
        # Cette ligne renvoie `answer_gemini(question, history, context)` au code qui a appelé la fonction.
        return answer_gemini(question, history, context)
    # Cette ligne renvoie `answer_ollama(question, history, context)` au code qui a appelé la fonction.
    return answer_ollama(question, history, context)


# Cette définition sert à Indique si le service Ollama local répond à une requête de disponibilité .
def ollama_ready() -> bool:
    # Cette ligne exécute `"""Indique si le service Ollama local répond à une requête de disponibilité."""` dans le traitement courant.
    """Indique si le service Ollama local répond à une requête de disponibilité."""
    # commentaire  # Cette chaîne documente le module, la classe ou la fonction.
    try:
        # Cette ligne ouvre la ressource `urllib.request.urlopen(f"{OLLAMA_URL}/api/tags", timeout=2) as r` et garantit sa fermeture à la fin du bloc.
        with urllib.request.urlopen(f"{OLLAMA_URL}/api/tags", timeout=2) as r:
            # Cette ligne affecte la variable `models` avec `[m["name"] for m in json.loads(r.read()).get("models", [])]`.
            models = [m["name"] for m in json.loads(r.read()).get("models", [])]
        # Cette ligne renvoie `any(m == OLLAMA_MODEL or m.startswith(OLLAMA_MODEL + ":") or m.split(":")[0] == OLLAMA_MODEL for m in models)` au code qui a appelé la fonction.
        return any(m == OLLAMA_MODEL or m.startswith(OLLAMA_MODEL + ":") or m.split(":")[0] == OLLAMA_MODEL for m in models)
    # Cette ligne intercepte les erreurs correspondant à `Exception`.
    except Exception:
        # Cette ligne renvoie `False` au code qui a appelé la fonction.
        return False


# Cette ligne affecte la variable `REWRITE_PROMPT` avec `("Tu aides un moteur de recherche d'une usine de faisceaux de câbles pour l'automobile. "`.
REWRITE_PROMPT = ("Tu aides un moteur de recherche d'une usine de faisceaux de câbles pour l'automobile. "
                  # Cette ligne exécute `"Traduis la question de l'employé (arabe, darija ou autre) en UNE question courte en français simple, "` dans le traitement courant.
                  "Traduis la question de l'employé (arabe, darija ou autre) en UNE question courte en français simple, "
                  # Cette ligne exécute `"avec les mots du métier (machine, coupe, sertissage, assemblage, sécurité, formation…). "` dans le traitement courant.
                  "avec les mots du métier (machine, coupe, sertissage, assemblage, sécurité, formation…). "
                  # Cette ligne exécute `"Réponds uniquement par cette question en français, sans explication.\n\nQuestion : ")` dans le traitement courant.
                  "Réponds uniquement par cette question en français, sans explication.\n\nQuestion : ")


# Cette définition sert à Petit appel au modèle (sans sources) : sert à traduire / reformuler la question .
def simple_complete(prompt: str) -> str:
    # Cette ligne exécute `"""Petit appel au modèle (sans sources) : sert à traduire / reformuler la question."""` dans le traitement courant.
    """Petit appel au modèle (sans sources) : sert à traduire / reformuler la question."""
    # commentaire  # Cette chaîne documente le module, la classe ou la fonction.
    if PROVIDER == "gemini":
        # Cette ligne affecte les données envoyées au service externe avec `{"contents": [{"role": "user", "parts": [{"text": prompt}]}],`.
        payload = {"contents": [{"role": "user", "parts": [{"text": prompt}]}],
                   # Cette ligne exécute `"generationConfig": {"temperature": 0, "maxOutputTokens": 120}}` dans le traitement courant.
                   "generationConfig": {"temperature": 0, "maxOutputTokens": 120}}
        # Cette ligne affecte les données reçues avec `gemini_generate(payload)`.
        data = gemini_generate(payload)
        # Cette ligne renvoie `"".join(p.get("text", "") for p in data["candidates"][0]["content"]["parts"]).strip()` au code qui a appelé la fonction.
        return "".join(p.get("text", "") for p in data["candidates"][0]["content"]["parts"]).strip()
    # Cette ligne vérifie la condition `PROVIDER == "anthropic"` avant d’exécuter le bloc.
    if PROVIDER == "anthropic":
        # Cette ligne importe les dépendances nécessaires : import anthropic.
        import anthropic
        # Cette ligne affecte la variable `resp` avec `anthropic.Anthropic().messages.create(model=CLAUDE_MODEL, max_tokens=120,`.
        resp = anthropic.Anthropic().messages.create(model=CLAUDE_MODEL, max_tokens=120,
                                                     # Cette ligne affecte la variable `messages` avec `[{"role": "user", "content": prompt}])`.
                                                     messages=[{"role": "user", "content": prompt}])
        # Cette ligne renvoie `"".join(b.text for b in resp.content if b.type == "text").strip()` au code qui a appelé la fonction.
        return "".join(b.text for b in resp.content if b.type == "text").strip()
    # Cette ligne affecte les données envoyées au service externe avec `{"model": OLLAMA_MODEL, "stream": False, "options": {"temperature": 0},`.
    payload = {"model": OLLAMA_MODEL, "stream": False, "options": {"temperature": 0},
               # Cette ligne exécute `"messages": [{"role": "user", "content": prompt}]}` dans le traitement courant.
               "messages": [{"role": "user", "content": prompt}]}
    # Cette ligne affecte la variable `req` avec `urllib.request.Request(f"{OLLAMA_URL}/api/chat", data=json.dumps(payload).encode(),`.
    req = urllib.request.Request(f"{OLLAMA_URL}/api/chat", data=json.dumps(payload).encode(),
                                 # Cette ligne affecte la variable `headers` avec `{"Content-Type": "application/json"})`.
                                 headers={"Content-Type": "application/json"})
    # Cette ligne ouvre la ressource `urllib.request.urlopen(req, timeout=120) as r` et garantit sa fermeture à la fin du bloc.
    with urllib.request.urlopen(req, timeout=120) as r:
        # Cette ligne renvoie `json.loads(r.read())["message"]["content"].strip()` au code qui a appelé la fonction.
        return json.loads(r.read())["message"]["content"].strip()


# Cette définition sert à Détecte les caractères non latins afin de choisir les consignes de langue arabe .
def has_non_latin(text: str) -> bool:
    # Cette ligne exécute `"""Détecte les caractères non latins afin de choisir les consignes de langue arabe."""` dans le traitement courant.
    """Détecte les caractères non latins afin de choisir les consignes de langue arabe."""
    # commentaire  # Cette chaîne documente le module, la classe ou la fonction.
    return any(ord(c) > 0x024F and c.isalpha() for c in text)


# Cette ligne affecte la variable `LAST_REWRITE_ERROR` avec `""`.
LAST_REWRITE_ERROR = ""


# Cette définition sert à Traduit la question en français pour la recherche. En cas d'échec, garde la question d'origine .
def rewrite_query(question: str) -> str:
    # Cette ligne exécute `"""Traduit la question en français pour la recherche. En cas d'échec, garde la question d'origine."""` dans le traitement courant.
    """Traduit la question en français pour la recherche. En cas d'échec, garde la question d'origine."""
    # commentaire  # Cette chaîne documente le module, la classe ou la fonction.
    global LAST_REWRITE_ERROR
    # Cette ligne affecte la variable `LAST_REWRITE_ERROR` avec `""`.
    LAST_REWRITE_ERROR = ""
    # Cette ligne ouvre un bloc dont les erreurs seront traitées dans les clauses except.
    try:
        # Cette ligne affecte la variable `out` avec `simple_complete(REWRITE_PROMPT + question)`.
        out = simple_complete(REWRITE_PROMPT + question)
        # Cette ligne renvoie `out.splitlines()[0].strip() if out else question` au code qui a appelé la fonction.
        return out.splitlines()[0].strip() if out else question
    # Cette ligne intercepte les erreurs correspondant à `Exception as e`.
    except Exception as e:
        # Cette ligne affecte la variable `LAST_REWRITE_ERROR` avec `f"{type(e).__name__}: {e}"`.
        LAST_REWRITE_ERROR = f"{type(e).__name__}: {e}"
        # Cette ligne écrit une information de suivi : `print(f"[traduction] erreur : {LAST_REWRITE_ERROR}", flush=True)`.
        print(f"[traduction] erreur : {LAST_REWRITE_ERROR}", flush=True)
        # Cette ligne renvoie `question` au code qui a appelé la fonction.
        return question


# Cette ligne déclare une route HTTP FastAPI avec le décorateur get.
@app.get("/")
# Cette ligne déclare une route HTTP FastAPI avec le décorateur get.
@app.get("/login")
# Cette ligne déclare une route HTTP FastAPI avec le décorateur get.
@app.get("/accueil")
# Cette ligne déclare une route HTTP FastAPI avec le décorateur get.
@app.get("/chat-page")
# Cette définition sert à Retourne la page HTML principale du portail .
def home():
    # Cette ligne exécute `"""Retourne la page HTML principale du portail."""` dans le traitement courant.
    """Retourne la page HTML principale du portail."""
    # commentaire  # Cette chaîne documente le module, la classe ou la fonction.
    return FileResponse(BASE / "static" / "index.html", headers={"Cache-Control": "no-store"})


# Cette ligne déclare une route HTTP FastAPI avec le décorateur get.
@app.get("/api/modules")
# Cette définition sert à Liste les modules de formation et fiches disponibles dans la base RAG .
def api_modules():
    # Cette ligne exécute `"""Liste les modules de formation et fiches disponibles dans la base RAG."""` dans le traitement courant.
    """Liste les modules de formation et fiches disponibles dans la base RAG."""
    # commentaire  # Cette chaîne documente le module, la classe ou la fonction.
    docs = {}
    # Cette ligne parcourt `c in chunks` pour traiter chaque élément.
    for c in chunks:
        # Cette ligne vérifie la condition `c.doc_id not in docs` avant d’exécuter le bloc.
        if c.doc_id not in docs:
            # Cette ligne exécute `docs[c.doc_id] = {` dans le traitement courant.
            docs[c.doc_id] = {
                # Cette ligne exécute `"id": c.doc_id,` dans le traitement courant.
                "id": c.doc_id,
                # Cette ligne exécute `"nom": c.doc_name,` dans le traitement courant.
                "nom": c.doc_name,
                # Cette ligne exécute `"source": c.source,` dans le traitement courant.
                "source": c.source,
                # Cette ligne exécute `"sections": []` dans le traitement courant.
                "sections": []
            # Cette ligne exécute `}` dans le traitement courant.
            }
        # Cette ligne vérifie la condition `c.section not in docs[c.doc_id]["sections"]` avant d’exécuter le bloc.
        if c.section not in docs[c.doc_id]["sections"]:
            # Cette ligne exécute `docs[c.doc_id]["sections"].append(c.section)` dans le traitement courant.
            docs[c.doc_id]["sections"].append(c.section)
    # Cette ligne renvoie `{"modules": list(docs.values()), "total_chunks": len(chunks)}` au code qui a appelé la fonction.
    return {"modules": list(docs.values()), "total_chunks": len(chunks)}



# Cette ligne déclare une route HTTP FastAPI avec le décorateur get.
@app.get("/health")
# Cette définition sert à Expose l'état du service, de la recherche documentaire et du fournisseur LLM .
def health():
    # Cette ligne exécute `"""Expose l'état du service, de la recherche documentaire et du fournisseur LLM."""` dans le traitement courant.
    """Expose l'état du service, de la recherche documentaire et du fournisseur LLM."""
    # commentaire  # Cette chaîne documente le module, la classe ou la fonction.
    retrieval = index.status() if isinstance(index, HybridSearch) else {"mode": "bm25"}
    # Cette ligne vérifie la condition `PROVIDER == "gemini"` avant d’exécuter le bloc.
    if PROVIDER == "gemini":
        # Cette ligne renvoie `{"chunks": len(chunks), "provider": "gemini", "llm": bool(GEMINI_KEY), "model": GEMINI_MODEL, "retrieval": retrieval}` au code qui a appelé la fonction.
        return {"chunks": len(chunks), "provider": "gemini", "llm": bool(GEMINI_KEY), "model": GEMINI_MODEL, "retrieval": retrieval}
    # Cette ligne vérifie la condition `PROVIDER == "anthropic"` avant d’exécuter le bloc.
    if PROVIDER == "anthropic":
        # Cette ligne renvoie `{"chunks": len(chunks), "provider": "anthropic", "llm": bool(os.getenv("ANTHROPIC_API_KEY")), "model": CLAUDE_MODEL, "retrieval": retrieval}` au code qui a appelé la fonction.
        return {"chunks": len(chunks), "provider": "anthropic", "llm": bool(os.getenv("ANTHROPIC_API_KEY")), "model": CLAUDE_MODEL, "retrieval": retrieval}
    # Cette ligne renvoie `{"chunks": len(chunks), "provider": "ollama", "llm": ollama_ready(), "model": OLLAMA_MODEL, "retrieval": retrieval}` au code qui a appelé la fonction.
    return {"chunks": len(chunks), "provider": "ollama", "llm": ollama_ready(), "model": OLLAMA_MODEL, "retrieval": retrieval}


# Cette ligne déclare une route HTTP FastAPI avec le décorateur post.
@app.post("/api/auth/signup")
# Cette définition sert à Enregistre un nouvel utilisateur / opérateur dans PostgreSQL .
def auth_signup(req: SignupRequest):
    # Cette ligne exécute `"""Enregistre un nouvel utilisateur / opérateur dans PostgreSQL."""` dans le traitement courant.
    """Enregistre un nouvel utilisateur / opérateur dans PostgreSQL."""
    # commentaire  # Cette chaîne documente le module, la classe ou la fonction.
    name = req.name.strip()
    # Cette ligne affecte le matricule de l’utilisateur avec `req.matricule.strip()`.
    matricule = req.matricule.strip()
    # Cette ligne laisse volontairement ce bloc vide pour le moment.
    password = req.password.strip()

    # Cette ligne vérifie la condition `not name or not matricule or not password` avant d’exécuter le bloc.
    if not name or not matricule or not password:
        # Cette ligne signale l’erreur `HTTPException(` et interrompt le traitement courant.
        raise HTTPException(
            # Cette ligne affecte la variable `status_code` avec `status.HTTP_400_BAD_REQUEST,`.
            status_code=status.HTTP_400_BAD_REQUEST,
            # Cette ligne affecte la variable `detail` avec `"Le nom, le matricule et le mot de passe sont obligatoires."`.
            detail="Le nom, le matricule et le mot de passe sont obligatoires."
        # Cette ligne exécute `)` dans le traitement courant.
        )

    # Cette ligne vérifie la condition `len(password) < 4` avant d’exécuter le bloc.
    if len(password) < 4:
        # Cette ligne signale l’erreur `HTTPException(` et interrompt le traitement courant.
        raise HTTPException(
            # Cette ligne affecte la variable `status_code` avec `status.HTTP_400_BAD_REQUEST,`.
            status_code=status.HTTP_400_BAD_REQUEST,
            # Cette ligne affecte la variable `detail` avec `"Le mot de passe doit comporter au moins 4 caractères."`.
            detail="Le mot de passe doit comporter au moins 4 caractères."
        # Cette ligne exécute `)` dans le traitement courant.
        )

    # Cette ligne ouvre un bloc dont les erreurs seront traitées dans les clauses except.
    try:
        # Cette ligne importe les dépendances nécessaires : from database import SessionLocal.
        from database import SessionLocal
        # Cette ligne importe les dépendances nécessaires : from db_models import User.
        from db_models import User
        # Cette ligne importe les dépendances nécessaires : from auth import hash_password.
        from auth import hash_password

        # Cette ligne ouvre la ressource `SessionLocal() as db` et garantit sa fermeture à la fin du bloc.
        with SessionLocal() as db:
            # Vérifier si le matricule existe déjà
            # Cette ligne affecte la variable `existing` avec `db.query(User).filter(User.matricule == matricule).first()`.
            existing = db.query(User).filter(User.matricule == matricule).first()
            # Cette ligne vérifie la condition `existing` avant d’exécuter le bloc.
            if existing:
                # Cette ligne signale l’erreur `HTTPException(` et interrompt le traitement courant.
                raise HTTPException(
                    # Cette ligne affecte la variable `status_code` avec `status.HTTP_400_BAD_REQUEST,`.
                    status_code=status.HTTP_400_BAD_REQUEST,
                    # Cette ligne affecte la variable `detail` avec `f"Le matricule '{matricule}' est déjà enregistré. Veuillez vous connecter."`.
                    detail=f"Le matricule '{matricule}' est déjà enregistré. Veuillez vous connecter."
                # Cette ligne exécute `)` dans le traitement courant.
                )

            # Vérifier l'email s'il est renseigné
            # Cette ligne vérifie la condition `req.email and req.email.strip()` avant d’exécuter le bloc.
            if req.email and req.email.strip():
                # Cette ligne affecte la variable `existing_email` avec `db.query(User).filter(User.email == req.email.strip()).first()`.
                existing_email = db.query(User).filter(User.email == req.email.strip()).first()
                # Cette ligne vérifie la condition `existing_email` avant d’exécuter le bloc.
                if existing_email:
                    # Cette ligne signale l’erreur `HTTPException(` et interrompt le traitement courant.
                    raise HTTPException(
                        # Cette ligne affecte la variable `status_code` avec `status.HTTP_400_BAD_REQUEST,`.
                        status_code=status.HTTP_400_BAD_REQUEST,
                        # Cette ligne affecte la variable `detail` avec `"Cette adresse email est déjà associée à un compte."`.
                        detail="Cette adresse email est déjà associée à un compte."
                    # Cette ligne exécute `)` dans le traitement courant.
                    )

            # Cette ligne affecte l’utilisateur enregistré avec `User(`.
            user = User(
                # Cette ligne affecte la variable `name` avec `name,`.
                name=name,
                # Cette ligne affecte le matricule de l’utilisateur avec `matricule,`.
                matricule=matricule,
                # Cette ligne affecte la variable `email` avec `req.email.strip() if req.email else None,`.
                email=req.email.strip() if req.email else None,
                # Cette ligne laisse volontairement ce bloc vide pour le moment.
                password_hash=hash_password(password),
                # Cette ligne affecte la variable `role` avec `req.role or "Nouvel Arrivant (Tronc Commun)",`.
                role=req.role or "Nouvel Arrivant (Tronc Commun)",
                # Cette ligne affecte la variable `lang` avec `req.lang or "fr",`.
                lang=req.lang or "fr",
            # Cette ligne exécute `)` dans le traitement courant.
            )
            # Cette ligne exécute `db.add(user)` dans le traitement courant.
            db.add(user)
            # Cette ligne exécute `db.commit()` dans le traitement courant.
            db.commit()
            # Cette ligne exécute `db.refresh(user)` dans le traitement courant.
            db.refresh(user)

            # Cette ligne renvoie `{` au code qui a appelé la fonction.
            return {
                # Cette ligne exécute `"success": True,` dans le traitement courant.
                "success": True,
                # Cette ligne exécute `"message": "Inscription réussie !",` dans le traitement courant.
                "message": "Inscription réussie !",
                # Cette ligne exécute `"user": user.to_dict()` dans le traitement courant.
                "user": user.to_dict()
            # Cette ligne exécute `}` dans le traitement courant.
            }
    # Cette ligne intercepte les erreurs correspondant à `HTTPException`.
    except HTTPException:
        # Cette ligne exécute `raise` dans le traitement courant.
        raise
    # Cette ligne intercepte les erreurs correspondant à `Exception as e`.
    except Exception as e:
        # Cette ligne écrit une information de suivi : `print(f"[PostgreSQL Auth Signup] {e}", flush=True)`.
        print(f"[PostgreSQL Auth Signup] {e}", flush=True)
        # Cette ligne signale l’erreur `HTTPException(` et interrompt le traitement courant.
        raise HTTPException(
            # Cette ligne affecte la variable `status_code` avec `status.HTTP_500_INTERNAL_SERVER_ERROR,`.
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            # Cette ligne affecte la variable `detail` avec `f"Erreur de base de données PostgreSQL : {e}"`.
            detail=f"Erreur de base de données PostgreSQL : {e}"
        # Cette ligne exécute `)` dans le traitement courant.
        )


# Cette ligne déclare une route HTTP FastAPI avec le décorateur post.
@app.post("/api/auth/login")
# Cette définition sert à Authentifie un utilisateur avec son matricule et son mot de passe depuis PostgreSQL .
def auth_login(req: LoginRequest):
    # Cette ligne exécute `"""Authentifie un utilisateur avec son matricule et son mot de passe depuis PostgreSQL."""` dans le traitement courant.
    """Authentifie un utilisateur avec son matricule et son mot de passe depuis PostgreSQL."""
    # commentaire  # Cette chaîne documente le module, la classe ou la fonction.
    matricule = req.matricule.strip()
    # Cette ligne laisse volontairement ce bloc vide pour le moment.
    password = req.password.strip()

    # Cette ligne vérifie la condition `not matricule or not password` avant d’exécuter le bloc.
    if not matricule or not password:
        # Cette ligne signale l’erreur `HTTPException(` et interrompt le traitement courant.
        raise HTTPException(
            # Cette ligne affecte la variable `status_code` avec `status.HTTP_400_BAD_REQUEST,`.
            status_code=status.HTTP_400_BAD_REQUEST,
            # Cette ligne affecte la variable `detail` avec `"Veuillez fournir votre matricule et votre mot de passe."`.
            detail="Veuillez fournir votre matricule et votre mot de passe."
        # Cette ligne exécute `)` dans le traitement courant.
        )

    # Cette ligne ouvre un bloc dont les erreurs seront traitées dans les clauses except.
    try:
        # Cette ligne importe les dépendances nécessaires : from database import SessionLocal.
        from database import SessionLocal
        # Cette ligne importe les dépendances nécessaires : from db_models import User.
        from db_models import User
        # Cette ligne importe les dépendances nécessaires : from auth import verify_password.
        from auth import verify_password

        # Cette ligne ouvre la ressource `SessionLocal() as db` et garantit sa fermeture à la fin du bloc.
        with SessionLocal() as db:
            # Cette ligne affecte l’utilisateur enregistré avec `db.query(User).filter(User.matricule == matricule).first()`.
            user = db.query(User).filter(User.matricule == matricule).first()
            # Cette ligne vérifie la condition `not user or not verify_password(user.password_hash, password)` avant d’exécuter le bloc.
            if not user or not verify_password(user.password_hash, password):
                # Cette ligne signale l’erreur `HTTPException(` et interrompt le traitement courant.
                raise HTTPException(
                    # Cette ligne affecte la variable `status_code` avec `status.HTTP_401_UNAUTHORIZED,`.
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    # Cette ligne affecte la variable `detail` avec `"Matricule ou mot de passe incorrect."`.
                    detail="Matricule ou mot de passe incorrect."
                # Cette ligne exécute `)` dans le traitement courant.
                )

            # Cette ligne renvoie `{` au code qui a appelé la fonction.
            return {
                # Cette ligne exécute `"success": True,` dans le traitement courant.
                "success": True,
                # Cette ligne exécute `"message": "Connexion réussie !",` dans le traitement courant.
                "message": "Connexion réussie !",
                # Cette ligne exécute `"user": user.to_dict()` dans le traitement courant.
                "user": user.to_dict()
            # Cette ligne exécute `}` dans le traitement courant.
            }
    # Cette ligne intercepte les erreurs correspondant à `HTTPException`.
    except HTTPException:
        # Cette ligne exécute `raise` dans le traitement courant.
        raise
    # Cette ligne intercepte les erreurs correspondant à `Exception as e`.
    except Exception as e:
        # Cette ligne écrit une information de suivi : `print(f"[PostgreSQL Auth Login] {e}", flush=True)`.
        print(f"[PostgreSQL Auth Login] {e}", flush=True)
        # Cette ligne signale l’erreur `HTTPException(` et interrompt le traitement courant.
        raise HTTPException(
            # Cette ligne affecte la variable `status_code` avec `status.HTTP_500_INTERNAL_SERVER_ERROR,`.
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            # Cette ligne affecte la variable `detail` avec `f"Erreur de base de données PostgreSQL : {e}"`.
            detail=f"Erreur de base de données PostgreSQL : {e}"
        # Cette ligne exécute `)` dans le traitement courant.
        )


# Cette ligne déclare une route HTTP FastAPI avec le décorateur get.
@app.get("/api/auth/status")
# Cette définition sert à Retourne l'état de la connexion PostgreSQL .
def auth_status():
    # Cette ligne exécute `"""Retourne l'état de la connexion PostgreSQL."""` dans le traitement courant.
    """Retourne l'état de la connexion PostgreSQL."""
    # commentaire  # Cette chaîne documente le module, la classe ou la fonction.
    from database import test_connection, POSTGRES_DB, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_USER
    # Cette ligne exécute `connected, msg = test_connection()` dans le traitement courant.
    connected, msg = test_connection()
    # Cette ligne renvoie `{` au code qui a appelé la fonction.
    return {
        # Cette ligne exécute `"connected": connected,` dans le traitement courant.
        "connected": connected,
        # Cette ligne exécute `"message": msg,` dans le traitement courant.
        "message": msg,
        # Cette ligne exécute `"database": POSTGRES_DB,` dans le traitement courant.
        "database": POSTGRES_DB,
        # Cette ligne exécute `"host": POSTGRES_HOST,` dans le traitement courant.
        "host": POSTGRES_HOST,
        # Cette ligne exécute `"port": POSTGRES_PORT,` dans le traitement courant.
        "port": POSTGRES_PORT,
        # Cette ligne exécute `"user": POSTGRES_USER` dans le traitement courant.
        "user": POSTGRES_USER
    # Cette ligne exécute `}` dans le traitement courant.
    }


# Cette définition sert à Enregistre l'échange dans PostgreSQL sans bloquer le chat si la DB est indisponible .
def save_chat_to_db(question: str, answer: str, user_matricule: Optional[str] = None) -> None:
    # Cette ligne exécute `"""Enregistre l'échange dans PostgreSQL sans bloquer le chat si la DB est indisponible."""` dans le traitement courant.
    """Enregistre l'échange dans PostgreSQL sans bloquer le chat si la DB est indisponible."""
    # commentaire  # Cette chaîne documente le module, la classe ou la fonction.
    try:
        # Cette ligne importe les dépendances nécessaires : from database import SessionLocal.
        from database import SessionLocal
        # Cette ligne importe les dépendances nécessaires : from db_models import QuestionLog.
        from db_models import QuestionLog
        # Cette ligne ouvre la ressource `SessionLocal() as db` et garantit sa fermeture à la fin du bloc.
        with SessionLocal() as db:
            # Cette ligne exécute `db.add(QuestionLog(question=question, answer=answer, user_matricule=user_matricule))` dans le traitement courant.
            db.add(QuestionLog(question=question, answer=answer, user_matricule=user_matricule))
            # Cette ligne exécute `db.commit()` dans le traitement courant.
            db.commit()
    # Cette ligne intercepte les erreurs correspondant à `Exception as e`.
    except Exception as e:
        # Cette ligne écrit une information de suivi : `print(f"[PostgreSQL] Non enregistré : {e}", flush=True)`.
        print(f"[PostgreSQL] Non enregistré : {e}", flush=True)


# Cette ligne déclare une route HTTP FastAPI avec le décorateur post.
@app.post("/chat")
# Cette définition sert à Point d'entrée HTTP du chat, avec traduction des erreurs en réponses API .
def chat(q: Question):
    # Cette ligne exécute `"""Point d'entrée HTTP du chat, avec traduction des erreurs en réponses API."""` dans le traitement courant.
    """Point d'entrée HTTP du chat, avec traduction des erreurs en réponses API."""
    # commentaire  # Cette chaîne documente le module, la classe ou la fonction.
    result = _chat(q)
    # Cette ligne exécute `save_chat_to_db(q.question, result.get("answer", ""), user_matricule=q.user_matricule)` dans le traitement courant.
    save_chat_to_db(q.question, result.get("answer", ""), user_matricule=q.user_matricule)
    # Cette ligne vérifie la condition `not q.show_sources` avant d’exécuter le bloc.
    if not q.show_sources:
        # Cette ligne exécute `result["sources"] = []` dans le traitement courant.
        result["sources"] = []
    # Cette ligne renvoie `result` au code qui a appelé la fonction.
    return result


# Cette définition sert à Recherche les passages, produit la réponse et enregistre l'échange .
def _chat(q: Question):
    # Cette ligne exécute `"""Recherche les passages, produit la réponse et enregistre l'échange."""` dans le traitement courant.
    """Recherche les passages, produit la réponse et enregistre l'échange."""
    # commentaire  # Cette chaîne documente le module, la classe ou la fonction.
    search_text = q.question
    # Cette ligne vérifie la condition `has_non_latin(search_text):          # arabe / darija : on traduit d'abord pour chercher dans les fiches` avant d’exécuter le bloc.
    if has_non_latin(search_text):          # arabe / darija : on traduit d'abord pour chercher dans les fiches
        # Cette ligne affecte la variable `search_text` avec `rewrite_query(search_text)`.
        search_text = rewrite_query(search_text)
    # Cette ligne affecte les passages trouvés par la recherche avec `index.search(search_text, k=6)`.
    hits = index.search(search_text, k=6)
    # Cette ligne vérifie la condition `not hits and search_text == q.question:  # rien trouvé : seconde chance avec une reformulation` avant d’exécuter le bloc.
    if not hits and search_text == q.question:  # rien trouvé : seconde chance avec une reformulation
        # Cette ligne affecte la variable `search_text` avec `rewrite_query(search_text)`.
        search_text = rewrite_query(search_text)
        # Cette ligne affecte les passages trouvés par la recherche avec `index.search(search_text, k=6)`.
        hits = index.search(search_text, k=6)
    # Cette ligne vérifie la condition `hits and not isinstance(index, HybridSearch):  # le seuil BM25 ne s'applique pas aux rangs RRF` avant d’exécuter le bloc.
    if hits and not isinstance(index, HybridSearch):  # le seuil BM25 ne s'applique pas aux rangs RRF
        # Cette ligne affecte la variable `top` avec `hits[0][0]`.
        top = hits[0][0]
        # Cette ligne affecte les passages trouvés par la recherche avec `[h for h in hits if h[0] >= 0.5 * top]`.
        hits = [h for h in hits if h[0] >= 0.5 * top]
    # Cette ligne affecte les références des fiches utilisées avec `[{"fiche": c.doc_name, "section": c.section} for _, c in hits]`.
    sources = [{"fiche": c.doc_name, "section": c.section} for _, c in hits]
    # Cette ligne vérifie la condition `not hits` avant d’exécuter le bloc.
    if not hits:
        # Cette ligne exécute `log_unanswered(q.question, "aucun extrait trouvé")` dans le traitement courant.
        log_unanswered(q.question, "aucun extrait trouvé")
        # Cette ligne affecte la variable `overview` avec `[c for c in chunks if "quoi sert" in c.section.lower() or c.doc_id in ("PROC-INTEGRATION", "GLOSSAIRE")]`.
        overview = [c for c in chunks if "quoi sert" in c.section.lower() or c.doc_id in ("PROC-INTEGRATION", "GLOSSAIRE")]
        # Cette ligne vérifie la condition `not overview or LAST_REWRITE_ERROR` avant d’exécuter le bloc.
        if not overview or LAST_REWRITE_ERROR:
            # Cette ligne affecte la variable `hint` avec `f" (Détail technique : {LAST_REWRITE_ERROR})" if LAST_REWRITE_ERROR else ""`.
            hint = f" (Détail technique : {LAST_REWRITE_ERROR})" if LAST_REWRITE_ERROR else ""
            # Cette ligne renvoie `{"answer": "Je n'ai pas encore cette information dans ma base. "` au code qui a appelé la fonction.
            return {"answer": "Je n'ai pas encore cette information dans ma base. "
                              # Cette ligne exécute `"Pouvez-vous poser la question autrement, avec d'autres mots ?" + hint, "sources": []}` dans le traitement courant.
                              "Pouvez-vous poser la question autrement, avec d'autres mots ?" + hint, "sources": []}
        # Cette ligne affecte les passages trouvés par la recherche avec `[(0.0, c) for c in overview[:8]]   # vue d'ensemble de l'usine : le modèle explique en général`.
        hits = [(0.0, c) for c in overview[:8]]   # vue d'ensemble de l'usine : le modèle explique en général
    # Cette ligne affecte les extraits documentaires fournis au modèle avec `build_context(hits)`.
    context = build_context(hits)
    # Cette ligne ouvre un bloc dont les erreurs seront traitées dans les clauses except.
    try:
        # Cette ligne affecte le texte en cours de traitement avec `answer_with_llm(q.question, q.history, context)`.
        text = answer_with_llm(q.question, q.history, context)
        # Cette ligne vérifie la condition `UNKNOWN_TAG in text` avant d’exécuter le bloc.
        if UNKNOWN_TAG in text:
            # Cette ligne affecte le texte en cours de traitement avec `text.replace(UNKNOWN_TAG, "").strip()`.
            text = text.replace(UNKNOWN_TAG, "").strip()
            # Cette ligne exécute `log_unanswered(q.question, "information manquante dans les fiches")` dans le traitement courant.
            log_unanswered(q.question, "information manquante dans les fiches")
        # Cette ligne renvoie `{"answer": text, "sources": sources}` au code qui a appelé la fonction.
        return {"answer": text, "sources": sources}
    # Cette ligne intercepte les erreurs correspondant à `Exception as e`.
    except Exception as e:
        # Cette ligne affecte la variable `err_msg` avec `str(e)`.
        err_msg = str(e)
        # Cette ligne vérifie la condition `"10061" in err_msg or "refused" in err_msg.lower() or "target machine actively refused" in err_msg.lower()` avant d’exécuter le bloc.
        if "10061" in err_msg or "refused" in err_msg.lower() or "target machine actively refused" in err_msg.lower():
            # Cette ligne affecte la variable `hint` avec `(`.
            hint = (
                # Cette ligne exécute `"ℹ️ **Le moteur d'intelligence artificielle locale (Ollama) n'est pas encore démarré.**\n\n"` dans le traitement courant.
                "ℹ️ **Le moteur d'intelligence artificielle locale (Ollama) n'est pas encore démarré.**\n\n"
                # Cette ligne exécute `"👉 **Deux solutions simples pour activer le chatbot :**\n"` dans le traitement courant.
                "👉 **Deux solutions simples pour activer le chatbot :**\n"
                # Cette ligne exécute `"1. **Option Cloud (Recommandée & Gratuite) :** Créez une clé API gratuite sur [Google AI Studio](https://aistudio.google.com/) et` dans le traitement courant.
                "1. **Option Cloud (Recommandée & Gratuite) :** Créez une clé API gratuite sur [Google AI Studio](https://aistudio.google.com/) et ajoutez-la dans votre fichier `.env` (`GEMINI_API_KEY=AIzaSy...`)\n"
                # Cette ligne exécute `"2. **Option Locale :** Installez et lancez Ollama avec `ollama serve` et `ollama run qwen2.5:3b`.\n\n"` dans le traitement courant.
                "2. **Option Locale :** Installez et lancez Ollama avec `ollama serve` et `ollama run qwen2.5:3b`.\n\n"
                # Cette ligne exécute `"---\n\n"` dans le traitement courant.
                "---\n\n"
                # Cette ligne exécute `f"**En attendant, voici les informations extraites de nos fiches techniques d'usine :**\n\n{context}"` dans le traitement courant.
                f"**En attendant, voici les informations extraites de nos fiches techniques d'usine :**\n\n{context}"
            # Cette ligne exécute `)` dans le traitement courant.
            )
            # Cette ligne renvoie `{"answer": hint, "sources": sources}` au code qui a appelé la fonction.
            return {"answer": hint, "sources": sources}
        # Cette ligne renvoie `{"answer": f"(Modèle IA indisponible : {e})\n\n**Extraits trouvés dans la base documentaire :**\n\n{context}", "sources": sources}` au code qui a appelé la fonction.
        return {"answer": f"(Modèle IA indisponible : {e})\n\n**Extraits trouvés dans la base documentaire :**\n\n{context}", "sources": sources}
