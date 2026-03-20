# %%
"""
PROJET 1 - ANALYSE DE RENTABILITÉ CLIENT BANCAIRE
Auteur : Renée Michèle
Date : Mars 2026

Ce script analyse la rentabilité d'un portefeuille de 1000 clients bancaires.
Objectif : Segmenter les clients et identifier les leviers d'optimisation.
"""

# %%
# === IMPORTS ===
import duckdb
import pandas as pd


# %%
# === CONNEXION DUCKDB ===
con = duckdb.connect(':memory:')  # Base de données en mémoire
print("Connexion DuckDB créée")

# %%
# === CHARGEMENT DES DONNÉES ===

# Table clients
con.execute("""
    CREATE TABLE clients AS
    SELECT * FROM read_csv_auto('data/clients.csv')
""")
print("Table clients chargée")

# Table transactions
con.execute("""
    CREATE TABLE transactions AS
    SELECT * FROM read_csv_auto('data/transactions.csv')
""")
print("Table transactions chargée")

# Table produits
con.execute("""
    CREATE TABLE produits_souscrits AS
    SELECT * FROM read_csv_auto('data/produits_souscrits.csv')
""")
print("Table produits_souscrits chargée")

# Table recap_rentabilite
# %%
# === CHARGER LA TABLE RECAP_RENTABILITE ===
con.execute("""
    CREATE TABLE recap_rentabilite AS
    SELECT * FROM read_csv_auto('data/recap_rentabilite.csv')
""")
print("Table recap_rentabilite chargée")



# PROFIT TOTAL
result = con.execute("""
    SELECT SUM(profit_net) AS profit_total
           FROM recap_rentabilite
""").fetchdf()
print(result)

# PROFIT MOYEN
result = con.execute("""
    SELECT AVG(profit_net) AS profit_moyen
           FROM recap_rentabilite
""").fetchdf()
print(result)

# REPARTITION PAR SEGMENT
result = con.execute("""
    SELECT segment_calcule,
           COUNT(*) AS nb_clients,
           ROUND(COUNT(*) * 100.0/ (SELECT COUNT(*) FROM recap_rentabilite),1) AS pourcentage
           FROM recap_rentabilite
           GROUP BY segment_calcule
           ORDER BY nb_clients DESC
""").fetchdf()
print(result)


# TOP 20 CLIENTS
result = con.execute("""
    SELECT client_id,
           ROUND(profit_net, 2) AS profit_net,
           segment_calcule
           FROM recap_rentabilite
           ORDER BY profit_net desc
           LIMIT 20
""").fetchdf()
print(result)


# BOTTOM 20 CLIENTS
result = con.execute("""
    SELECT client_id,
           ROUND(profit_net, 2) AS profit_net,
           segment_calcule
           FROM recap_rentabilite
           ORDER BY profit_net ASC
           LIMIT 20
""").fetchdf()
print(result)

# Principe de Pareto
result = con.execute("""
       WITH top_200 AS (
       SELECT SUM(profit_net) AS profit_top
        FROM (
            SELECT profit_net
            FROM recap_rentabilite
            ORDER BY profit_net DESC
            LIMIT 200
        ) AS top_clients
        ),
        total AS (
            SELECT SUM(profit_net) AS profit_total
            FROM recap_rentabilite
        )
        SELECT
             top_200.profit_top,
             total.profit_total,
             ((top_200.profit_top / total.profit_total)*100) AS pourcentage
             FROM top_200, total
""").fetchdf()
print(result)

# Produits les plus rentables
result = con.execute(""" SELECT produit,
       SUM(profit_annuel) AS sum_profit,
       COUNT(client_id) AS nombre_de_client,
       AVG(profit_annuel) AS profit_moyen_par_produit
FROM produits_souscrits
GROUP BY produit
ORDER BY sum_profit DESC
""").fetchdf()
print("les plus rentables :")
print(result)

# Nombre de clients par produit
result = con.execute("""SELECT produit,
       COUNT(client_id) AS nombre_de_client
FROM produits_souscrits
GROUP BY produit
ORDER BY nombre_de_client DESC
""").fetchdf()
print("Nombre de clients par produit :")
print(result)

#  Produits des clients VIP
result = con.execute("""SELECT p.produit,
       COUNT(p.client_id) AS nombre_de_client
FROM produits_souscrits p
INNER JOIN recap_rentabilite r ON p.client_id = r.client_id
WHERE r.segment_calcule = 'VIP'
GROUP BY p.produit
ORDER BY nombre_de_client DESC
""").fetchdf()
print("Produits des clients VIP :")
print(result)

# Rentabilité par type d'emploi
result = con.execute("""SELECT c.emploi,
       SUM(r.profit_net) AS sum_profit,
       AVG(r.profit_net) AS avg_profit,
       COUNT(c.client_id) AS nombre_de_clients
FROM clients c
INNER JOIN recap_rentabilite r ON c.client_id = r.client_id
GROUP BY c.emploi
ORDER BY avg_profit DESC
""").fetchdf()
print("Rentabilité par type d'emploi :")
print(result)

#  Part transactions vs produits dans le revenu
result = con.execute("""SELECT SUM(revenus_transactions) AS revenus_transactions_total,
       SUM(revenus_annuels) AS revenus_produits_total,
       ROUND((SUM(revenus_transactions)/(SUM(revenus_transactions)+SUM(revenus_annuels))*100),1) AS pct_revenus_transactions,
       ROUND((SUM(revenus_annuels)/(SUM(revenus_transactions)+SUM(revenus_annuels))*100),1) AS pct_revenus_produits
FROM recap_rentabilite
""").fetchdf()
print("Part transactions vs produits dans le revenu :")
print(result)


# Part de Cadre avec le crédit immobilier
result = con.execute("""WITH total_cadre AS (
    SELECT COUNT(client_id) AS nombre_total_cadre
    FROM clients
    WHERE emploi = 'Cadre'
),
cadre_immobilier AS (
    SELECT COUNT(c.client_id) AS nombre_credit_immobilier
    FROM clients c
    INNER JOIN produits_souscrits p ON c.client_id = p.client_id
    WHERE c.emploi = 'Cadre'
    AND p.produit = 'Crédit Immobilier'
)
SELECT
    ca.nombre_credit_immobilier,
    tc.nombre_total_cadre,
    ROUND((ca.nombre_credit_immobilier / tc.nombre_total_cadre) * 100, 1) AS pourcentage
FROM cadre_immobilier ca, total_cadre tc
""").fetchdf()
print("Part de Cadre avec le crédit immobilier:")
print(result)
