Analyse de Rentabilité Client - Secteur Bancaire

Contexte du Projet:

La rentabilité d'une banque dépend de la rentabilité de ces clients.
Nous avons ici une banque de 1000 clients.

Problématique : Dans cet établissement bancaire de 1000 clients, le but de cette analyse sera de trouver les leviers d'optimisation de rentabilité de la banque.

---

Résultats principaux:

Rentabilité globale
Le profit total de l'entreprise est de 1,19 M€.
Le profit moyen par client est de 1 193 €

Segmentation
-4,5% clients sont des clients VIP et on un profit supérieur à 500€. Il représente 645 clients.
-35,4% clients sont des clients Standard et on un profit entre 0 et 500 euros. Il représente 354 clients.
-0,1% clients sont des clients Déficitaires et on un profit inférieur à 0. Cela représente un seul client.

Insights & Analyse Business

Le profit de la banque n'est pas concentrée que sur une partie de ces clients.
Les 20% de clients les plus rentables (200 clients) génèrent 57% du profit total.
La banque a donc un équilibre modérée de son profit et ne dépend pas que de quelques gros clients
La base de client reste diversifiée.


---

Dataset

-Table 1 Clients
1.client_id
2.nom_complet
3.age
4.emploi
5.balance_moyenne
6.date_acquisition
7.ancienneté_mois
8.coût acquisition
9.segment

-Table 2 Transactions
1.transaction_id
2.client_id
3.date_transaction
4.type_transaction
5.montant
6.frais_générés

-Table 3 Produits_souscrits
1.client_id
2.produit
3.revenus_annuels
4.coût_gestion_annuel
5.profit_annuel

-Table 4 Recap_rentabilite
1.client_id
2.revenus_transactions
3.revenus_annuels
4.coûts_totaux
5.profit_net
6.segment_calcule

---

Technologies Utilisées

- SQL (DuckDB) - Analyses de données et requêtes complexes (CTEs, window functions, agrégations)
- Python - Génération de données réalistes et automatisation
- Pandas - Manipulation et traitement de données

---

Méthodologie

1. Génération des Données à l'aide d'un script python
Création d'un dataset bancaire réaliste avec distributions cohérentes :
- Table Clients
- Table Transactions
- Table Produits souscrits
- Table Récap Rentabilité

2. Calcul de Rentabilité
3. Segmentation client
4. Analyse de la rentabilité clients

---

Compétences développées

Génération d'un script python grâce à l'IA
Requêtes SQL - Common Table Expressions (CTEs)



À Propos

Renée Michèle Niangoran
Data Analyst
10 ans d'expérience dans le domaine financier
