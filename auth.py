"""Fonctions de sécurité utilisées pour créer et vérifier les mots de passe."""
# Cette ligne importe les dépendances nécessaires : import hashlib.
import hashlib
# Cette ligne importe les dépendances nécessaires : import secrets.
import secrets
# Cette ligne importe les dépendances nécessaires : from typing import Optional.
from typing import Optional


# Cette définition sert à Hache le mot de passe avec PBKDF2-HMAC-SHA256 et un sel aléatoire .
def hash_password(password: str) -> str:
    # Cette ligne exécute `"""Hache le mot de passe avec PBKDF2-HMAC-SHA256 et un sel aléatoire."""` dans le traitement courant.
    """Hache le mot de passe avec PBKDF2-HMAC-SHA256 et un sel aléatoire."""
    # commentaire  # Cette chaîne documente le module, la classe ou la fonction.
    if not password:
        # Cette ligne signale l’erreur `ValueError("Le mot de passe ne peut pas être vide")` et interrompt le traitement courant.
        raise ValueError("Le mot de passe ne peut pas être vide")
    # Cette ligne affecte la variable `salt` avec `secrets.token_hex(16)`.
    salt = secrets.token_hex(16)
    # Cette ligne affecte la variable `key` avec `hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 100_000)`.
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 100_000)
    # Cette ligne renvoie `f"{salt}${key.hex()}"` au code qui a appelé la fonction.
    return f"{salt}${key.hex()}"


# Cette définition sert à Vérifie si le mot de passe fourni correspond au hash stocké .
def verify_password(stored_password_hash: str, provided_password: str) -> bool:
    # Cette ligne exécute `"""Vérifie si le mot de passe fourni correspond au hash stocké."""` dans le traitement courant.
    """Vérifie si le mot de passe fourni correspond au hash stocké."""
    # commentaire  # Cette chaîne documente le module, la classe ou la fonction.
    if not stored_password_hash or not provided_password:
        # Cette ligne renvoie `False` au code qui a appelé la fonction.
        return False
    # Cette ligne ouvre un bloc dont les erreurs seront traitées dans les clauses except.
    try:
        # Cette ligne exécute `salt, key_hex = stored_password_hash.split("$", 1)` dans le traitement courant.
        salt, key_hex = stored_password_hash.split("$", 1)
        # Cette ligne affecte la variable `test_key` avec `hashlib.pbkdf2_hmac("sha256", provided_password.encode("utf-8"), salt.encode("utf-8"), 100_000)`.
        test_key = hashlib.pbkdf2_hmac("sha256", provided_password.encode("utf-8"), salt.encode("utf-8"), 100_000)
        # Cette ligne renvoie `secrets.compare_digest(key_hex, test_key.hex())` au code qui a appelé la fonction.
        return secrets.compare_digest(key_hex, test_key.hex())
    # Cette ligne intercepte les erreurs correspondant à `Exception`.
    except Exception:
        # Cette ligne renvoie `False` au code qui a appelé la fonction.
        return False
