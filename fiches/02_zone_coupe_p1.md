---
id: ZONE-P1-COUPE
nom: Zone de coupe P1
atelier: Coupe
machines: Komax (inventaire local non vérifié)
postes_concernes: [opérateur coupe, régleur]
version: 0.3
date_maj: 2026-11-07
statut: guide_general_non_valide_site
langue: fr
---

# Zone de coupe P1

## 1. À quoi sert cette zone
La zone de coupe (P1) **prépare les fils** pour toutes les autres zones. Elle les fournit dans la **bonne quantité**, avec la **bonne qualité**, et **au bon moment**.

Le document initial mentionne **29 machines automatiques de marque Komax**, sans inventaire vérifiable. Ce nombre reste une donnée locale non confirmée. Ces machines **coupent les fils à la longueur demandée**.

Explication simple : un faisceau de câbles est un grand nombre de fils de longueurs différentes. Dans la zone P1, on coupe d'abord tous ces fils, un par un, à la bonne longueur. C'est la première étape de la fabrication.

## 2. Paramètres de coupe
Les trois réglages importants sont :
- **La longueur du fil** : de combien de centimètres on coupe.
- **Le dénudage** : on enlève la gaine en plastique du bout du fil, pour voir le cuivre. Il faut respecter la longueur à dénuder.
- **Le sertissage** : on fixe une pièce métallique (une cosse, aussi appelée terminal) au bout du fil. La machine l'écrase pour qu'elle tienne solidement.

Lire les valeurs et tolérances sur l’OF, le plan et la spécification applicables au couple fil-terminal : longueur coupée, longueur dénudée et caractéristiques du sertissage. Vérifier les unités et la version du document. Il n’existe pas de valeur universelle ; sans spécification approuvée, ne pas régler ni lancer la série.

## 3. Explication simple d'un fil
Un fil électrique a deux parties :
- le **cuivre** au centre (c'est lui qui conduit l'électricité) ;
- l'**isolant** autour (le plastique coloré qui protège).

Quand on dénude, on retire seulement l'isolant, sans abîmer le cuivre. Si on coupe des brins de cuivre, le fil devient moins bon : c'est un défaut.

## 4. Utilisation de base
Les étapes générales d'une machine de coupe (à confirmer pour chaque machine Komax) :
1. Charger la **bobine** de fil (le rouleau de fil) sur la machine.
2. Lancer l'**OF** (ordre de fabrication) : c'est l'ordre qui dit quoi produire, combien, et à quelle longueur.
3. Contrôler les **premières pièces** avant de continuer la production.
4. Surveiller la machine pendant qu'elle produit.

Comment on apprend : le formateur explique d'abord le fonctionnement des machines Komax, les paramètres de coupe et les critères de qualité. Le nouvel employé **regarde** d'abord, puis **pratique sur la machine, sous supervision**.

Avant le démarrage, un opérateur formé vérifie l'OF, les références du fil et des terminaux, les protections et la disponibilité du contrôle première pièce. Le chargement, l'enfilage et le choix du programme suivent la notice du modèle et l'instruction du poste. Ne pas modifier une recette sans autorisation. Après validation de la première pièce, surveiller les alarmes et identifier les lots produits.
Pour un arrêt normal, utiliser la commande prévue par la notice, attendre l'immobilisation et enregistrer les quantités. Pour un danger immédiat, utiliser l'arrêt d'urgence si accessible sans risque. L'arrêt d'urgence ne remplace pas la consignation. Les commandes et codes d'alarme dépendent du modèle Komax et ne sont pas documentés ici.

## 5. Règles de sécurité générales (à valider par le HSE)
- Ne jamais mettre la main dans une machine en marche.
- Ne jamais ouvrir un carter de protection quand la machine fonctionne.
- En cas de danger : appuyer sur l'arrêt d'urgence et prévenir le superviseur.
Les **EPI obligatoires** sont ceux indiqués sur l'affichage du poste et définis par l'évaluation HSE. La liste propre à cette usine n'est pas documentée. Exemples selon le risque : chaussures de sécurité pour les chutes de charges, lunettes pour les projections, protection auditive en zone bruyante. Les gants doivent être compatibles avec la tâche : ils peuvent être dangereux près d'organes tournants ou entraînants. Ne pas commencer une tâche si les protections requises sont absentes ou détériorées.

## 6. Contrôle qualité
Points à regarder sur un fil coupé :
- La longueur est-elle bonne ?
- Le dénudage est-il propre, sans brins de cuivre coupés ?
- Le sertissage est-il bien fait, la cosse bien serrée ?
Utiliser les instruments prévus et vérifiés : règle ou dispositif de longueur, moyen de mesure du dénudage, micromètre de sertissage adapté. Le test de traction est réalisé sur les échantillons désignés avec le matériel prévu ; ne pas remettre une pièce soumise à un essai destructif dans la production. Comparer chaque résultat aux limites de la spécification fil-terminal et enregistrer le contrôle. La fréquence et les seuils relèvent du plan de contrôle, pas d’une valeur générique.

## 7. Erreurs de débutant à éviter
- Ne pas vérifier la première pièce.
- Changer un réglage sans l'accord du régleur.
- Continuer à produire quand un fil semble mal dénudé.

## 8. Problèmes fréquents
- **Alarme Komax** : arrêter la production selon la notice, relever le code exact, le modèle, l'OF et le symptôme ; prévenir le régleur. Ne pas réarmer plusieurs fois ni contourner une sécurité. Reprendre après résolution autorisée et contrôle de la première pièce.
- **Fil mal dénudé, brins coupés, cosse déformée ou mauvaise longueur** : séparer les pièces suspectes depuis le dernier contrôle conforme ; faire vérifier fil, outillage et réglage par la personne autorisée.
- **Bobine bloquée ou fil coincé** : ne pas tirer dans le mécanisme et ne pas introduire la main ; faire intervenir le personnel habilité.
- **Sécurité des lames** : ne jamais toucher les lames ni enlever les déchets dans la zone dangereuse. Nettoyage, débourrage et remplacement nécessitent la mise en sécurité prévue, avec consignation par une personne habilitée lorsque nécessaire.

## 9. Qui contacter
- **Chef d'équipe / superviseur** : organisation, manque de matériel, anomalie et arrêt de production.
- **Qualité** : décision sur une pièce douteuse, isolement et autorisation de remise dans le flux.
- **Régleur ou maintenance habilitée** : réglage, panne ou intervention sur un équipement.
- **HSE et secouriste désigné** : risque, protection ou accident ; alerter immédiatement en cas de danger.
Les noms, numéros et emplacements locaux ne sont pas documentés. Utiliser l'annuaire interne et l'affichage du poste ; aucun contact nominatif n'est supposé dans cette fiche.

## 10. Vocabulaire
- **Komax** : la marque des machines automatiques de coupe.
- **OF (ordre de fabrication)** : l'ordre qui dit quoi produire et en quelle quantité.
- **Dénudage** : retirer l'isolant au bout du fil.
- **Sertissage** : fixer une cosse au bout du fil en l'écrasant.
- **Cosse (terminal)** : petite pièce métallique au bout d'un fil.
- **Bobine** : rouleau de fil.
- **Tolérance** : la petite différence acceptée par rapport à la valeur demandée.


## Sources et portée de la fiche
Guide pédagogique général enrichi le 7 novembre 2026 à partir de ressources publiques et du document initial. Les étapes proposées sont une synthèse pédagogique, pas une procédure interne homologuée. Les sources publiques ne confirment ni l’organisation ni les paramètres de cette usine. Les notices, plans, instructions et règles HSE approuvés du site priment. Les références INRS servent de prévention générale, sans présumer du droit applicable au site.

- [Komax — Wire processing](https://www.komaxgroup.com/en/products/wire-processing)
- [TE Connectivity — Splices FAQ](https://www.te.com/en/faqs/splices.html)
- [INRS — Prévention des risques machines](https://www.inrs.fr/risques/utilisation-machines/prevention-risques-utilisation-machines)
- [INRS — Protection individuelle](https://www.inrs.fr/demarche/protection-individuelle/ce-qu-il-faut-retenir)
