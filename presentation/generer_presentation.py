"""Construit le diaporama de présentation du chatbot et de son architecture RAG."""

# Cette ligne importe les dépendances nécessaires : from pathlib import Path.
from pathlib import Path
# Cette ligne importe les dépendances nécessaires : from pptx import Presentation.
from pptx import Presentation
# Cette ligne importe les dépendances nécessaires : from pptx.util import Inches, Pt.
from pptx.util import Inches, Pt
# Cette ligne importe les dépendances nécessaires : from pptx.dml.color import RGBColor.
from pptx.dml.color import RGBColor
# Cette ligne importe les dépendances nécessaires : from pptx.enum.shapes import MSO_SHAPE.
from pptx.enum.shapes import MSO_SHAPE

# Cette ligne affecte la variable `OUT` avec `Path(__file__).parent`.
OUT = Path(__file__).parent
# Titre, idée principale, cartes (titre, texte), notes orales, durée en secondes.
# Cette ligne affecte la variable `slides` avec `[`.
slides = [
# Cette ligne exécute `('Un assistant pour mieux\naccueillir les nouveaux employés',` dans le traitement courant.
('Un assistant pour mieux\naccueillir les nouveaux employés',
 # Cette ligne exécute `'Chatbot d’intégration • Industrie des faisceaux de câbles',` dans le traitement courant.
 'Chatbot d’intégration • Industrie des faisceaux de câbles',
 # Cette ligne exécute `[('COMPRENDRE', 'Expliquer les métiers avec des mots simples.'), ('RETROUVER', 'Chercher dans une base documentaire dédiée.'), ('A` dans le traitement courant.
 [('COMPRENDRE', 'Expliquer les métiers avec des mots simples.'), ('RETROUVER', 'Chercher dans une base documentaire dédiée.'), ('ACCOMPAGNER', 'Répondre aux questions du nouvel arrivant.')],
 # Cette ligne exécute `'Bonjour Mesdames et Messieurs les membres du jury. Je vous présente mon projet de chatbot pour accompagner les nouveaux employés ` dans le traitement courant.
 'Bonjour Mesdames et Messieurs les membres du jury. Je vous présente mon projet de chatbot pour accompagner les nouveaux employés dans une usine de faisceaux de câbles. Un faisceau est un ensemble de fils qui relie les équipements électriques d’un véhicule. Mon objectif est de rendre les premières explications plus accessibles. Le point central du projet est le RAG : une méthode qui recherche des informations dans des documents avant de rédiger une réponse. Je vais présenter le besoin, la solution, son fonctionnement et les résultats obtenus.', 45),
# Cette ligne exécute `('Le besoin : rendre les premiers jours plus clairs',` dans le traitement courant.
('Le besoin : rendre les premiers jours plus clairs',
 # Cette ligne exécute `'Un nouvel employé doit découvrir un environnement technique.',` dans le traitement courant.
 'Un nouvel employé doit découvrir un environnement technique.',
 # Cette ligne exécute `[('VOCABULAIRE', 'Coupe, dénudage, sertissage : des mots à comprendre.'), ('REPÈRES', 'Identifier les zones, leurs rôles et leurs ` dans le traitement courant.
 [('VOCABULAIRE', 'Coupe, dénudage, sertissage : des mots à comprendre.'), ('REPÈRES', 'Identifier les zones, leurs rôles et leurs liens.'), ('ACCÈS', 'Poser une question simplement, au moment du besoin.')],
 # Cette ligne exécute `'À son arrivée, un employé découvre de nouveaux mots, de nouvelles zones et des règles de travail. Par exemple, il peut ne pas con` dans le traitement courant.
 'À son arrivée, un employé découvre de nouveaux mots, de nouvelles zones et des règles de travail. Par exemple, il peut ne pas connaître la différence entre couper un fil et sertir une cosse. L’idée est de lui proposer un point d’accès simple aux explications. Les bénéfices recherchés sont une meilleure compréhension et un accès plus direct à l’information. Je parle ici d’objectifs : je n’ai pas encore mesuré une réduction du temps de formation sur le terrain.', 40),
# Cette ligne exécute `('La solution : un dialogue appuyé sur des documents',` dans le traitement courant.
('La solution : un dialogue appuyé sur des documents',
 # Cette ligne exécute `'Une question naturelle → une explication simple → des sources consultables.',` dans le traitement courant.
 'Une question naturelle → une explication simple → des sources consultables.',
 # Cette ligne exécute `[('DIALOGUER', 'Interface de chat et historique de conversation.'), ('EXPLIQUER', 'Réponses courtes, vocabulaire accessible, exemp` dans le traitement courant.
 [('DIALOGUER', 'Interface de chat et historique de conversation.'), ('EXPLIQUER', 'Réponses courtes, vocabulaire accessible, exemples.'), ('CONSULTER', 'Affichage optionnel de la fiche et de la section utilisées.')],
 # Cette ligne exécute `'L’utilisateur pose sa question dans une interface de chat. Le système recherche des extraits utiles, puis le modèle les utilise p` dans le traitement courant.
 'L’utilisateur pose sa question dans une interface de chat. Le système recherche des extraits utiles, puis le modèle les utilise pour expliquer le sujet dans une langue simple. L’utilisateur peut afficher les fiches et les sections sélectionnées. Le projet comprend aussi des comptes et un enregistrement des échanges dans PostgreSQL, ainsi que des fonctions vocales selon le navigateur. Pour cette présentation, je me concentre sur la contribution principale : la chaîne de recherche documentaire et son intégration dans le dialogue.', 45),
# Cette ligne exécute `('Le RAG, expliqué simplement',` dans le traitement courant.
('Le RAG, expliqué simplement',
 # Cette ligne exécute `'RAG = génération de réponse enrichie par une recherche documentaire.',` dans le traitement courant.
 'RAG = génération de réponse enrichie par une recherche documentaire.',
 # Cette ligne exécute `[('1 · RECHERCHER', 'Retrouver les passages utiles dans les fiches.'), ('2 · FOURNIR', 'Donner ces passages au modèle avec la ques` dans le traitement courant.
 [('1 · RECHERCHER', 'Retrouver les passages utiles dans les fiches.'), ('2 · FOURNIR', 'Donner ces passages au modèle avec la question.'), ('3 · EXPLIQUER', 'Rédiger une réponse à partir du contexte fourni.')],
 # Cette ligne exécute `'On peut imaginer un assistant qui ouvre un dossier avant de répondre. La recherche trouve les bonnes pages. Le modèle de langage ` dans le traitement courant.
 'On peut imaginer un assistant qui ouvre un dossier avant de répondre. La recherche trouve les bonnes pages. Le modèle de langage transforme ensuite ces informations en une explication compréhensible. C’est le principe du RAG. Dans ce projet, je n’entraîne pas un nouveau modèle sur les fiches : je les lui fournis au moment de la question. Cela facilite la mise à jour des connaissances. Le RAG réduit le risque de réponse sans fondement, mais il ne garantit pas que toutes les réponses seront correctes.', 55),
# Cette ligne exécute `('La base documentaire : petite, structurée, traçable',` dans le traitement courant.
('La base documentaire : petite, structurée, traçable',
 # Cette ligne exécute `'9 fiches • 89 extraits chargés dans la version actuelle',` dans le traitement courant.
 '9 fiches • 89 extraits chargés dans la version actuelle',
 # Cette ligne exécute `[('LE PÉRIMÈTRE', 'Magasins, coupe, préparation, assemblage, contrôle, sécurité, intégration et glossaire.'), ('LE DÉCOUPAGE', 'Un` dans le traitement courant.
 [('LE PÉRIMÈTRE', 'Magasins, coupe, préparation, assemblage, contrôle, sécurité, intégration et glossaire.'), ('LE DÉCOUPAGE', 'Une section devient un extrait, avec son titre et sa fiche d’origine.'), ('LA PORTÉE', 'Guides pédagogiques généraux ; validation par le site nécessaire.')],
 # Cette ligne exécute `'La base actuelle contient neuf fiches, découpées en quatre-vingt-neuf extraits. Le découpage suit les sections : par exemple le r` dans le traitement courant.
 'La base actuelle contient neuf fiches, découpées en quatre-vingt-neuf extraits. Le découpage suit les sections : par exemple le rôle d’une zone ou son contrôle qualité. Chaque extrait conserve sa provenance. Ce choix permet de retrouver une information précise sans transmettre tout le corpus au modèle. Les fiches sont des synthèses pédagogiques issues notamment de ressources publiques. Elles ne constituent pas des procédures internes approuvées. Cette distinction est essentielle avant une utilisation industrielle.', 50),
# Cette ligne exécute `('Le cœur technique : une chaîne RAG hybride',` dans le traitement courant.
('Le cœur technique : une chaîne RAG hybride',
 # Cette ligne exécute `'Deux recherches complémentaires, puis une sélection plus fine.',` dans le traitement courant.
 'Deux recherches complémentaires, puis une sélection plus fine.',
 # Cette ligne exécute `[('RECHERCHER', 'BM25 : les mots\nEmbeddings : le sens'), ('CLASSER', 'Fusion RRF\nPuis reranker Gemini'), ('RÉPONDRE', 'Jusqu’à 6` dans le traitement courant.
 [('RECHERCHER', 'BM25 : les mots\nEmbeddings : le sens'), ('CLASSER', 'Fusion RRF\nPuis reranker Gemini'), ('RÉPONDRE', 'Jusqu’à 6 extraits\nPuis modèle de réponse')],
 # Cette ligne exécute `'Voici le parcours d’une question. Le système peut d’abord la traduire ou la reformuler si nécessaire. Deux méthodes recherchent e` dans le traitement courant.
 'Voici le parcours d’une question. Le système peut d’abord la traduire ou la reformuler si nécessaire. Deux méthodes recherchent ensuite les extraits : BM25 et les embeddings. La fusion RRF combine leurs classements. Un reranker Gemini peut relire jusqu’à vingt candidats avec les réglages par défaut, puis les reclasser. Enfin, les six premiers extraits disponibles sont envoyés au modèle de réponse avec la question et l’historique. Chaque étape a un rôle différent : trouver, choisir, puis expliquer.', 65),
# Cette ligne exécute `('Pourquoi combiner les mots et le sens ?',` dans le traitement courant.
('Pourquoi combiner les mots et le sens ?',
 # Cette ligne exécute `'Une même intention peut être exprimée de plusieurs façons.',` dans le traitement courant.
 'Une même intention peut être exprimée de plusieurs façons.',
 # Cette ligne exécute `[('BM25 · LES MOTS', 'Utile pour les termes précis : « zone P1 », « coupe », « sertissage ».'), ('EMBEDDINGS · LE SENS', 'Comparer` dans le traitement courant.
 [('BM25 · LES MOTS', 'Utile pour les termes précis : « zone P1 », « coupe », « sertissage ».'), ('EMBEDDINGS · LE SENS', 'Comparer des représentations numériques pour retrouver des formulations proches.'), ('RRF · LA FUSION', 'Combiner les positions dans les deux listes, sans comparer leurs scores bruts.')],
 # Cette ligne exécute `'BM25 repère les mots importants de la question dans les documents. Il est utile pour les termes métier précis. Les embeddings rep` dans le traitement courant.
 'BM25 repère les mots importants de la question dans les documents. Il est utile pour les termes métier précis. Les embeddings représentent les textes par des vecteurs, c’est-à-dire des listes de nombres. Leur proximité aide à repérer des passages proches par le sens. Dans ce projet, ils sont calculés localement avec Ollama et embeddinggemma. Comme les deux recherches ont des scores différents, je combine leurs rangs avec RRF. C’est une complémentarité technique ; le gain réel doit être mesuré sur des questions représentatives.', 60),
# Cette ligne exécute `('Le reranker : relire avant de choisir',` dans le traitement courant.
('Le reranker : relire avant de choisir',
 # Cette ligne exécute `'L’amélioration vise la pertinence des extraits transmis au modèle.',` dans le traitement courant.
 'L’amélioration vise la pertinence des extraits transmis au modèle.',
 # Cette ligne exécute `[('ENTRÉE', 'La question et jusqu’à 20 extraits candidats, par défaut.'), ('RECLASSEMENT', 'Gemini renvoie les identifiants dans u` dans le traitement courant.
 [('ENTRÉE', 'La question et jusqu’à 20 extraits candidats, par défaut.'), ('RECLASSEMENT', 'Gemini renvoie les identifiants dans un nouvel ordre de pertinence.'), ('CONTRÔLE', 'Doublons ou identifiants invalides : retour au classement initial.')],
 # Cette ligne exécute `'La première recherche peut remonter plusieurs extraits proches du sujet. Le reranker les relit avec la question pour faire passer` dans le traitement courant.
 'La première recherche peut remonter plusieurs extraits proches du sujet. Le reranker les relit avec la question pour faire passer les plus utiles en premier. Ici, il s’agit d’un modèle génératif Gemini utilisé pour reclasser, et non d’un cross-encoder local. Sa sortie est contrôlée : chaque candidat doit apparaître exactement une fois. Il ne peut donc pas ajouter un nouveau document. Cette étape ajoute un appel réseau, de la latence et une consommation de quota. Son intérêt doit être comparé à ce coût.', 60),
# Cette ligne exécute `('Exemple : reconnaître la zone de coupe',` dans le traitement courant.
('Exemple : reconnaître la zone de coupe',
 # Cette ligne exécute `'« Où prépare-t-on les fils à la bonne longueur avant de les assembler ? »',` dans le traitement courant.
 '« Où prépare-t-on les fils à la bonne longueur avant de les assembler ? »',
 # Cette ligne exécute `[('INTENTION', 'L’utilisateur décrit une opération sans citer « P1 ».'), ('DOCUMENT CIBLE', 'Zone de coupe P1\nSection : « À quoi ` dans le traitement courant.
 [('INTENTION', 'L’utilisateur décrit une opération sans citer « P1 ».'), ('DOCUMENT CIBLE', 'Zone de coupe P1\nSection : « À quoi sert cette zone ».'), ('EXPLICATION', '« La zone P1 coupe les fils à la longueur demandée avant les étapes suivantes. »')],
 # Cette ligne exécute `'Cet exemple montre ce que je cherche à obtenir. L’utilisateur ne cite pas le nom de la zone ; il décrit sa fonction. Le document ` dans le traitement courant.
 'Cet exemple montre ce que je cherche à obtenir. L’utilisateur ne cite pas le nom de la zone ; il décrit sa fonction. Le document cible explique justement que P1 coupe les fils à la longueur demandée. La phrase affichée ici est une illustration pédagogique, pas une capture d’une réponse générée aujourd’hui. Une vérification antérieure documentée dans le projet a placé ce passage en premier avec le reranker. Cela valide un exemple précis, sans démontrer un gain général sur toutes les questions.', 50),
# Cette ligne exécute `('Une architecture avec des rôles séparés',` dans le traitement courant.
('Une architecture avec des rôles séparés',
 # Cette ligne exécute `'Interface web → API FastAPI → recherche documentaire → modèle de réponse',` dans le traitement courant.
 'Interface web → API FastAPI → recherche documentaire → modèle de réponse',
 # Cette ligne exécute `[('INTERFACE', 'HTML, CSS, JavaScript\nChat, langues, sources et voix selon le navigateur.'), ('MOTEUR RAG', 'Python\nFiches Markd` dans le traitement courant.
 [('INTERFACE', 'HTML, CSS, JavaScript\nChat, langues, sources et voix selon le navigateur.'), ('MOTEUR RAG', 'Python\nFiches Markdown, BM25, vecteurs en mémoire et reranker.'), ('SERVICES', 'Ollama : embeddings locaux\nGemini / Ollama / Claude : réponse selon configuration\nPostgreSQL : comptes et échanges')],
 # Cette ligne exécute `'L’interface permet le dialogue. FastAPI reçoit la question et orchestre les traitements. Le moteur RAG prépare et recherche les e` dans le traitement courant.
 'L’interface permet le dialogue. FastAPI reçoit la question et orchestre les traitements. Le moteur RAG prépare et recherche les extraits. Le modèle de réponse est indépendant du modèle d’embeddings, ce qui facilite le changement de fournisseur. PostgreSQL sert aux comptes et aux échanges : ce n’est pas la base vectorielle du projet. Les vecteurs sont conservés en mémoire. Enfin, des embeddings locaux ne rendent pas tout le traitement local : lorsque Gemini est utilisé, les textes nécessaires à cet appel sont envoyés au service distant.', 55),
# Cette ligne exécute `('Prévoir les erreurs pour garder un service utile',` dans le traitement courant.
('Prévoir les erreurs pour garder un service utile',
 # Cette ligne exécute `'Le système prévoit des replis et expose son état technique.',` dans le traitement courant.
 'Le système prévoit des replis et expose son état technique.',
 # Cette ligne exécute `[('EMBEDDINGS EN ÉCHEC', 'La recherche BM25 prend le relais.'), ('RERANKER EN ÉCHEC', 'Le classement initial est conservé.'), ('IN` dans le traitement courant.
 [('EMBEDDINGS EN ÉCHEC', 'La recherche BM25 prend le relais.'), ('RERANKER EN ÉCHEC', 'Le classement initial est conservé.'), ('INFORMATION MANQUANTE', 'Consigne de signaler le manque ; journalisation des questions concernées.')],
 # Cette ligne exécute `'Une chaîne avec plusieurs composants doit prévoir les pannes. Si les embeddings échouent, BM25 reste disponible. Si le reranker é` dans le traitement courant.
 'Une chaîne avec plusieurs composants doit prévoir les pannes. Si les embeddings échouent, BM25 reste disponible. Si le reranker échoue, le système conserve les candidats dans leur ordre initial. Le point de contrôle health permet de voir l’état de la recherche. Pour les informations absentes, les consignes demandent au modèle de le dire et le projet peut journaliser ces questions. Ces mécanismes améliorent la robustesse, mais ils ne prouvent pas la vérité de chaque réponse. Les sources affichées sont les extraits sélectionnés, pas une vérification automatique phrase par phrase.', 50),
# Cette ligne exécute `('Résultats mesurés : une base de comparaison claire',` dans le traitement courant.
('Résultats mesurés : une base de comparaison claire',
 # Cette ligne exécute `'Évaluation locale du 15 novembre 2026 • BM25 seul • 32 questions documentées',` dans le traitement courant.
 'Évaluation locale du 15 novembre 2026 • BM25 seul • 32 questions documentées',
 # Cette ligne exécute `[('50 % · HIT@1', '16 / 32\nLa section attendue est au premier rang.'), ('87,5 % · HIT@3', '28 / 32\nLa section attendue est parmi` dans le traitement courant.
 [('50 % · HIT@1', '16 / 32\nLa section attendue est au premier rang.'), ('87,5 % · HIT@3', '28 / 32\nLa section attendue est parmi les 3 premières.'), ('100 % · HIT@6', '32 / 32\nLa section attendue est parmi les 6 premières.')],
 # Cette ligne exécute `'J’ai exécuté l’évaluation disponible dans le projet. Avec BM25 seul, la section attendue arrive en première position pour seize q` dans le traitement courant.
 'J’ai exécuté l’évaluation disponible dans le projet. Avec BM25 seul, la section attendue arrive en première position pour seize questions sur trente-deux, dans les trois premières pour vingt-huit questions et dans les six premières pour toutes les questions du jeu. Cela mesure la recherche de sections, pas la justesse des réponses finales. Le score MRR est de zéro virgule soixante-neuf. Douze tests automatisés passent également, avec des services externes simulés. La comparaison chiffrée avec le mode hybride et le reranker reste à réaliser. Ce petit jeu doit aussi être relu, car il contient des questions sur des données locales non confirmées.', 65),
# Cette ligne exécute `('Démonstration : trois situations à montrer',` dans le traitement courant.
('Démonstration : trois situations à montrer',
 # Cette ligne exécute `'Activer les sources et ouvrir une nouvelle conversation pour chaque question.',` dans le traitement courant.
 'Activer les sources et ouvrir une nouvelle conversation pour chaque question.',
 # Cette ligne exécute `[('QUESTION DIRECTE', '« À quoi sert la zone de coupe P1 ? »\nObserver l’explication et la source.'), ('REFORMULATION', '« Où prép` dans le traitement courant.
 [('QUESTION DIRECTE', '« À quoi sert la zone de coupe P1 ? »\nObserver l’explication et la source.'), ('REFORMULATION', '« Où prépare-t-on les fils à la bonne longueur ? »\nVérifier que P1 est retrouvée.'), ('LIMITE DOCUMENTAIRE', '« Combien de jours de congé ai-je par an ? »\nVérifier que le bot ne devine pas.')],
 # Cette ligne exécute `'Pour la démonstration, je commence par une question directe. Je montre ensuite une reformulation afin d’observer si le même sujet` dans le traitement courant.
 'Pour la démonstration, je commence par une question directe. Je montre ensuite une reformulation afin d’observer si le même sujet est retrouvé. Enfin, je pose une question dont la réponse précise n’est pas documentée. Le comportement recherché est que le système reconnaisse ce manque. Je garde les sources visibles et j’ouvre une nouvelle conversation entre les questions pour limiter l’effet de l’historique. Avant la séance, je vérifie les services nécessaires. Si la connexion ne permet pas une démonstration, j’explique ce scénario sans présenter un résultat inventé comme une exécution réelle.', 90),
# Cette ligne exécute `('Ce que le projet apporte, et ce qu’il reste à valider',` dans le traitement courant.
('Ce que le projet apporte, et ce qu’il reste à valider',
 # Cette ligne exécute `'Un prototype intégré, avec une méthode d’amélioration progressive.',` dans le traitement courant.
 'Un prototype intégré, avec une méthode d’amélioration progressive.',
 # Cette ligne exécute `[('APPORTS', 'Connaissances structurées\nRecherche hybride et reranking\nExplications accessibles et sources'), ('LIMITES', 'Fiche` dans le traitement courant.
 [('APPORTS', 'Connaissances structurées\nRecherche hybride et reranking\nExplications accessibles et sources'), ('LIMITES', 'Fiches à faire valider par le métier\nQualité finale et latence à mesurer\nSécurité applicative à renforcer'), ('SUITE PRIORITAIRE', 'Comparer les 3 modes de recherche\nFaire tester par les utilisateurs\nEnrichir les fiches à partir des questions')],
 # Cette ligne exécute `'La valeur du projet est d’avoir relié une base documentaire, une recherche en plusieurs étapes et une interface accessible. Je di` dans le traitement courant.
 'La valeur du projet est d’avoir relié une base documentaire, une recherche en plusieurs étapes et une interface accessible. Je distingue ce qui est réalisé de ce qui reste à prouver. Avant une mise en production, il faut valider les contenus, renforcer notamment l’authentification et le contrôle d’accès, puis mesurer la qualité, les délais et les coûts. La prochaine expérience consiste à comparer BM25, hybride et hybride avec reranker sur les mêmes questions. Un test avec de vrais nouveaux employés permettra ensuite d’évaluer l’utilité pour la formation.', 50),
# Cette ligne exécute `('Rendre le savoir technique plus accessible',` dans le traitement courant.
('Rendre le savoir technique plus accessible',
 # Cette ligne exécute `'La contribution centrale : retrouver l’information utile avant de l’expliquer.',` dans le traitement courant.
 'La contribution centrale : retrouver l’information utile avant de l’expliquer.',
 # Cette ligne exécute `[('UN BESOIN CONCRET', 'Accompagner la compréhension des nouveaux arrivants.'), ('UN CHOIX TECHNIQUE', 'RAG hybride, fusion et rec` dans le traitement courant.
 [('UN BESOIN CONCRET', 'Accompagner la compréhension des nouveaux arrivants.'), ('UN CHOIX TECHNIQUE', 'RAG hybride, fusion et reclassement des extraits.'), ('UNE DÉMARCHE MESURABLE', 'Tests, évaluation et limites explicitement identifiées.')],
 # Cette ligne exécute `'Pour conclure, ce projet montre comment un assistant conversationnel peut rendre une documentation technique plus accessible. Son` dans le traitement courant.
 'Pour conclure, ce projet montre comment un assistant conversationnel peut rendre une documentation technique plus accessible. Son intérêt principal est la chaîne RAG : rechercher dans les fiches, combiner plusieurs méthodes, sélectionner les extraits, puis expliquer simplement. Le prototype est intégré et dispose de tests ainsi que d’une première mesure de recherche. L’étape suivante est de confirmer la qualité avec les utilisateurs et des contenus approuvés. Merci pour votre attention. Je suis à votre disposition pour vos questions.', 35),
# Cette ligne exécute `('Annexe · Les choix techniques à défendre',` dans le traitement courant.
('Annexe · Les choix techniques à défendre',
 # Cette ligne exécute `'À utiliser pendant les questions du jury.',` dans le traitement courant.
 'À utiliser pendant les questions du jury.',
 # Cette ligne exécute `[('POURQUOI PAS UN FINE-TUNING ?', 'Les connaissances sont fournies à la demande ; les fiches se mettent à jour sans réentraîner l` dans le traitement courant.
 [('POURQUOI PAS UN FINE-TUNING ?', 'Les connaissances sont fournies à la demande ; les fiches se mettent à jour sans réentraîner le modèle.'), ('POURQUOI PAS UNE BASE VECTORIELLE ?', '89 extraits : stockage en mémoire adapté au prototype ; persistance à étudier si le volume augmente.'), ('LE RAG ÉVITE-T-IL TOUTE ERREUR ?', 'Non. La sélection des sources et la génération doivent toutes les deux être évaluées.')],
 # Cette ligne exécute `'Cette diapositive est une réserve pour les questions. RRF additionne une contribution de 1 / (60 + rang) pour chaque liste. Le sc` dans le traitement courant.
 'Cette diapositive est une réserve pour les questions. RRF additionne une contribution de 1 / (60 + rang) pour chaque liste. Le score de fusion et le seuil de similarité ne sont pas des probabilités de vérité. Le seuil sémantique par défaut de 0,3 demande un ajustement expérimental. Le mode hybride avec reranker doit être comparé à BM25 dans les mêmes conditions. La présence d’une source n’est pas une preuve que toutes les affirmations de la réponse sont soutenues.', 0),
# Cette ligne exécute `]` dans le traitement courant.
]

# Cette ligne importe les dépendances nécessaires : from design_visuel import build_visual.
from design_visuel import build_visual

# Cette ligne affecte la variable `prs` avec `build_visual(slides, OUT)`.
prs = build_visual(slides, OUT)

# Cette ligne affecte la variable `guide` avec `['# Guide oral — Soutenance du chatbot RAG',`.
guide = ['# Guide oral — Soutenance du chatbot RAG',
         # Cette ligne exécute `'Durée indicative : 13 à 15 minutes, démonstration comprise. 15 diapositives principales et 1 annexe. Les notes sont également int` dans le traitement courant.
         'Durée indicative : 13 à 15 minutes, démonstration comprise. 15 diapositives principales et 1 annexe. Les notes sont également intégrées au PowerPoint (mode Présentateur).',
         # Cette ligne exécute `'## Avant la soutenance',` dans le traitement courant.
         '## Avant la soutenance',
         # Cette ligne exécute `'- Ajouter votre nom, votre établissement, votre encadrant et la date sur la première diapositive si nécessaire. Aucun nom ni logo` dans le traitement courant.
         '- Ajouter votre nom, votre établissement, votre encadrant et la date sur la première diapositive si nécessaire. Aucun nom ni logo d’entreprise n’a été inventé.\n- Répéter à voix haute avec un chronomètre. Expliquer les mots techniques avant de les employer.\n- Vérifier le démarrage du chatbot, Ollama, le modèle de réponse et la base si vous utilisez la connexion. Activer les sources.\n- Préparer des captures de vos propres essais réussis comme solution de secours. Les identifier comme captures, sans les présenter comme une démonstration en direct.\n- Ne pas afficher de clé API, de mot de passe ou de données personnelles.']
# Cette ligne parcourt `n, (title, subtitle, cards, speech, duration) in enumerate(slides, 1)` pour traiter chaque élément.
for n, (title, subtitle, cards, speech, duration) in enumerate(slides, 1):
    # Cette ligne ajoute la variable `guide` avec `[f'## Diapositive {n} — {title.replace(chr(10), " ")}', f'**Durée : {duration} s**' if duration else '**Annexe`.
    guide += [f'## Diapositive {n} — {title.replace(chr(10), " ")}', f'**Durée : {duration} s**' if duration else '**Annexe : à ouvrir si nécessaire.**', '**À dire :**\n\n'+speech]
# Cette ligne ajoute la variable `guide` avec `['## Questions probables du jury',`.
guide += ['## Questions probables du jury',
'''**Quelle est votre contribution principale ?**  
L’intégration d’une chaîne documentaire complète : fiches structurées, recherche BM25 et sémantique, fusion RRF, reranker avec validation de sa sortie, puis génération et affichage des sources. Le reranker constitue l’amélioration récente documentée du projet.

**Pourquoi ne pas interroger directement un modèle ?**  
Il n’a pas automatiquement accès aux fiches du projet. Le RAG lui apporte les extraits utiles au moment de la question et permet d’indiquer leur provenance.

**Avez-vous entraîné une intelligence artificielle ?**  
Non. J’utilise des modèles existants. Mon travail porte sur leur intégration, la recherche documentaire, le classement et l’application.

**Le reranker améliore-t-il vraiment la qualité ?**  
Un cas réel est documenté et les mécanismes techniques sont testés. Je n’ai pas encore mesuré un gain global. Il faut comparer les trois modes sur les mêmes questions, puis vérifier les réponses et les temps de traitement.

**100 % au Hit@6 signifie-t-il 100 % de bonnes réponses ?**  
Non. Cela signifie que la section attendue est dans les six premiers résultats sur les 32 questions du jeu actuel. Le modèle peut encore mal interpréter un passage. La qualité des documents eux-mêmes doit être validée.

**Pourquoi le jeu de questions doit-il évoluer ?**  
Il est petit et contient des questions liées à des informations locales non confirmées. Par exemple, retrouver une section mentionnant un nombre de machines ne valide pas ce nombre. Il faut relire les attentes avec le métier et ajouter des questions nouvelles, ambiguës et sans réponse.

**Que signifie MRR = 0,69 ?**  
C’est la moyenne de l’inverse du rang de la première section attendue : rang 1 donne 1, rang 2 donne 0,5. Plus le résultat est proche de 1, plus le passage attendu arrive tôt. Ce n’est pas un taux de vérité.

**Comment fonctionne RRF ?**  
Chaque extrait reçoit 1 / (60 + son rang) dans chaque liste où il apparaît. Les contributions sont additionnées. Cela évite de comparer directement un score BM25 et une similarité cosinus.

**Les données restent-elles toutes sur l’ordinateur ?**  
Non lorsque Gemini ou Claude est utilisé. Les embeddings Ollama sont locaux, mais le reclassement Gemini et la génération cloud transmettent les textes nécessaires au fournisseur. Une configuration entièrement locale suppose aussi de désactiver le reranker Gemini et de générer avec Ollama.

**Que se passe-t-il si aucune source ne répond ?**  
Le système peut reformuler la question puis utiliser un contexte général si aucun extrait n’est trouvé. Les consignes demandent au modèle de reconnaître les informations manquantes. Ce comportement doit être testé : il n’existe pas de garantie automatique de refus de toute réponse non fondée.

**Les sources sont-elles des citations vérifiées ?**  
L’interface montre les fiches et sections sélectionnées. Elle ne vérifie pas automatiquement chaque phrase de la réponse.

**Le chatbot remplace-t-il la formation sur machine ?**  
La portée défendable devant le jury est une aide pédagogique. Une procédure approuvée, l’habilitation et la supervision restent nécessaires pour les opérations. Le prompt actuel emploie une formulation de remplacement du formateur : ce point devra être revu avant un usage réel.

**Qu’est-ce qui manque pour une mise en production ?**  
La validation métier des fiches, une évaluation des réponses avec les utilisateurs, la sécurité des sessions et des droits d’accès, la gestion des données personnelles, la mesure de latence et de coût, et une supervision opérationnelle.

**Comment mettre les connaissances à jour ?**  
Modifier ou ajouter les fiches Markdown, puis redémarrer pour recharger les extraits et recalculer les embeddings. Aucun réentraînement du modèle de réponse n’est nécessaire.

**Le français, l’arabe et la voix sont-ils tous évalués ?**  
Le code prévoit des fonctions multilingues, une traduction de certaines questions et des fonctions vocales selon le navigateur. Leur qualité, notamment en darija, n’est pas démontrée par les tests RAG actuels.
''',
 # Cette ligne exécute `'## Preuves et périmètre des résultats',` dans le traitement courant.
 '## Preuves et périmètre des résultats',
 # Cette ligne exécute `'Vérifications exécutées le 15 novembre 2026 : `python -m unittest discover -s tests -p "test_*.py"` : 12 tests réussis ; `python ` dans le traitement courant.
 'Vérifications exécutées le 15 novembre 2026 : `python -m unittest discover -s tests -p "test_*.py"` : 12 tests réussis ; `python eval.py --mode bm25` : Hit@1 = 16/32, Hit@3 = 28/32, Hit@6 = 32/32, MRR = 0,69. Questions directes : Hit@3 = 17/18 ; indirectes : 11/14. Corpus chargé : 89 extraits, 9 fiches. Aucun appel réel hybride/reranker ni test de l’interface n’a été effectué pendant cette préparation.',
 # Cette ligne exécute `'Sources du projet : [moteur RAG](../rag.py), [application](../app.py), [évaluation](../eval.py), [tests](../tests/test_rag.py), [` dans le traitement courant.
 'Sources du projet : [moteur RAG](../rag.py), [application](../app.py), [évaluation](../eval.py), [tests](../tests/test_rag.py), [questions](../tests/questions.json), [améliorations documentées](../AMELIORATIONS_RAG.md), [portée des fiches](../SOURCES_FICHES.md).',
 # Cette ligne exécute `'Les validations réelles antérieures citées proviennent du document des améliorations ; elles ne sont pas des mesures refaites auj` dans le traitement courant.
 'Les validations réelles antérieures citées proviennent du document des améliorations ; elles ne sont pas des mesures refaites aujourd’hui. Les gains de temps, de précision et de productivité restent des bénéfices attendus, pas des résultats établis.',
 # Cette ligne exécute `'## Formulations à retenir',` dans le traitement courant.
 '## Formulations à retenir',
 # Cette ligne exécute `'« Le système recherche d’abord, puis il explique. »\n\n« Les tests valident des comportements techniques ; l’évaluation métier re` dans le traitement courant.
 '« Le système recherche d’abord, puis il explique. »\n\n« Les tests valident des comportements techniques ; l’évaluation métier reste indispensable. »\n\n« La valeur du projet est de rendre une documentation structurée accessible par une conversation simple. »']
# Cette ligne exécute `(OUT / 'Guide_oral_et_questions_jury.md').write_text('\n\n'.join(guide), encoding='utf-8')` dans le traitement courant.
(OUT / 'Guide_oral_et_questions_jury.md').write_text('\n\n'.join(guide), encoding='utf-8')
# Cette ligne écrit une information de suivi : `print(f'Créé : {len(slides)} diapositives avec notes ; durée indicative : {sum(s[4] for s in slides)} s.')`.
print(f'Créé : {len(slides)} diapositives avec notes ; durée indicative : {sum(s[4] for s in slides)} s.')
# Cette ligne exécute `"""Génère la présentation PowerPoint du projet à partir de contenu et de dessins."""` dans le traitement courant.
"""Génère la présentation PowerPoint du projet à partir de contenu et de dessins."""

