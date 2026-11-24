---
id: ZONE-CTRL
nom: Zone de contrôle
atelier: Contrôle qualité
postes_concernes: [opérateur test, contrôleur visuel, contrôle qualité]
version: 0.3
date_maj: 2026-11-07
statut: guide_general_non_valide_site
langue: fr
---

# Zone de contrôle

## 1. À quoi sert cette zone
La zone de contrôle **vérifie que chaque faisceau marche bien et qu'il est de bonne qualité**. Cette vérification a lieu **avant le stockage et l'expédition**.

Explication simple : on ne peut pas envoyer un faisceau au client s'il est défectueux. Dans une voiture, un seul fil mal branché peut empêcher une fonction de marcher. Ici, on trouve les défauts **avant** le départ.

## 2. Les postes de contrôle
| Poste | Rôle |
|---|---|
| Test électrique | Vérifie les connexions attendues et recherche les coupures, inversions et courts-circuits selon le programme. Étanchéité et verrouillages exigent des contrôles dédiés. |
| Test caméra | Contrôle de la présence et de la conformité des éléments de protection (relais, fusibles) montés sur le faisceau, conformément à l'instruction de travail. Les éléments réellement inspectés dépendent du programme validé du poste. |
| Inspection visuelle | Dernier contrôle des faisceaux conformes (appelé « contention »), avant étiquetage, emballage et envoi au client. |
| Firewall | Barrière qualité supplémentaire ciblant des défauts définis dans une liste de contrôle ; son périmètre local n’est pas documenté. |

## 3. Explication simple de chaque poste
- **Test électrique** : le faisceau est branché sur un **banc de test** (une machine avec un ordinateur). Elle envoie du courant dans chaque fil et vérifie :
  - que **chaque connexion est présente** (le courant passe là où il doit passer) ;
  - qu'il n'y a **pas de court-circuit** (deux fils qui se touchent par erreur) ;
  Un test électrique seul ne prouve pas l’**étanchéité des boîtiers** : celle-ci demande un essai dédié, par exemple un contrôle de fuite avec un équipement adapté et des seuils validés.
  Les **contacts encliquetés** et **verrouillages secondaires** doivent être contrôlés par les moyens mécaniques, visuels ou capteurs prévus. Une continuité correcte ne prouve pas leur retenue mécanique.
  La machine dit si le faisceau est bon ou mauvais.
- **Test caméra** : une caméra regarde le faisceau pour contrôler que les protections, comme les **relais** et les **fusibles**, sont bien là et conformes. Un fusible protège le circuit : si le courant est trop fort, il coupe. Le relais est un petit interrupteur électrique.
- **Inspection visuelle (contention)** : une personne regarde le faisceau **sur toutes ses faces**. C'est le **dernier contrôle** avant l'étiquetage, l'emballage et l'envoi au client.
- **Firewall** : contrôle supplémentaire de confinement de défauts, selon une liste qualité dédiée. Il ne remplace pas les contrôles précédents et ne désigne pas ici un pare-feu informatique.

## 4. Si un faisceau n'est pas bon
1. Arrêter le transfert de la pièce vers l'emballage.
2. Identifier le faisceau, son lot, le défaut, le poste et le résultat du test ; garder l'historique.
3. Le placer dans l'emplacement de non-conformité prévu, séparé des pièces acceptées.
4. Informer la qualité et le superviseur ; faire déterminer l'étendue du lot suspect.
5. Une personne autorisée décide de la retouche ou du rebut. Après retouche, refaire les contrôles prescrits et enregistrer la libération. Ne pas relancer un test jusqu'à obtenir un résultat favorable sans traiter la cause.

## 5. Règles de sécurité générales (à valider par le HSE)
- Ne pas toucher les contacts pendant un essai. Attendre la fin du cycle et la confirmation de mise en sécurité avant de connecter ou déconnecter le faisceau, particulièrement sur un banc haute tension. Respecter les protections et la notice.
- Ne jamais forcer un connecteur.
Les **EPI obligatoires** sont ceux indiqués sur l'affichage du poste et définis par l'évaluation HSE. La liste propre à cette usine n'est pas documentée. Exemples selon le risque : chaussures de sécurité pour les chutes de charges, lunettes pour les projections, protection auditive en zone bruyante. Les gants doivent être compatibles avec la tâche : ils peuvent être dangereux près d'organes tournants ou entraînants. Ne pas commencer une tâche si les protections requises sont absentes ou détériorées.

## 6. Erreurs de débutant à éviter
- Laisser passer un faisceau « presque bon ».
- Oublier de regarder toutes les faces pendant l'inspection.
- Ne pas signaler un défaut qui se répète.

## 7. Problèmes fréquents
- Circuit ouvert : connexion attendue absente ; faire rechercher fil coupé, terminal mal inséré ou défaut de raccordement au banc.
- Court-circuit ou inversion : isoler le faisceau ; vérifier le câblage avec le diagnostic et le plan.
- Test caméra NOK : conserver le résultat et vérifier référence, présence et position des composants ; ne pas modifier les seuils pour accepter la pièce.
- Défaut intermittent ou adaptateur usé : alerter la qualité et la maintenance ; ne pas attribuer automatiquement le défaut au faisceau.
- Programme incompatible avec la référence : suspendre le test et faire sélectionner le programme validé.

## 8. Qui contacter
- **Chef d'équipe / superviseur** : organisation, manque de matériel, anomalie et arrêt de production.
- **Qualité** : décision sur une pièce douteuse, isolement et autorisation de remise dans le flux.
- **Régleur ou maintenance habilitée** : réglage, panne ou intervention sur un équipement.
- **HSE et secouriste désigné** : risque, protection ou accident ; alerter immédiatement en cas de danger.
Les noms, numéros et emplacements locaux ne sont pas documentés. Utiliser l'annuaire interne et l'affichage du poste ; aucun contact nominatif n'est supposé dans cette fiche.

## 9. Vocabulaire
- **Banc de test** : machine qui teste électriquement un faisceau.
- **Court-circuit** : deux fils qui se touchent par erreur et qui ne devraient pas.
- **Continuité** : le courant passe bien d'un bout à l'autre du fil.
- **Étanchéité** : l'eau ou la poussière n'entre pas.
- **Verrouillage secondaire** : deuxième verrou qui garde le terminal en place.
- **Fusible / relais** : pièces de protection et de commande du circuit.
- **Contention** : confinement et contrôles renforcés d'un lot suspect ; le document initial emploie aussi ce terme pour l'inspection finale, un usage local non vérifié.
- **Conforme / non conforme** : bon ou mauvais par rapport à ce qui est demandé.


## Sources et portée de la fiche
Guide pédagogique général enrichi le 7 novembre 2026 à partir de ressources publiques et du document initial. Les étapes proposées sont une synthèse pédagogique, pas une procédure interne homologuée. Les sources publiques ne confirment ni l’organisation ni les paramètres de cette usine. Les notices, plans, instructions et règles HSE approuvés du site priment. Les références INRS servent de prévention générale, sans présumer du droit applicable au site.

- [Cirris — Testers](https://cirris.com/testers/)
- [Cirris — Resistance test thresholds](https://cirris.com/guidelines-for-setting-resistance-test-thresholds/)
- [INRS — Prévention des risques machines](https://www.inrs.fr/risques/utilisation-machines/prevention-risques-utilisation-machines)
- [INRS — Protection individuelle](https://www.inrs.fr/demarche/protection-individuelle/ce-qu-il-faut-retenir)
