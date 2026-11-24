"""Script d'initialisation de la base PostgreSQL :
1. Vérifie ou crée la base 'chatbot'
2. Crée les tables nécessaires (users, question_log)
3. Insère les comptes opérateurs démo avec mot de passe par défaut
"""
# Cette ligne importe les dépendances nécessaires : import sys.
import sys
# Cette ligne importe les dépendances nécessaires : from sqlalchemy import create_engine, text.
from sqlalchemy import create_engine, text
# Cette ligne importe les dépendances nécessaires : from database import engine, Base, SessionLocal, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB.
from database import engine, Base, SessionLocal, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB
# Cette ligne importe les dépendances nécessaires : import db_models.
import db_models
# Cette ligne importe les dépendances nécessaires : from auth import hash_password.
from auth import hash_password


# Cette définition sert à Se connecte à la base de maintenance postgres et crée la base chatbot si nécessaire .
def ensure_database_exists():
    """Se connecte à la base de maintenance postgres et crée la base chatbot si nécessaire."""
    # Cette ligne affecte la variable `maintenance_url` avec `f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/postgres"`.
    maintenance_url = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/postgres"
    # Cette ligne ouvre un bloc dont les erreurs seront traitées dans les clauses except.
    try:
        # Cette ligne affecte la variable `m_engine` avec `create_engine(maintenance_url, isolation_level="AUTOCOMMIT")`.
        m_engine = create_engine(maintenance_url, isolation_level="AUTOCOMMIT")
        # Cette ligne ouvre la ressource `m_engine.connect() as conn` et garantit sa fermeture à la fin du bloc.
        with m_engine.connect() as conn:
            # Cette ligne affecte le résultat du traitement avec `conn.execute(`.
            result = conn.execute(
                # Cette ligne exécute `text("SELECT 1 FROM pg_database WHERE datname = :dbname"),` dans le traitement courant.
                text("SELECT 1 FROM pg_database WHERE datname = :dbname"),
                # Cette ligne exécute `{"dbname": POSTGRES_DB}` dans le traitement courant.
                {"dbname": POSTGRES_DB}
            # Cette ligne exécute `)` dans le traitement courant.
            )
            # Cette ligne affecte la variable `exists` avec `result.scalar() is not None`.
            exists = result.scalar() is not None
            # Cette ligne vérifie la condition `not exists` avant d’exécuter le bloc.
            if not exists:
                # Cette ligne écrit une information de suivi : `print(f"[PostgreSQL] Création de la base '{POSTGRES_DB}'...")`.
                print(f"[PostgreSQL] Création de la base '{POSTGRES_DB}'...")
                # Cette ligne exécute `conn.execute(text(f'CREATE DATABASE "{POSTGRES_DB}"'))` dans le traitement courant.
                conn.execute(text(f'CREATE DATABASE "{POSTGRES_DB}"'))
                # Cette ligne écrit une information de suivi : `print(f"[PostgreSQL] Base '{POSTGRES_DB}' créée avec succès !")`.
                print(f"[PostgreSQL] Base '{POSTGRES_DB}' créée avec succès !")
            # Cette ligne démarre le cas exécuté lorsque les conditions précédentes ne sont pas satisfaites.
            else:
                # Cette ligne écrit une information de suivi : `print(f"[PostgreSQL] La base '{POSTGRES_DB}' existe déjà.")`.
                print(f"[PostgreSQL] La base '{POSTGRES_DB}' existe déjà.")
    # Cette ligne intercepte les erreurs correspondant à `UnicodeDecodeError`.
    except UnicodeDecodeError:
        # Cette ligne écrit une information de suivi : `print(f"[PostgreSQL] Authentification échouée : mot de passe incorrect pour '{POSTGRES_USER}'. Vérifiez le mot`.
        print(f"[PostgreSQL] Authentification échouée : mot de passe incorrect pour '{POSTGRES_USER}'. Vérifiez le mot de passe dans le fichier .env.")
        # Cette ligne exécute `raise` dans le traitement courant.
        raise
    # Cette ligne intercepte les erreurs correspondant à `Exception as e`.
    except Exception as e:
        # Cette ligne écrit une information de suivi : `print(f"[PostgreSQL] Note création base : {e}")`.
        print(f"[PostgreSQL] Note création base : {e}")


# Cette définition sert à Crée les profils d'opérateurs initiaux dans PostgreSQL si absents .
def seed_demo_users():
    # Cette ligne exécute `"""Crée les profils d'opérateurs initiaux dans PostgreSQL si absents."""` dans le traitement courant.
    """Crée les profils d'opérateurs initiaux dans PostgreSQL si absents."""
    # commentaire  # Cette chaîne documente le module, la classe ou la fonction.
    demo_accounts = [
        # Cette ligne exécute `{` dans le traitement courant.
        {
            # Cette ligne exécute `"name": "Amine El Mansouri",` dans le traitement courant.
            "name": "Amine El Mansouri",
            # Cette ligne exécute `"matricule": "OP-2026-104",` dans le traitement courant.
            "matricule": "OP-2026-104",
            # Cette ligne exécute `"email": "amine.elmansouri@auto-harness.local",` dans le traitement courant.
            "email": "amine.elmansouri@auto-harness.local",
            # Cette ligne exécute `"password": "pass123",` dans le traitement courant.
            "password": "pass123",
            # Cette ligne exécute `"role": "P1 - Coupe & Dénudage",` dans le traitement courant.
            "role": "P1 - Coupe & Dénudage",
            # Cette ligne exécute `"lang": "fr",` dans le traitement courant.
            "lang": "fr",
        # Cette ligne exécute `},` dans le traitement courant.
        },
        # Cette ligne exécute `{` dans le traitement courant.
        {
            # Cette ligne exécute `"name": "Fatima Zahra Bennani",` dans le traitement courant.
            "name": "Fatima Zahra Bennani",
            # Cette ligne exécute `"matricule": "OP-2026-218",` dans le traitement courant.
            "matricule": "OP-2026-218",
            # Cette ligne exécute `"email": "fatima.bennani@auto-harness.local",` dans le traitement courant.
            "email": "fatima.bennani@auto-harness.local",
            # Cette ligne exécute `"password": "pass123",` dans le traitement courant.
            "password": "pass123",
            # Cette ligne exécute `"role": "P2 - Préparation & Sertissage",` dans le traitement courant.
            "role": "P2 - Préparation & Sertissage",
            # Cette ligne exécute `"lang": "fr",` dans le traitement courant.
            "lang": "fr",
        # Cette ligne exécute `},` dans le traitement courant.
        },
        # Cette ligne exécute `{` dans le traitement courant.
        {
            # Cette ligne exécute `"name": "Youssef Alami",` dans le traitement courant.
            "name": "Youssef Alami",
            # Cette ligne exécute `"matricule": "OP-2026-309",` dans le traitement courant.
            "matricule": "OP-2026-309",
            # Cette ligne exécute `"email": "youssef.alami@auto-harness.local",` dans le traitement courant.
            "email": "youssef.alami@auto-harness.local",
            # Cette ligne exécute `"password": "pass123",` dans le traitement courant.
            "password": "pass123",
            # Cette ligne exécute `"role": "P3 - Assemblage & Câblage",` dans le traitement courant.
            "role": "P3 - Assemblage & Câblage",
            # Cette ligne exécute `"lang": "fr",` dans le traitement courant.
            "lang": "fr",
        # Cette ligne exécute `},` dans le traitement courant.
        },
        # Cette ligne exécute `{` dans le traitement courant.
        {
            # Cette ligne exécute `"name": "Sara Chaoui",` dans le traitement courant.
            "name": "Sara Chaoui",
            # Cette ligne exécute `"matricule": "OP-2026-015",` dans le traitement courant.
            "matricule": "OP-2026-015",
            # Cette ligne exécute `"email": "sara.chaoui@auto-harness.local",` dans le traitement courant.
            "email": "sara.chaoui@auto-harness.local",
            # Cette ligne exécute `"password": "pass123",` dans le traitement courant.
            "password": "pass123",
            # Cette ligne exécute `"role": "Nouvel Arrivant (Tronc Commun)",` dans le traitement courant.
            "role": "Nouvel Arrivant (Tronc Commun)",
            # Cette ligne exécute `"lang": "fr",` dans le traitement courant.
            "lang": "fr",
        # Cette ligne exécute `},` dans le traitement courant.
        },
    # Cette ligne exécute `]` dans le traitement courant.
    ]

    # Cette ligne ouvre un bloc dont les erreurs seront traitées dans les clauses except.
    try:
        # Cette ligne ouvre la ressource `SessionLocal() as db` et garantit sa fermeture à la fin du bloc.
        with SessionLocal() as db:
            # Cette ligne parcourt `acc in demo_accounts` pour traiter chaque élément.
            for acc in demo_accounts:
                # Cette ligne affecte la variable `existing` avec `db.query(db_models.User).filter_by(matricule=acc["matricule"]).first()`.
                existing = db.query(db_models.User).filter_by(matricule=acc["matricule"]).first()
                # Cette ligne vérifie la condition `not existing` avant d’exécuter le bloc.
                if not existing:
                    # Cette ligne affecte l’utilisateur enregistré avec `db_models.User(`.
                    user = db_models.User(
                        # Cette ligne affecte la variable `name` avec `acc["name"],`.
                        name=acc["name"],
                        # Cette ligne affecte le matricule de l’utilisateur avec `acc["matricule"],`.
                        matricule=acc["matricule"],
                        # Cette ligne affecte la variable `email` avec `acc["email"],`.
                        email=acc["email"],
                        # Cette ligne laisse volontairement ce bloc vide pour le moment.
                        password_hash=hash_password(acc["password"]),
                        # Cette ligne affecte la variable `role` avec `acc["role"],`.
                        role=acc["role"],
                        # Cette ligne affecte la variable `lang` avec `acc["lang"],`.
                        lang=acc["lang"],
                    # Cette ligne exécute `)` dans le traitement courant.
                    )
                    # Cette ligne exécute `db.add(user)` dans le traitement courant.
                    db.add(user)
                    # Cette ligne écrit une information de suivi : `print(f"[PostgreSQL] Compte démo initialisé : {acc['name']} ({acc['matricule']})")`.
                    print(f"[PostgreSQL] Compte démo initialisé : {acc['name']} ({acc['matricule']})")
            # Cette ligne exécute `db.commit()` dans le traitement courant.
            db.commit()
    # Cette ligne intercepte les erreurs correspondant à `Exception as e`.
    except Exception as e:
        # Cette ligne écrit une information de suivi : `print(f"[PostgreSQL] Note peuplement comptes démo : {e}")`.
        print(f"[PostgreSQL] Note peuplement comptes démo : {e}")


# Cette ligne vérifie la condition `__name__ == "__main__"` avant d’exécuter le bloc.
if __name__ == "__main__":
    # Cette ligne écrit une information de suivi : `print("=== INITIALISATION BASE DE DONNÉES POSTGRESQL ===")`.
    print("=== INITIALISATION BASE DE DONNÉES POSTGRESQL ===")
    # Cette ligne ouvre un bloc dont les erreurs seront traitées dans les clauses except.
    try:
        # Cette ligne exécute `ensure_database_exists()` dans le traitement courant.
        ensure_database_exists()
        # Cette ligne écrit une information de suivi : `print("[PostgreSQL] Synchronisation des tables (users, question_log)...")`.
        print("[PostgreSQL] Synchronisation des tables (users, question_log)...")
        # Cette ligne exécute `Base.metadata.create_all(bind=engine)` dans le traitement courant.
        Base.metadata.create_all(bind=engine)
        # Cette ligne écrit une information de suivi : `print("[PostgreSQL] Tables créées avec succès !")`.
        print("[PostgreSQL] Tables créées avec succès !")
        # Cette ligne exécute `seed_demo_users()` dans le traitement courant.
        seed_demo_users()
        # Cette ligne écrit une information de suivi : `print("[PostgreSQL] Initialisation terminée avec succès !")`.
        print("[PostgreSQL] Initialisation terminée avec succès !")
    # Cette ligne intercepte les erreurs correspondant à `Exception as e`.
    except Exception as e:
        # Cette ligne écrit une information de suivi : `print(f"\n[!] Impossible de se connecter à PostgreSQL avec les identifiants actuels.")`.
        print(f"\n[!] Impossible de se connecter à PostgreSQL avec les identifiants actuels.")
        # Cette ligne écrit une information de suivi : `print(f"    Veuillez renseigner votre mot de passe PostgreSQL dans le fichier .env (POSTGRES_PASSWORD=...)")`.
        print(f"    Veuillez renseigner votre mot de passe PostgreSQL dans le fichier .env (POSTGRES_PASSWORD=...)")
