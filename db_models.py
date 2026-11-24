"""Définit les tables PostgreSQL des comptes et de l'historique des questions."""

# Cette ligne importe les dépendances nécessaires : from sqlalchemy import Column, Integer, String, Text, DateTime, func.
from sqlalchemy import Column, Integer, String, Text, DateTime, func
# Cette ligne importe les dépendances nécessaires : from database import Base.
from database import Base


# Cette définition sert à Table des utilisateurs (opérateurs / clients) pour l'authentification .
class User(Base):
    # Cette ligne exécute `"""Table des utilisateurs (opérateurs / clients) pour l'authentification."""` dans le traitement courant.
    """Table des utilisateurs (opérateurs / clients) pour l'authentification."""
    # commentaire  # Cette chaîne documente le module, la classe ou la fonction.
    __tablename__ = "users"

    # Cette ligne affecte la variable `id` avec `Column(Integer, primary_key=True, index=True, autoincrement=True)`.
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    # Cette ligne affecte la variable `name` avec `Column(String(120), nullable=False)`.
    name = Column(String(120), nullable=False)
    # Cette ligne affecte le matricule de l’utilisateur avec `Column(String(60), unique=True, index=True, nullable=False)`.
    matricule = Column(String(60), unique=True, index=True, nullable=False)
    # Cette ligne affecte la variable `email` avec `Column(String(120), unique=True, index=True, nullable=True)`.
    email = Column(String(120), unique=True, index=True, nullable=True)
    # Cette ligne laisse volontairement ce bloc vide pour le moment.
    password_hash = Column(String(256), nullable=False)
    # Cette ligne affecte la variable `role` avec `Column(String(100), default="Nouvel Arrivant (Tronc Commun)", nullable=False)`.
    role = Column(String(100), default="Nouvel Arrivant (Tronc Commun)", nullable=False)
    # Cette ligne affecte la variable `lang` avec `Column(String(10), default="fr", nullable=False)`.
    lang = Column(String(10), default="fr", nullable=False)
    # Cette ligne affecte la variable `created_at` avec `Column(DateTime(timezone=True), server_default=func.now(), nullable=False)`.
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Cette définition sert à Convertit le compte en dictionnaire sans inclure le hash du mot de passe .
    def to_dict(self):
        # Cette ligne exécute `"""Convertit le compte en dictionnaire sans inclure le hash du mot de passe."""` dans le traitement courant.
        """Convertit le compte en dictionnaire sans inclure le hash du mot de passe."""
        # commentaire  # Cette chaîne documente le module, la classe ou la fonction.
        return {
            # Cette ligne exécute `"id": self.id,` dans le traitement courant.
            "id": self.id,
            # Cette ligne exécute `"name": self.name,` dans le traitement courant.
            "name": self.name,
            # Cette ligne exécute `"matricule": self.matricule,` dans le traitement courant.
            "matricule": self.matricule,
            # Cette ligne exécute `"email": self.email,` dans le traitement courant.
            "email": self.email,
            # Cette ligne exécute `"role": self.role,` dans le traitement courant.
            "role": self.role,
            # Cette ligne exécute `"lang": self.lang,` dans le traitement courant.
            "lang": self.lang,
            # Cette ligne exécute `"created_at": self.created_at.isoformat() if self.created_at else None,` dans le traitement courant.
            "created_at": self.created_at.isoformat() if self.created_at else None,
        # Cette ligne exécute `}` dans le traitement courant.
        }


# Cette définition sert à Enregistre chaque échange question/réponse du chatbot .
class QuestionLog(Base):
    # Cette ligne exécute `"""Enregistre chaque échange question/réponse du chatbot."""` dans le traitement courant.
    """Enregistre chaque échange question/réponse du chatbot."""
    # commentaire  # Cette chaîne documente le module, la classe ou la fonction.
    __tablename__ = "question_log"

    # Cette ligne affecte la variable `id` avec `Column(Integer, primary_key=True, index=True, autoincrement=True)`.
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    # Cette ligne affecte la variable `user_matricule` avec `Column(String(60), nullable=True)`.
    user_matricule = Column(String(60), nullable=True)
    # Cette ligne affecte la question posée par l’utilisateur avec `Column(Text, nullable=False)`.
    question = Column(Text, nullable=False)
    # Cette ligne affecte la réponse du chatbot avec `Column(Text, nullable=False)`.
    answer = Column(Text, nullable=False)
    # Cette ligne affecte la variable `created_at` avec `Column(DateTime(timezone=True), server_default=func.now(), nullable=False)`.
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
