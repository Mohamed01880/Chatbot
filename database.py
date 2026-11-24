"""Configuration SQLAlchemy et fonctions d'accès à la base PostgreSQL."""

# Cette ligne importe les dépendances nécessaires : import os.
import os
# Cette ligne importe les dépendances nécessaires : from pathlib import Path.
from pathlib import Path
# Cette ligne importe les dépendances nécessaires : from dotenv import load_dotenv.
from dotenv import load_dotenv
# Cette ligne importe les dépendances nécessaires : from sqlalchemy import create_engine, text.
from sqlalchemy import create_engine, text
# Cette ligne importe les dépendances nécessaires : from sqlalchemy.orm import sessionmaker, declarative_base.
from sqlalchemy.orm import sessionmaker, declarative_base

# Charger le fichier .env situé à la racine du projet
# Cette ligne exécute `load_dotenv(Path(__file__).parent / ".env")` dans le traitement courant.
load_dotenv(Path(__file__).parent / ".env")

# Cette ligne affecte la variable `POSTGRES_USER` avec `os.getenv("POSTGRES_USER", "postgres")`.
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
# Cette ligne affecte la variable `POSTGRES_PASSWORD` avec `os.getenv("POSTGRES_PASSWORD", "postgres")`.
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
# Cette ligne affecte la variable `POSTGRES_HOST` avec `os.getenv("POSTGRES_HOST", "localhost")`.
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
# Cette ligne affecte la variable `POSTGRES_PORT` avec `os.getenv("POSTGRES_PORT", "5432")`.
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
# Cette ligne affecte la variable `POSTGRES_DB` avec `os.getenv("POSTGRES_DB", "chatbot")`.
POSTGRES_DB = os.getenv("POSTGRES_DB", "chatbot")

# URL de connexion SQLAlchemy pour PostgreSQL
# Cette ligne affecte la variable `DATABASE_URL` avec `os.getenv(`.
DATABASE_URL = os.getenv(
    # Cette ligne exécute `"DATABASE_URL",` dans le traitement courant.
    "DATABASE_URL",
    # Cette ligne exécute `f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"` dans le traitement courant.
    f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
# Cette ligne exécute `)` dans le traitement courant.
)

# Cette ligne affecte le moteur SQLAlchemy avec `create_engine(`.
engine = create_engine(
    # Cette ligne exécute `DATABASE_URL,` dans le traitement courant.
    DATABASE_URL,
    # Cette ligne affecte la variable `echo` avec `False,`.
    echo=False,
    # Cette ligne affecte la variable `future` avec `True,`.
    future=True,
    # Cette ligne affecte la variable `pool_pre_ping` avec `True,`.
    pool_pre_ping=True,
    # Cette ligne affecte la variable `pool_recycle` avec `1800,`.
    pool_recycle=1800,
# Cette ligne exécute `)` dans le traitement courant.
)
# Cette ligne affecte la variable `SessionLocal` avec `sessionmaker(autocommit=False, autoflush=False, bind=engine)`.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cette ligne affecte la classe de base des modèles SQLAlchemy avec `declarative_base()`.
Base = declarative_base()


# Cette définition sert à Générateur de session pour l'injection de dépendances FastAPI .
def get_db():
    # Cette ligne exécute `"""Générateur de session pour l'injection de dépendances FastAPI."""` dans le traitement courant.
    """Générateur de session pour l'injection de dépendances FastAPI."""
    # commentaire  # Cette chaîne documente le module, la classe ou la fonction.
    db = SessionLocal()
    # Cette ligne ouvre un bloc dont les erreurs seront traitées dans les clauses except.
    try:
        # Cette ligne exécute `yield db` dans le traitement courant.
        yield db
    # Cette ligne démarre le bloc `finally`.
    finally:
        # Cette ligne exécute `db.close()` dans le traitement courant.
        db.close()


# Cette définition sert à Vérifie si la connexion à PostgreSQL est active .
def test_connection():
    # Cette ligne exécute `"""Vérifie si la connexion à PostgreSQL est active."""` dans le traitement courant.
    """Vérifie si la connexion à PostgreSQL est active."""
    # commentaire  # Cette chaîne documente le module, la classe ou la fonction.
    try:
        # Cette ligne ouvre la ressource `engine.connect() as conn` et garantit sa fermeture à la fin du bloc.
        with engine.connect() as conn:
            # Cette ligne exécute `conn.execute(text("SELECT 1"))` dans le traitement courant.
            conn.execute(text("SELECT 1"))
        # Cette ligne renvoie `True, "Connecté à PostgreSQL"` au code qui a appelé la fonction.
        return True, "Connecté à PostgreSQL"
    # Cette ligne intercepte les erreurs correspondant à `UnicodeDecodeError`.
    except UnicodeDecodeError:
        # Cette ligne renvoie `False, "Échec d'authentification : mot de passe PostgreSQL incorrect (éditez le fichier .env)."` au code qui a appelé la fonction.
        return False, "Échec d'authentification : mot de passe PostgreSQL incorrect (éditez le fichier .env)."
    # Cette ligne intercepte les erreurs correspondant à `Exception as e`.
    except Exception as e:
        # Cette ligne affecte la variable `err` avec `str(e)`.
        err = str(e)
        # Cette ligne vérifie la condition `"authentification" in err.lower() or "password" in err.lower() or "fe_sendauth" in err.lower()` avant d’exécuter le bloc.
        if "authentification" in err.lower() or "password" in err.lower() or "fe_sendauth" in err.lower():
            # Cette ligne renvoie `False, "Échec d'authentification : mot de passe PostgreSQL incorrect (éditez le fichier .env)."` au code qui a appelé la fonction.
            return False, "Échec d'authentification : mot de passe PostgreSQL incorrect (éditez le fichier .env)."
        # Cette ligne renvoie `False, err` au code qui a appelé la fonction.
        return False, err
